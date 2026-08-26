# Changelog

## 2.0.0a1 - Unreleased

- Require Python 3.12+ and support Django 5.2–6.1.
- Replace setuptools, tox, and Travis CI with uv, `pyproject.toml`, Ruff, coverage, and GitHub Actions.
- Update removed Django APIs and make historical migrations usable by modern Django.
- Fix unused campaign coupon counts and coupon-code collision handling.
- Keep configurable coupon types out of package migrations.
- Add a coupon-generation link to the Django admin.
- Remove obsolete Python 2 and South support.

## V 1.2.0

* Drop support for Django 1.4 and 1.5

## V 1.1.0
 * campaigns
   Coupons may now be associated with campaigns for better tracking
 * segmented coupon codes
   Coupon codes may now be segmented like "xxxx-xxxx-xx"
   New settings (defaults):
    * COUPONS_SEGMENTED_CODES (False)
    * COUPONS_SEGMENT_LENGTH (4)
    * COUPONS_SEGMENT_SEPARATOR ("-")
 * prefixes for coupon codes
   Coupons may now be auto prefixed upon creation
 * expiration date for coupons
   Coupons can now expire, see valid_until field
 * migrations for south and django 1.7+ included
 * django 1.8 now officially supported
 * minor fixes

## V 1.0.4
redeem_done signal

## V 1.0.3
Typo and CouponForm fix.

## V 1.0.2
Fixed Typo in settings.
* COUPNS_CODE_LENGTH -> COUPONS_CODE_LENGTH
* COUPNS_CODE_CHARS -> COUPONS_CODE_CHARS

*Check your settings after updating!*

## V 1.0.1
add django 1.7 migrations and south legacy migrations

## V 1.0.0
Supports:
* django 1.4 - 1.7
* python 2.7, 3.4
