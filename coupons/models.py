import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from settings import COUPON_TYPES, CODE_LENGTH, CODE_CHARS


class Coupon(models.Model):
    value = models.IntegerField(_("Value"), help_text=_("Arbitrary coupon value"))
    code = models.CharField(_("Code"), max_length=30, unique=True)
    type = models.CharField(_("Type"), max_length=20, choices=COUPON_TYPES)
    user = models.ForeignKey(User, verbose_name=_("User"), null=True, blank=True,
        help_text=_("You may specify a user youn with to limit this coupon to"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    redeemed_at = models.DateTimeField(_("Created at"), blank=True, null=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __unicode__(self):
        return self.code

    @classmethod
    def generate_code(cls):
        return "".join(random.choice(CODE_CHARS) for i in xrange(CODE_LENGTH))

