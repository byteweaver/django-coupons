# django-coupons

[![CI](https://github.com/byteweaver/django-coupons/actions/workflows/ci.yml/badge.svg)](https://github.com/byteweaver/django-coupons/actions/workflows/ci.yml)

A reusable Django application for coupon generation and redemption.

## Requirements

- Python 3.12+
- Django 5.2 through 6.1

## Installation

```console
python -m pip install django-coupons
```

Add `"coupons"` to `INSTALLED_APPS`, then apply its migrations:

```console
python manage.py migrate
```

## Coupon use cases

Coupons can be configured for these redemption patterns:

1. Single-use: one redemption without requiring a user.
2. User-limited: one redemption by a specific user.
3. Limited-use: a fixed number of redemptions, once per user.
4. User list: one redemption by each specified user.
5. Unlimited: unlimited redemptions overall, but only once per user.

Coupon types default to monetary, percentage, and virtual currency. Override `COUPONS_COUPON_TYPES` to provide application-specific choices. Code length, characters, segmentation, and separators can also be configured with the `COUPONS_*` settings in `coupons/settings.py`.

## Development

Install [uv](https://docs.astral.sh/uv/), then create the locked development environment and run all local checks:

```console
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run coverage run -m django test --settings=coupons.tests.settings
uv run coverage report
uv run django-admin check --settings=coupons.tests.settings
uv run django-admin makemigrations --check --dry-run --settings=coupons.tests.settings
uv build
```

CI additionally tests Django 5.2, 6.0, and 6.1 across Python 3.12–3.14.
