from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
import helpers.billing

User = settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS = True
SUBSCRIPTION_PERMISSIONS = [
    ("advanced", "Advanced Perm"),
    ("pro", "Pro Perm"),
    ("basic", "Basic Perm"),
    ("basic_ai", "Basic AI Perm"),
]

# Create your models here.
class Subscription(models.Model):
    """
    Subscription = Stripe Product
    """
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(
        Permission,
        limit_choices_to={
            "content_type__app_label": "subscriptions",
            "codename__in": [perm[0] for perm in SUBSCRIPTION_PERMISSIONS]
        }
    )
    stripe_id = models.CharField(max_length=120, null=True, blank=True)


    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

    def save(self, *args, **kwargs):      
        
        if not self.stripe_id:
            stripe_id = helpers.billing.create_product(name=self.name, metadata={"subscription_plan_id":self.id}, raw=False)
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubscriptionPrice(models.Model):
    """
    Subscription price  = Stripe Price
    """
    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Yearly"
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)    
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    interval = models.CharField(max_length=120, default=IntervalChoices.MONTHLY, choices=IntervalChoices.choices)

    @property
    def stripe_currency(self):
        return "usd"
    
    @property
    def stripe_price(self):
        return self.price * 100

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id
    
    def save(self, *args, **kwargs):
        if (not self.stripe_id is None and self.product_stripe_id is not None):
                stripe_id = helpers.billing.create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                interval=self.interval,                
                product=self.product_stripe_id,
                metadata={"subscription_price_id":self.id},
                raw=False
            )
        self.stripe_id = stripe_id 

        super().save(*args, **kwargs)

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.subscription.name if self.subscription else "No Subscription"}'
    

def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        group_ids = groups.values_list('id', flat=True)
    user.groups.set(groups)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            sub_qs = Subscription.objects.filter(active=True).exclude(id=subscription_obj.id)
        subs_groups = subs_qs.value_list("groups__id", flat=True)
        subs_groups_set = set(subs_groups)
        # group_ids = groups.values_list('id', flat=True)
        current_groups = user.groups.all().values_list('id', flat=True)
        group_ids_set = set(group_ids)
        current_group_set = set(current_groups) - subs_groups_set       
        final_group_ids = list(group_ids_set | current_group_set) 
        user.groups.set(groups)

post_save.connect(user_sub_post_save, sender=UserSubscription)
    