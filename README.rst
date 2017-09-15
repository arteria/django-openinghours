Django Opening Hours
====================

.. image:: https://travis-ci.org/arteria/django-openinghours.svg?branch=master
    :target: https://travis-ci.org/arteria/django-openinghours
.. image:: https://coveralls.io/repos/github/arteria/django-openinghours/badge.svg?branch=master
    :target: https://coveralls.io/github/arteria/django-openinghours?branch=master
.. image:: https://img.shields.io/pypi/v/django-openinghours.svg
    :target: https://pypi.python.org/pypi/django-openinghours

A reusable Django app to work with opening hours.

Comes with the following features:

-  Multiple company (premises) support, customisable to directly plug in
   your own model.
-  Able to show if a company is currently open (“Come in, we’re open!”,
   “Sorry, we’re closed.”).
-  Able to list the opening hours, e.g. Monday 9am to 5pm, etc. for
   multiple company premises.
-  Possible to define opening hours passing midnight.
-  Possible to define closing hours, e.g. for holiday.

Installation
------------

To get the latest stable release from PyPi

::

    pip install django-openinghours

To get the latest version from GitHub

::

    pip install -e git+git://github.com/arteria/django-openinghours.git#egg=openinghours-master

Add ``openinghours`` to your ``INSTALLED_APPS``

::

    INSTALLED_APPS = (
        ...,
        'openinghours',
    )

You can use the company model provided or plug your own using
settings.py:

::

    OPENINGHOURS_PREMISES_MODEL = 'yourcastleapp.Castle'

Add the ``openinghours`` URLs to your ``urls.py``

::

    urlpatterns = [
        ...
        url(r'^openinghours/', include('openinghours.urls')),
    ]

Before your tags/filters are available in your templates, load them
using

::

    {% load openinghours_tags %}

Create your tables

::

    ./manage.py migrate openinghours

Set ``'TIME_ZONE'`` in your project settings.

Usage
-----

Set up a company
~~~~~~~~~~~~~~~~

This app supports multiple companies (or your custom model) with
multiple opening and closing hours.

Set up opening hours
~~~~~~~~~~~~~~~~~~~~

Used to describe when premises are open, defined on a daily basis (per
day) by defining one or more start and end times of opening slots.

Optionally, set up the closing hour rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is used to define when premises are closed (e.g. due to a holiday,
absences, sickness or similar). Please note that the closing hours
override the opening hours.

You can find examples of how to use this app in our `templates`_.

Remarks
-------

Opening hours is built using datetime’s isoweekday. This means Monday is
represented by number 1 and Sunday by 7.

Planned features
----------------

Priority 1 = high/must have, 2 = and 3 = low/nice to have

- **1** Migrate to Django’s timezone
- **2** Docs for live testing of defined rules
- **3** Shortcut for everyday (1-7) = 0 in WEEKDAYS, or 8 = monday to
  friday, etc.
- **3** Global closing hours to override all companies. Use cases: close
  a whole shopping centre

See also `CHANGELOG`_ and `UPGRADING`_ docs.

Contribute
----------

Just send us your pull request. File and issue. Use it. Talk about
`it`_.

.. _templates: openinghours/templates/openinghours/index.html
.. _CHANGELOG: CHANGELOG.txt
.. _UPGRADING: docs/UPGRADING.rst
.. _it: https://github.com/arteria/django-openinghours



django-openinghours is free software. If you find it useful and would like to give back, please consider to make a donation using Bitcoin https://blockchain.info/payment_request?address=1AJkbQdcNkrHzxi91mB1kkPxh4t4BJ4hu4 or  PayPal https://www.paypal.me/arteriagmbh. Thank you!
