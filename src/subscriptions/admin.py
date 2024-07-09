from django.contrib import admin
from .models import Subscription, SubscriptionPrice, UserSubscription

class SubscriptionPriceInline(admin.TabularInline):
    model = SubscriptionPrice
    extra = 0

class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPriceInline]
    list_display = ['name', 'active', 'stripe_id_display']  # Add 'stripe_id_display' if needed

    def stripe_id_display(self, obj):
        return obj.stripe_id if obj.stripe_id else "Not available"
    stripe_id_display.short_description = 'Stripe ID'

    readonly_fields = ['stripe_id']

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)