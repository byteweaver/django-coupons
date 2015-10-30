from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from coupons.admin import CouponAdmin
from coupons.models import Coupon


class MockRequest(object):
    pass


request = MockRequest()


class CouponAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_list_display(self):
        admin = CouponAdmin(Coupon, self.site)

        self.assertEquals(
            list(admin.get_fields(request)),
            ['value', 'code', 'type', 'user', 'redeemed_at', 'valid_until', 'campaign']
        )
