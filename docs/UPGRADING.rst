See `README`_ and `CHANGELOG`_.

Upgrading
=========
To upgrade from version prior to 0.1, please rename your template tag names and
make sure to pass the company or premises object to the tag instead of a slug.

===============================  ============================
<= 0.0.27                        > 0.1
-------------------------------  ----------------------------

``companyOpeningHoursList``      ``opening_hours``
``isCompanyCurrentlyOpen``       ``is_open``
``isoDayToWeekday``              ``iso_day_to_weekday``
``toWeekday``                    ``to_weekday``
``getCompanyNextOpeningHour``    ``next_time_open``
``hasCompanyClosingRuleForNow``  ``has_closing_rule_for_now``
``getCompanyClosingRuleForNow``  ``get_closing_rule_for_now``
===============================  ============================

| ``{% companyOpeningHoursList 'company-ltd' %}`` becomes
| ``{% opening_hours location %}``
| 
| ``{% isCompanyCurrentlyOpen 'company-ltd' as open %}`` becomes
| ``{% is_open location as open %}``

.. _README: ../README.rst
.. _CHANGELOG: ../CHANGELOG.txt