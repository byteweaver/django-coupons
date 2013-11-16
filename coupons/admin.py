from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from forms import CouponGenerationForm
from models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'code', 'type', 'value', 'user', 'redeemed_at']
    list_filter = ['type', 'created_at', 'redeemed_at']
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'user__email', 'code', 'value')

    def get_urls(self):
        urls = super(CouponAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'generate-coupons', self.admin_site.admin_view(GenerateCouponsAdminView.as_view()), name='generate_coupons'),
        )
        return my_urls + urls


class GenerateCouponsAdminView(TemplateView):
    template_name = 'admin/generate_coupons.html'

    def get_context_data(self, **kwargs):
        context = super(GenerateCouponsAdminView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            form = CouponGenerationForm(self.request.POST)
            if form.is_valid():
                context['coupons'] = Coupon.objects.create_coupons(
                    form.cleaned_data['quantity'],
                    form.cleaned_data['type'],
                    form.cleaned_data['value']
                )
                messages.success(self.request, _("Your coupons have been generated."))
        else:
            form = CouponGenerationForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


admin.site.register(Coupon, CouponAdmin)
