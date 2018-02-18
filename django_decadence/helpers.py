import os
import json
from django.conf import settings
from channels import Group



DECADENCE_DIR = getattr(settings, "DECADENCE_DIR", os.path.join("includes", "decadence"))


def check_template_path(path):
    """
    Checks whether the path is valid. Valid path is a path that:
    - is not outside DECADENCE_DIR (default: templates/includes/decadence)
    - ...
    """
    # normalize path
    normalized = os.path.normpath(path)

    if not normalized.startswith(DECADENCE_DIR):
        raise Exception("Template path '%s' is outside '%s'" % normalized, DECADENCE_DIR)


def update(type_name="update_value", path="", value="", classname="",
           attribute_name=""):
    """
    Pushes out content updates to user through our update channel.

    :param type_name: type of content update:

        - toggle_class - adds/remove given class from element, if value is 
                         true, it's added
        - update_attribute - replaces html attribute value with given value
        - update_value - updates content of html element with given value

    :param path: name of update group
    :param value: new value
    :param classname: name of class to be added/removed to element (optional)
    :param attribute_name: name of attribute which value will be replaced 
                           (optional)
    """
    # default data
    data = {
        "type": type_name,
        "value": value,
        "path": path,
    }

    # add optional arguments for different types
    if type_name == "toggle_class":
        data["class"] = classname
    if type_name == "update_attribute":
        data["attribute_name"] = attribute_name

    Group(path).send({"text": json.dumps(data)})
