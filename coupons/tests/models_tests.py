import re

from django.test import TestCase

from coupons.models import Coupon
from coupons.settings import CODE_LENGTH, CODE_CHARS


class CouponTestCase(TestCase):
    def test_generate_code(self):
        self.assertIsNotNone(re.match("^[%s]{%d}" % (CODE_CHARS, CODE_LENGTH,), Coupon.generate_code()))

