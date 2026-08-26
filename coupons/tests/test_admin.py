from django.contrib.admin.sites import AdminSite
from django.template.loader import get_template
from django.test import RequestFactory, TestCase
from django.urls import reverse

from coupons.admin import CampaignAdmin, CouponAdmin
from coupons.models import Campaign, Coupon


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

    def test_coupon_change_list_links_to_coupon_generation(self):
        template = get_template("admin/coupons/coupon/change_list.html")

        self.assertIn("Generate coupons", template.template.source)

    def test_campaign_unused_count(self):
        campaign = Campaign.objects.create(name="Launch")
        Coupon.objects.create_coupon("monetary", 100, campaign=campaign)
        campaign_admin = CampaignAdmin(Campaign, self.site)

        self.assertEqual(campaign_admin.num_coupons_unused(campaign), 1)
