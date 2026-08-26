import random

from django.conf import settings
from django.db import IntegrityError, models, transaction
from django.dispatch import Signal
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .settings import (
    CODE_CHARS,
    CODE_LENGTH,
    SEGMENT_LENGTH,
    SEGMENT_SEPARATOR,
    SEGMENTED_CODES,
)

user_model = settings.AUTH_USER_MODEL
redeem_done = Signal()


class CouponManager(models.Manager):
    def create_coupon(self, type, value, users=None, valid_until=None, prefix="", campaign=None, user_limit=None):
        values = {
            "value": value,
            "type": type,
            "valid_until": valid_until,
            "campaign": campaign,
        }
        if user_limit is not None:
            values["user_limit"] = user_limit

        for _attempt in range(10):
            try:
                with transaction.atomic():
                    coupon = self.create(code=Coupon.generate_code(prefix), **values)
                break
            except IntegrityError:
                continue
        else:
            raise RuntimeError("Could not generate a unique coupon code after 10 attempts")

        if users is None:
            users = []
        elif not isinstance(users, (list, tuple, set)):
            users = [users]
        for user in users:
            if user:
                CouponUser(user=user, coupon=coupon).save()
        return coupon

    def create_coupons(self, quantity, type, value, valid_until=None, prefix="", campaign=None):
        coupons = []
        for _index in range(quantity):
            coupons.append(self.create_coupon(type, value, None, valid_until, prefix, campaign))
        return coupons

    def used(self):
        return self.exclude(users__redeemed_at__isnull=True)

    def unused(self):
        return self.filter(users__redeemed_at__isnull=True)

    def expired(self):
        return self.filter(valid_until__lt=timezone.now())


class Coupon(models.Model):
    value = models.IntegerField(_("Value"), help_text=_("Arbitrary coupon value"))
    code = models.CharField(
        _("Code"),
        max_length=30,
        unique=True,
        blank=True,
        help_text=_("Leaving this field empty will generate a random code."),
    )
    type = models.CharField(_("Type"), max_length=20)
    user_limit = models.PositiveIntegerField(_("User limit"), default=1)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    valid_until = models.DateTimeField(
        _("Valid until"), blank=True, null=True, help_text=_("Leave empty for coupons that never expire")
    )
    campaign = models.ForeignKey(
        "Campaign",
        verbose_name=_("Campaign"),
        blank=True,
        null=True,
        related_name="coupons",
        on_delete=models.SET_NULL,
    )

    objects = CouponManager()

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = Coupon.generate_code()
        super().save(*args, **kwargs)

    def expired(self):
        return self.valid_until is not None and self.valid_until < timezone.now()

    @property
    def is_redeemed(self):
        """Returns true is a coupon is redeemed (completely for all users) otherwise returns false."""
        return self.users.filter(redeemed_at__isnull=False).count() >= self.user_limit and self.user_limit != 0

    @property
    def redeemed_at(self):
        redemption = self.users.filter(redeemed_at__isnull=False).order_by("redeemed_at").last()
        return redemption.redeemed_at if redemption else None

    @classmethod
    def generate_code(cls, prefix="", segmented=SEGMENTED_CODES):
        code = "".join(random.choice(CODE_CHARS) for i in range(CODE_LENGTH))
        if segmented:
            code = SEGMENT_SEPARATOR.join([code[i : i + SEGMENT_LENGTH] for i in range(0, len(code), SEGMENT_LENGTH)])
            return prefix + code
        else:
            return prefix + code

    def redeem(self, user=None):
        try:
            coupon_user = self.users.get(user=user)
        except CouponUser.DoesNotExist:
            try:  # silently fix unbouned or nulled coupon users
                coupon_user = self.users.get(user__isnull=True)
                coupon_user.user = user
            except CouponUser.DoesNotExist:
                coupon_user = CouponUser(coupon=self, user=user)
        coupon_user.redeemed_at = timezone.now()
        coupon_user.save()
        redeem_done.send(sender=self.__class__, coupon=self)


class Campaign(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")

    def __str__(self):
        return self.name


class CouponUser(models.Model):
    coupon = models.ForeignKey(Coupon, related_name="users", on_delete=models.CASCADE)
    user = models.ForeignKey(user_model, verbose_name=_("User"), null=True, blank=True, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(_("Redeemed at"), blank=True, null=True)

    class Meta:
        unique_together = (("coupon", "user"),)

    def __str__(self):
        return str(self.user)
