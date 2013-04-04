from django.test import TestCase

from coupons.forms import CouponGenerationForm


class CouponGenerationFormTestCase(TestCase):
    def test_form(self):
        form_data = {'quantity': 23, 'value': 42, 'type': 'monetary'}
        form = CouponGenerationForm(data=form_data)
        self.assertTrue(form.is_valid())

