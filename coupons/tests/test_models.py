import re
from datetime import timedelta
from unittest.mock import patch

from django.utils import timezone
from django.test import TestCase

from coupons.models import Coupon, Campaign
from coupons.settings import (
    CODE_LENGTH,
    CODE_CHARS,
    SEGMENT_LENGTH,
    SEGMENT_SEPARATOR,
)


class CouponTestCase(TestCase):
    def test_generate_code(self):
        self.assertIsNotNone(re.match("^[%s]{%d}" % (CODE_CHARS, CODE_LENGTH,), Coupon.generate_code()))

    def test_generate_code_segmented(self):
        num_segments = CODE_LENGTH // SEGMENT_LENGTH  # full ones
        num_rest = CODE_LENGTH - num_segments * SEGMENT_LENGTH
        self.assertIsNotNone(
            re.match(
                "^([{chars}]{{{sl}}}{sep}){{{ns}}}[{chars}]{{{nr}}}$".format(
                    chars=CODE_CHARS,
                    sep=SEGMENT_SEPARATOR,
                    sl=SEGMENT_LENGTH,
                    ns=num_segments,
                    nr=num_rest),
                Coupon.generate_code("", True)
            )
        )

    def test_save(self):
        coupon = Coupon(type='monetary', value=100)
        coupon.save()
        self.assertTrue(coupon.pk)

    def test_create_coupon(self):
        coupon = Coupon.objects.create_coupon("monetary", 100)
        self.assertTrue(coupon.pk)
        self.assertIsNone(coupon.redeemed_at)

    def test_create_coupon_retries_code_collisions(self):
        Coupon.objects.create(code="duplicate", type="monetary", value=100)
        with patch.object(Coupon, "generate_code", side_effect=["duplicate", "unique"]):
            coupon = Coupon.objects.create_coupon("monetary", 100)

        self.assertEqual(coupon.code, "unique")

    def test_create_coupon_accepts_multiple_user_iterables(self):
        from django.contrib.auth import get_user_model

        users = tuple(get_user_model().objects.create(username=f"user-{index}") for index in range(2))
        coupon = Coupon.objects.create_coupon("monetary", 100, users=users)

        self.assertEqual(coupon.users.count(), 2)

    def test_create_coupons(self):
        coupons = Coupon.objects.create_coupons(50, 'monetary', 100)
        for coupon in coupons:
            self.assertTrue(coupon.pk)

    def test_redeem(self):
        coupon = Coupon.objects.create_coupon('monetary', 100)
        coupon.redeem()
        self.assertIsNotNone(coupon.redeemed_at)

    def test_expired(self):
        coupon = Coupon.objects.create_coupon('monetary', 100)
        self.assertFalse(coupon.expired())
        self.assertEqual(Coupon.objects.expired().count(), 0)
        coupon.valid_until = timezone.now() - timedelta(1)
        coupon.save()
        self.assertTrue(coupon.expired())
        self.assertEqual(Coupon.objects.expired().count(), 1)

    def test_str(self):
        coupon = Coupon.objects.create_coupon('monetary', 100)
        self.assertEqual(coupon.code, str(coupon))

    def test_prefix(self):
        coupon = Coupon.objects.create_coupon('monetary', 100, None, None, "prefix-")
        self.assertTrue(coupon.code.startswith("prefix-"))

    def test_used_unused(self):
        coupon = Coupon.objects.create_coupon('monetary', 100)
        self.assertEqual(Coupon.objects.used().count(), 0)
        self.assertEqual(Coupon.objects.unused().count(), 1)
        coupon.redeem()
        coupon.save()
        self.assertEqual(Coupon.objects.used().count(), 1)
        self.assertEqual(Coupon.objects.unused().count(), 0)


class CampaignTestCase(TestCase):
    def test_str(self):
        campaign = Campaign(name="test")
        campaign.save()
        self.assertEqual("test", str(campaign))
