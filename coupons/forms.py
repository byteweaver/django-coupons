from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Coupon, CouponUser, Campaign
from .settings import COUPON_TYPES


class CouponGenerationForm(forms.Form):
    quantity = forms.IntegerField(label=_("Quantity"))
    value = forms.IntegerField(label=_("Value"))
    type = forms.ChoiceField(label=_("Type"), choices=COUPON_TYPES)
    valid_until = forms.SplitDateTimeField(
        label=_("Valid until"), required=False,
        help_text=_("Leave empty for coupons that never expire")
    )
    prefix = forms.CharField(label="Prefix", required=False)
    campaign = forms.ModelChoiceField(
        label=_("Campaign"), queryset=Campaign.objects.all(), required=False
    )


class CouponForm(forms.Form):
    code = forms.CharField(label=_("Coupon code"))

    def __init__(self, *args, **kwargs):
        self.user = None
        self.types = None
        if 'user' in kwargs:
            self.user = kwargs['user']
            del kwargs['user']
        if 'types' in kwargs:
            self.types = kwargs['types']
            del kwargs['types']
        super(CouponForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            raise forms.ValidationError(_("This code is not valid."))
        self.coupon = coupon

        if coupon.is_redeemed:
            raise forms.ValidationError(_("This code has already been used."))

        try:  # check if there is a user bound coupon existing
            user_coupon = coupon.users.get(user=self.user)
            if user_coupon.redeemed_at is not None:
                raise forms.ValidationError(_("This code has already been used by your account."))
        except CouponUser.DoesNotExist:
            if coupon.user_limit is not 0:  # zero means no limit of user count
                if coupon.user_limit is coupon.users.count():  # only user bound coupons left and you don't have one
                    raise forms.ValidationError(_("This code is not valid for your account."))
                if coupon.user_limit is coupon.users.filter(redeemed_at__isnull=True).count():  # all coupons redeemed
                    raise forms.ValidationError(_("This code has already been used."))
        if self.types is not None and coupon.type not in self.types:
            raise forms.ValidationError(_("This code is not meant to be used here."))
        if coupon.expired():
            raise forms.ValidationError(_("This code is expired."))
        return code
