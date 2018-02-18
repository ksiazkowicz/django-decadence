Decadence
=========

[![Documentation Status](https://readthedocs.org/projects/django-decadence/badge/?version=latest)](http://django-decadence.readthedocs.io/en/latest/?badge=latest)


Decadence is a library which enables creating dynamic, constantly updating webpages with Django. It consists of three elements:

- Serializable models - so you have a consistent way of displaying and accessing data
- Rendering API - exposes Django’s templating engine so you can use it from JS in your frontend
- Updates API - allows fields to be updated in real time over WebSocket protocol

You don’t need to use all of these elements if you don’t want to.

The main motivation behind this library is that you don’t have to switch over to a fancy JS framework nor duplicate rendering logic in both JS and Django templates for content loaded over AJAX/WebSocket protocols.

Quick start
-----------

1. Add "django_decadence" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_decadence',
    ]

2. Include the decadence URLconf in your project urls.py like this::

    url(r'^decadence/', include('django_decadence.urls')),

3. Put your templates in templates/includes/decadence

4. ...