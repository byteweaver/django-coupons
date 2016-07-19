#django-coupons

![build status](https://travis-ci.org/byteweaver/django-coupons.png)

A reuseable Django application for coupon gereration and handling

## Setup instructions

1. Install `django-coupons` via pip:
   ```
   $ pip install django-coupons
   ```

2. Add `'coupons'` to `INSTALLED_APPS` in `settings.py`.

3. Migrate database:

   ```
   $ python manage.py migrate
   ```

## Supported use cases of coupons

This application supports different kind of coupons in the way how they can be redeemed.
The difference is defined by the number of possible redeems and if they are bound to a specific user (may even be a list of users) or not.

    1) single time (default), coupon can be used one time without being bound to an user.
    2) user limited, coupon can be used one time but only by a specific user.
    3) limit number, coupon can be used a limited number of times, by any user once.
    4) users list, coupon can be used by a defined list of users, each once.
    5) unlimited, coupon can be used unlimited times, but only once by the same user.
