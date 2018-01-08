import os
from django.conf import settings


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
