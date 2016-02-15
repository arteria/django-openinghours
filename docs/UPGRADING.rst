See README and CHANGELOG.txt in the root folder.

Upgrading
=========
To upgrade from version prior to 0.1, please rename your template tag names and
make sure to pass the company or premisses object to the tag instead of a slug.

- ``companyOpeningHoursList`` = ``opening_hours``
- ``isCompanyCurrentlyOpen`` = ``is_open``
- ``isoDayToWeekday`` = ``iso_day_to_weekday``
- ``toWeekday`` = ``to_weekday``
- ``getCompanyNextOpeningHour`` = ``next_time_open``
- ``hasCompanyClosingRuleForNow`` = ``has_closing_rule_for_now``
- ``getCompanyClosingRuleForNow`` = ``get_closing_rule_for_now``

That way ``{% companyOpeningHoursList 'company-ltd' %}``
becomes ``{% opening_hours location %}``
and ``{% isCompanyCurrentlyOpen 'company-ltd' as open %}``
becomes ``{% is_open location as open %}``.
