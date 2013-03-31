from django.contrib import admin

from models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'code', 'type', 'value', 'user', 'redeemed_at',]
    list_filter = ['type', 'created_at', 'redeemed_at',]
    raw_id_fields = ('user',)

admin.site.register(Coupon, CouponAdmin)

