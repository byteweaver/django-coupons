from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from coupons.models import CouponUser


def validate_redeem(coupon, user=None):
    if coupon.is_redeemed:
        raise ValidationError(_("This code has already been used."))

    try:  # check if there is a user bound coupon existing
        user_coupon = coupon.users.get(user=user)
        if user_coupon.redeemed_at is not None:
            raise ValidationError(_("This code has already been used by your account."))
    except CouponUser.DoesNotExist:
        if coupon.user_limit is not 0:  # zero means no limit of user count
            if coupon.user_limit is coupon.users.count():  # only user bound coupons left and you don't have one
                raise ValidationError(_("This code is not valid for your account."))
            if coupon.user_limit is coupon.users.filter(redeemed_at__isnull=True).count():  # all coupons redeemed
                raise ValidationError(_("This code has already been used."))
