from django.db import models
from datetime import datetime, date, time
from django.template import Context, Template
import json


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
    objects = DecadenceManager()


    class Meta:
        abstract = True


    def serialize(self, user=None):
        """
        Attempts to generate a JSON serializable dictionary
        based on current model
        """
        # you might want to define a list of fields to be serialized
        try:
            fields = self.decadence_fields
        except:
            fields = [f.name for f in self._meta.get_fields()]

        # begin serialization
        serialized = {}
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
                    original_value = original_value()

                # choose method based on field type
                if type(original_value) in [str, bool, int, ]:
                    # nothing to do here
                    value = original_value
                if type(original_value) in [datetime, date, time, ]:
                    # use Django template engine for cool verbose date string
                    value = Template("{{ date }}").render(Context({"date": self.date}))
                else:
                    # try to use Python's JSON serialization as fallback
                    # probably will NEVER EVER work but shhhhh...
                    value = json.loads(json.dumps(original_value))
            
            # save serialized value
            serialized[field] = value

        return serialized

