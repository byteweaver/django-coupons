import string

from django.conf import settings


COUPON_TYPES = getattr(settings, 'COUPONS_COUPON_TYPES', (
        ('monetary', 'Money based coupon'),
        ('percentage', 'Percentage discount'),
        ('virtual_currency', 'Virtual currency'),
    ))

CODE_LENGTH = getattr(settings, 'COUPNS_CODE_LENGTH', 15)

CODE_CHARS = getattr(settings, 'COUPNS_CODE_CHARS', string.letters+string.digits)

