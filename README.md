=====
Decadence
=====

Decadence allows you to use your Django templates from JS for dynamically
loaded content. Please, just get a real JS templating engine instead
and don't use it on production.

Quick start
-----------

1. Add "django_decadence" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_decadence',
    ]

2. Include the decadence URLconf in your project urls.py like this::

    url(r'^decadence/', include('decadense.urls')),

3. Put your templates in templates/includes/decadence

4. ...