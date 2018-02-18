Decadence
=========

Decadence is a library which enables creating dynamic, constantly updating
webpages with Django. It consists of three elements:

- Serializable models - so you have a consistent way of displaying and accessing data
- Rendering API - exposes Django's templating engine so you can use it from JS in your frontend
- Updates API - allows fields to be updated in real time over WebSocket protocol

You don't need to use all of these elements if you don't want to.

The main motivation behind this library is that you don't have to switch over to
a fancy JS framework nor duplicate rendering logic in both JS and Django templates for
content loaded over AJAX/WebSocket protocols.

.. toctree::
   :maxdepth: 2
   :caption: Guides:

   guides/getting_started
   guides/using_updates

.. toctree::
   :maxdepth: 2
   :caption: API reference:

   decadence/consumers
   decadence/helpers
   decadence/models
   decadence/views
   decadence/templatetags

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
