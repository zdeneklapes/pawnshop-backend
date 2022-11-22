from config.settings import *  # noqa: F401 # pylint: disable=W0401
import config.settings as django_settings

django_settings.__dict__["AUTH"] = True
