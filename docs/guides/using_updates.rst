Using Updates API
#################

Updates API provides automatic content updates, for example, when post
title is changed, this change will be broadcast to all users that are
currently browsing the page.

General idea
------------

Updates API is exposed over WebSocket protocol at
``ws://localhost/updates``. New values are broadcast to Groups named in
this fashion: ``[namespace]-[object id]-[path]``:

-  namespace - for example, a name of model we're updating,
-  object id - pk of this object,
-  path - unique identifier that describes a specific field, for example
   title

For 23rd user's like status , we'd use something like:
``post-1-like.23``.

To be a part of such Group, client needs to send a subscription request.

::

    {
        "subscribe": true,
        "group": "post-1-like.23",
    }

Where ``subscribe`` field can be either true or false (in case client
wants to unsubscribe specific group).

Whenever field was updated with new data, server will send a message
that looks like this:

::

    {
        "type": "update_value",
        "path": "post-1-like.23",
        "value": "1"
    }

-  ``type`` - type of change Server asks client to apply. Available
   types are:

   -  ``update_value`` - value (ex. innerHTML of an Element containing
      this field) should be updated to ``value``
   -  ``toggle_class`` - class (ex. ``hidden`` of an Element
      corresponding to this field) defined in ``class`` field should be
      either added or removed to an Element
   -  ``update_attribute`` - attribute (ex. ``data-liked`` of an Element
      corresponding to this field) named ``attribute_name`` should be
      changed to ``value``

-  ``path`` - group name (field name)
-  ``value`` - new value

Optional parameters:

-  ``class`` - name of class to toggle (only in ``toggle_class``)
-  ``attribute_name`` - name of attribute, which value will be changed

Usage (Django)
--------------

Template
~~~~~~~~

There is also a template tag available at ``update_tags`` called
``updatable``.

Usage:

::

    {% updatable post "content" %}

This tag will include ``<span>`` element with all required data
attributes to enable automatic updates using ``UpdateListener``.

You can also add ``safe=True`` as argument if you want string to be marked as safe.

Model
~~~~~

General idea is, that if you already use serialization features from
Decadence in your model, you will usually send out a few "update_value"
requests during save(). To avoid reimplementing this from scratch for
each model and simplify integration, push_update method is provided.

To avoid updating certain fields (upload date for blog post?), you can add
this field in model:

::

        updates_excluded = []

Fields from this list will never get checked for changes and won't trigger
any errors.

By default, each change will result in ``update_value`` request being
broadcast. In case you want to override this behaviour, you can define a
list of options with which ``update()`` method will be called for
specific field. A common case could be, for example, updating an URL to
image if it changed. You can either define it as a list, or a method
which returns it.

::

        # as method, in case you need to override default value or something, in this case field is called "is_hidden"
        def updates_is_hidden(self):
            return [{
                "type_name": "toggle_class",   # use toggle_class instead of 
                "field": "main-div",           # in case you want to override path
                "classname": "hidden",
                "value": not self.is_hidden,   # override value, optional
            }, ]

        # as list, in this case field is called "image"
        updates_image = [{
            "type_name": "update_attribute",
            "attribute_name": "src",
        }, ]

One final step is overriding ``save()`` method, capturing data before
``save()`` and calling ``push_update()`` with captured data as an
argument.

::

        def save(self, *args, **kwargs):
            original_data = None
            if self.pk:
                old = ExampleModel.objects.get(pk=self.pk)
                original_data = old.serialize()
            super(ExampleModel, self).save(*args, **kwargs)
            self.push_update(original_data)

Low-level
~~~~~~~~~

To send out updates, you need to either override ``save()`` method on a
model or use signals.

Example:

::

    from django_decadence import update

    ...
    update(type_name="update_value", path="post-1-like.23", value="1");
    ...

Usage (TypeScript)
------------------

To simplify the process of subscribing to specific fields, there is a
client for Updates API available globally under window.UpdateListener.

``UpdateListener`` automatically captures all elements in ``document``
that have ``data-update-group`` attribute containing a valid Group name.
For dynamically created Elements, you need to call UpdateListener again:
``window["UpdateListener"].init(element)``. Decadence does this
automatically.