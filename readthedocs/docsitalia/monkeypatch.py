"""
Monkeypatches ``Project`` model to keep the size to 255 characters up from 63 since RTD 2.8.1.

RTD changed the name / slug length to 63 chars to fit DNS restrictions as they use the project
slug as third level domain (don't ask me why the restricted the name to the same length).

As we only use in a normal path we don't have such restrictions and we have a lot of long names,
we must revert this change.
Plus they changed a field type and we have to make sure our data fits correctly in the new type

* migration projects.0030_change-max-length-project-slug is modified in a noop (code is
  commented to clarify the original scope of the migration).
* monkeypatch `Project` to set field length and validator to our length to let things work at
  runtime (forms validation etc).  monkeypatch has been preferred over changing existing code
  to reduce the chances of conflicts.
"""

from django.core import validators

from readthedocs.projects.models import Project


def monkey_patch_project_model():
    """
    Revert changes in 8d2ee29de95690a9cd72d4f2a0b4131a44449928.

    They changed the original values as any domain part can't be longer than 63 chars
    but we don't have this limitation.
    """
    fields = ["name", "slug"]
    field_length = 255
    for field in fields:
        fieldobj = Project._meta.get_field(field)
        fieldobj.max_length = field_length
        for validator in fieldobj.validators:
            if isinstance(validator, validators.MaxLengthValidator):
                validator.limit_value = field_length


monkey_patch_project_model()
