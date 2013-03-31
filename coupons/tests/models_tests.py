import re

from django.test import TestCase

from coupons.models import Coupon
from coupons.settings import CODE_LENGTH, CODE_CHARS


class CouponTestCase(TestCase):
    def test_generate_code(self):
        self.assertIsNotNone(re.match("^[%s]{%d}" % (CODE_CHARS, CODE_LENGTH,), Coupon.generate_code()))

    def test_create_coupon(self):
        coupon = Coupon.objects.create_coupon('menetary', 100)
        self.assertTrue(coupon.pk)

    def test_create_coupons(self):
        coupons = Coupon.objects.create_coupons(50, 'menetary', 100)
        for coupon in coupons:
            self.assertTrue(coupon.pk)

