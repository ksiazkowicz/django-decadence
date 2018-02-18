import json
from django.db import models
from django.conf import settings
from django.core.serializers import serialize
from .helpers import update


class SerializableQuerySet(models.QuerySet):
    """
    QuerySet extended with Decadence serialization method
    """
    def serialized(self, user):
        return [x.serialize(user) for x in self]


class DecadenceManager(models.Manager):
    def get_queryset(self):
        return SerializableQuerySet(self.model, using=self._db)


class DecadenceModel(models.Model):
    """
    Implements a generic model that supports Decadence-specific features like
    serialization.
    """
    updates_excluded = []
    """list of fields excluded from updates"""

    objects = DecadenceManager()

    class Meta:
        abstract = True

    def get_update_path(self, field_name):
        return "%(namespace)s-%(pk)d-%(field)s" % {
            "namespace": str(self._meta),
            "pk": self.pk,
            "field": field_name
        }


    def push_update(self, original_data={}):
        """
        Compares changes between old serialization data and new, then pushes out updates through Updates API.
        """
        if not original_data:
            return False

        # try to serialize first
        new_data = self.serialize()

        # compare all the fields!
        for key, value in original_data.items():
            # check if key is excluded first
            if key in self.updates_excluded:
                continue

            # get value and compare
            new_value = new_data.get(key)

            if new_value != value:
                # first check if custom update for this field exists in case we need to override it
                # (for example, href attribute)
                try:
                    logic = getattr(self, "updates_%s" % key)

                    # this field might also be a callable for some reason
                    if callable(logic):
                        logic = logic()
                except AttributeError:
                    logic = [{"type_name": "update_value", }, ]

                # handle each operation
                for operation in logic:
                    # copy operation dictionary
                    options = operation.copy()

                    # "value" field is optional
                    if not "value" in options.keys():
                        options["value"] = new_value

                    # add "path" to options
                    options["path"] = self.get_update_path(operation.get("field", key))

                    # pop "field" value from "options" if provided
                    try:
                        options.pop("field")
                    except KeyError:
                        pass

                    update(**options)


    def serialize(self, user=None, fields=None):
        """
        Attempts to generate a JSON serializable dictionary
        based on current model
        """
        # you might want to define a list of fields to be serialized
        if not fields:
            if hasattr(self, "decadence_fields"):
                fields = self.decadence_fields
            else:
                fields = [f.name for f in self._meta.get_fields()]

        # use Django's built-in model serialization
        serialized = json.loads(serialize('json', [self], fields=fields))[0]["fields"]
        serialized["id"] = self.pk

        # begin serialization
        for field in fields:
            value = ""

            # try to call serialize_fieldname function first
            try:
                value = getattr(self, "serialize_%s" % field)(user)
            except AttributeError:
                # use default serialization if function is not defined
                original_value = getattr(self, field)

                # check if is callable and call it
                if callable(original_value):
                    original_value = original_value(user)

                # run custom serialization
                if type(original_value) in [str, bool, int, ]:
                    # nothing to do here
                    value = original_value
                elif isinstance(original_value, DecadenceModel):
                    # nested Decadence serialization
                    value = original_value.serialized()
                elif isinstance(original_value, models.Model):
                    # check for fields overrides
                    overrides = []
                    if hasattr(settings, "DECADENCE_FIELD_OVERRIDES"):
                        overrides = settings.DECADENCE_FIELD_OVERRIDES.get(str(original_value._meta), [])

                    # use overrides if provided and use Django serializer
                    if len(overrides) > 0:
                        fields = json.loads(serialize('json', [original_value], fields=overrides))
                    else:
                        fields = json.loads(serialize('json', [original_value]))
                    fields = fields[0]["fields"]

                    # add pk to fields
                    fields["id"] = original_value.pk
                    value = fields
                else:
                    continue
            
            # save serialized value
            serialized[field] = value

        serialized["update_namespace"] = str(self._meta)
        return serialized

