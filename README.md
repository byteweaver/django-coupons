#django-coupons

![build status](https://travis-ci.org/byteweaver/django-coupons.png)

A reuseable Django application for coupon gereration and handling


##Contributors
(alphabetical order)

* @akuryou
* @ikresoft
* @noxan
* @TigerDX
* @TimFletcher

##Changelog

###V 1.1.0
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

###V 1.0.4
redeem_done signal

###V 1.0.3
Typo and CouponForm fix.

###V 1.0.2
Fixed Typo in settings.
* COUPNS_CODE_LENGTH -> COUPONS_CODE_LENGTH
* COUPNS_CODE_CHARS -> COUPONS_CODE_CHARS

*Check your settings after updating!*

###V 1.0.1
add django 1.7 migrations and south legacy migrations

###V 1.0.0
Supports:
* django 1.4 - 1.7
* python 2.7, 3.4
