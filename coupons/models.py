from datetime import datetime
import random

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import models
from django.utils.timezone import get_default_timezone
from django.utils.translation import ugettext_lazy as _

from settings import COUPON_TYPES, CODE_LENGTH, CODE_CHARS


class CouponManager(models.Manager):
    def create_coupon(self, type, value, user=None):
        coupon = self.create(
                value=value,
                code=Coupon.generate_code(),
                type=type,
                user=user
            )
        try:
            coupon.save()
        except IntegrityError:
            # Try again with other code
            return Coupon.objects.create_coupon(type, value, user)
        else:
            return coupon

    def create_coupons(self, quantity, type, value):
        coupons = []
        for i in xrange(quantity):
            coupons.append(self.create_coupon(type, value))
        return coupons


class Coupon(models.Model):
    value = models.IntegerField(_("Value"), help_text=_("Arbitrary coupon value"))
    code = models.CharField(_("Code"), max_length=30, unique=True, blank=True,
        help_text=_("Leaving this field empty will generate a random code."))
    type = models.CharField(_("Type"), max_length=20, choices=COUPON_TYPES)
    user = models.ForeignKey(User, verbose_name=_("User"), null=True, blank=True,
        help_text=_("You may specify a user youn with to limit this coupon to"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    redeemed_at = models.DateTimeField(_("Redeemed at"), blank=True, null=True)

    objects = CouponManager()

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __unicode__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = Coupon.generate_code()
        super(Coupon, self).save(*args, **kwargs)

    @classmethod
    def generate_code(cls):
        return "".join(random.choice(CODE_CHARS) for i in xrange(CODE_LENGTH))

    def redeem(self, user=None):
        self.redeemed_at = datetime.now(get_default_timezone())
        self.user = user
        self.save()

