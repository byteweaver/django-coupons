import random

from django.conf import settings
from django.db import IntegrityError
from django.db import models
from django.dispatch import Signal
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .settings import COUPON_TYPES, CODE_LENGTH, CODE_CHARS


try:
    user_model = settings.AUTH_USER_MODEL
except AttributeError:
    from django.contrib.auth.models import User as user_model
redeem_done = Signal(providing_args=["coupon"])


class CouponManager(models.Manager):
    def create_coupon(self, type, value, user=None, valid_until=None):
        coupon = self.create(
            value=value,
            code=Coupon.generate_code(),
            type=type,
            user=user,
            valid_until=valid_until,
        )
        try:
            coupon.save()
        except IntegrityError:
            # Try again with other code
            return Coupon.objects.create_coupon(type, value, user)
        else:
            return coupon

    def create_coupons(self, quantity, type, value, valid_until=None):
        coupons = []
        for i in range(quantity):
            coupons.append(self.create_coupon(type, value, None, valid_until))
        return coupons


@python_2_unicode_compatible
class Coupon(models.Model):
    value = models.IntegerField(_("Value"), help_text=_("Arbitrary coupon value"))
    code = models.CharField(_("Code"), max_length=30, unique=True, blank=True,
        help_text=_("Leaving this field empty will generate a random code."))
    type = models.CharField(_("Type"), max_length=20, choices=COUPON_TYPES)
    user = models.ForeignKey(user_model, verbose_name=_("User"), null=True, blank=True,
        help_text=_("You may specify a user you want to restrict this coupon to."))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    redeemed_at = models.DateTimeField(_("Redeemed at"), blank=True, null=True)
    valid_until = models.DateTimeField(_("Valid until"), blank=True, null=True,
        help_text=_("Leave empty for coupons that never expire"))

    objects = CouponManager()

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = Coupon.generate_code()
        super(Coupon, self).save(*args, **kwargs)

    def expired(self):
        return self.valid_until is not None and self.valid_until < timezone.now()

    @classmethod
    def generate_code(cls):
        return "".join(random.choice(CODE_CHARS) for i in range(CODE_LENGTH))

    def redeem(self, user=None):
        self.redeemed_at = timezone.now()
        self.user = user
        self.save()
        redeem_done.send(sender=self.__class__, coupon=self)
