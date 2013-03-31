from django.conf import settings


COUPON_TYPES = getattr(settings, 'COUPNS_COUPON_TYPES', (
        ('monetary', 'Money based coupon'),
        ('percentage', 'Percentage discount'),
        ('virtual_currency', 'Virtual currency'),
    ))

