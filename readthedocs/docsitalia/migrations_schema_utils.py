"""
Contain migrations utilities that allows to create migrations targeted to external applications.

In this context yhis is useful to patch upstream models from within the docsitalia app.

It must be used with *great* care as it may lead to an inconsistent state between the models.
"""

from django.db import migrations


class AddField(migrations.AddField):

    """Adds app_label parameter to AddField migration to allow migrating other apps fields."""

    def __init__(self, *args, **kwargs):
        if 'app_label' in kwargs:
            self.app_label = kwargs.pop('app_label')
        else:
            self.app_label = None
        super(AddField, self).__init__(*args, **kwargs)

    def state_forwards(self, app_label, state):
        super(AddField, self).state_forwards(self.app_label or app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        super(AddField, self).database_forwards(
            self.app_label or app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        super(AddField, self).database_backwards(
            self.app_label or app_label, schema_editor, from_state, to_state)


class AlterField(migrations.AlterField):

    """Adds app_label parameter to AlterField migration to allow migrating other apps fields."""

    def __init__(self, *args, **kwargs):
        if 'app_label' in kwargs:
            self.app_label = kwargs.pop('app_label')
        else:
            self.app_label = None
        super(AlterField, self).__init__(*args, **kwargs)

    def state_forwards(self, app_label, state):
        super(AlterField, self).state_forwards(self.app_label or app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        super(AlterField, self).database_forwards(
            self.app_label or app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        super(AlterField, self).database_backwards(
            self.app_label or app_label, schema_editor, from_state, to_state)


class RemoveField(migrations.RemoveField):

    """Adds app_label parameter to RemoveField migration to allow migrating other apps fields."""

    def __init__(self, *args, **kwargs):
        if 'app_label' in kwargs:
            self.app_label = kwargs.pop('app_label')
        else:
            self.app_label = None
        super(RemoveField, self).__init__(*args, **kwargs)

    def state_forwards(self, app_label, state):
        super(RemoveField, self).state_forwards(self.app_label or app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        super(RemoveField, self).database_forwards(
            self.app_label or app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        super(RemoveField, self).database_backwards(
            self.app_label or app_label, schema_editor, from_state, to_state)
