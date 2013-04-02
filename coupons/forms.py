from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Coupon
from settings import COUPON_TYPES


class CouponGenerationForm(forms.Form):
    quantity = forms.IntegerField(label=_("Quantity"))
    value = forms.IntegerField(label=_("Value"))
    type = forms.ChoiceField(label=_("Type"), choices=COUPON_TYPES)


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
        return super(CouponForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code, redeemed_at=None)
        except Coupon.DoesNotExist:
            raise forms.ValidationError(_("This code is not valid."))
        self.coupon = coupon
        if not coupon.user is None and coupon.user != self.user:
            raise forms.ValidationError(_("This code is not valid for your account."))
        if not self.types is None and coupon.type not in self.types:
            raise forms.ValidationError(_("This code is not ment to be used here."))
        return code

