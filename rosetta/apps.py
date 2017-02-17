from django.apps import AppConfig
from django.db.models.signals import post_save
from rosetta.conf import settings as rosetta_settings


def add_to_translators(sender, **kwargs):
    from django.contrib.auth.models import Group
    user = kwargs["instance"]
    if kwargs["created"]:
        try:
            group = Group.objects.get(name='translators')
        except Group.DoesNotExist:
            group = Group(name='translators')
            group.save()

        user.groups.add(group)


class RosettaAppConfig(AppConfig):
    name = 'rosetta'

    def ready(self):
        from django.contrib import admin
        from django.contrib.auth.models import User

        if rosetta_settings.SHOW_AT_ADMIN_PANEL:
            admin.site.index_template = 'rosetta/admin_index.html'

        post_save.connect(add_to_translators, sender=User)
