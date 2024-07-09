from typing import Any
from django.core.management.base import BaseCommand
from subscriptions.models import Subscription

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        # print("hhh")
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            sub_perms = obj.Permissions.all()
            # print(obj.groups.all())
            for group in obj.groups.all():
                group.permissions.set(sub_perms)
                # for perm in obj.Permissions.all():
                #     group.permissions.add(perm)
                
            # print(obj.Permissions.all())