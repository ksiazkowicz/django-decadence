Getting Started
###############

To use Decadence in your project, first install it using pip

::

    pip install -e git://github.com/ksiazkowicz/django-decadence.git#egg=django-decadence


Then, add Decadence to ``INSTALLED_APPS`` in ``settings.py``

::

    INSTALLED_APPS = {
        ...
        "django_decadence",
        ...
    }


If you want to use Updates API, you also need to update your ``routing.py`` file

::

    from django_decadence.consumers import UpdateConsumer

    channel_routing = [
        ...
        route_class(UpdateConsumer, path=r"^/updates$"),
        ...
    ]


For Rendering API, add following lines to your url_patterns:

::

    url(r'^decadence/', include('django_decadence.urls')),


To be continued