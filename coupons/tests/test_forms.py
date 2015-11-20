from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase

from coupons.forms import CouponGenerationForm, CouponForm
from coupons.models import Coupon, CouponUser


class CouponGenerationFormTestCase(TestCase):
    def test_form(self):
        form_data = {'quantity': 23, 'value': 42, 'type': 'monetary'}
        form = CouponGenerationForm(data=form_data)
        self.assertTrue(form.is_valid())


class CouponFormTestCase(TestCase):
    def setUp(self):
        self.user = User(username="user1")
        self.user.save()
        self.coupon = Coupon.objects.create_coupon('monetary', 100, self.user)

    def test_wrong_code(self):
        form_data = {'code': 'foo'}
        form = CouponForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_right_code(self):
        form_data = {'code': self.coupon.code}
        form = CouponForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_types(self):
        form_data = {'code': self.coupon.code}
        form = CouponForm(data=form_data, user=self.user, types=('percentage',))
        self.assertFalse(form.is_valid())

    def test_user(self):
        other_user = User(username="user2")
        other_user.save()
        form_data = {'code': self.coupon.code}
        form = CouponForm(data=form_data, user=other_user)
        self.assertFalse(form.is_valid())

    def test_reuse(self):
        self.coupon.redeem()
        self.coupon.save()

        form_data = {'code': self.coupon.code}
        form = CouponForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_expired(self):
        self.coupon.valid_until = timezone.now() - timedelta(1)
        self.coupon.save()
        form_data = {'code': self.coupon.code}
        form = CouponForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())


class UnboundCouponFormTestCase(TestCase):
    def setUp(self):
        self.user = User(username="user1")
        self.user.save()
        self.coupon = Coupon.objects.create_coupon('monetary', 100)

    def test_none_coupon_user(self):
        CouponUser.objects.create(coupon=self.coupon)
        self.assertTrue(self.coupon.users.count(), 1)
        self.assertIsNone(self.coupon.users.first().user)
        self.assertIsNone(self.coupon.users.first().redeemed_at)

        form_data = {'code': self.coupon.code}
        form = CouponForm(data=form_data, user=self.user)

        self.assertTrue(form.is_valid())
