from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.urls import reverse

from coupons.admin import CouponAdmin
from coupons.models import Coupon


class CouponAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.request = RequestFactory().get("/")

    def test_list_display(self):
        coupon_admin = CouponAdmin(Coupon, self.site)

        self.assertEqual(
            list(coupon_admin.get_fields(self.request)),
            ["value", "code", "type", "user_limit", "valid_until", "campaign"],
        )

    def test_generate_coupons_url_is_registered(self):
        self.assertEqual(reverse("admin:generate_coupons"), "/admin/coupons/coupon/generate-coupons/")
