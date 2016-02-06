#Django Opening Hours


A reusable Django app to work with opening hours.

Comes with the following features:

* Multiple company (premises) support, customisable to directly plug in your own model.
* Able to show if a company is currently open ("Come in, we're open!", "Sorry, we're closed.").
* Able to list the opening hours, e.g. Monday 9am to 5pm, etc. for multiple company premises.
* Possible to define opening hours passing midnight.
* Possible to define closing hours, e.g. for holiday. 



##Installation

To get the latest stable release from PyPi


    pip install django-openinghours

To get the latest version from GitHub


    pip install -e git+git://github.com/arteria.ch/django-openinghours.git#egg=openinghours-master

Add ``openinghours`` to your ``INSTALLED_APPS``


    INSTALLED_APPS = (
        ...,
        'openinghours',
    )

You can use the company model provided or plug your own using settings.py:

    OPENINGHOURS_PREMISES_MODEL = 'yourcastleapp.models.Castle'

Add the ``openinghours`` URLs to your ``urls.py``


    urlpatterns = [
        ...
        url(r'^openinghours/', include('openinghours.urls')),
    ]

Before your tags/filters are available in your templates, load them using


	{% load openinghours_tags %}


Create your tables


    ./manage.py migrate openinghours



Set ``'TIME_ZONE'`` in your project settings.


## Usage


### Set up a company
This app supports multiple companies (or your custom model) with multiple opening and closing hours. 

### Set up opening hours
Used to describe when premises are open, defined on a daily basis (per day) by defining one or more 
start and end times of opening slots.

### Optionally, set up the closing hour rules

This is used to define when premises are closed (e.g. due to a holiday, 
absences, sickness or similar). Please note that the closing hours override the opening hours.



In the [index.html](https://github.com/arteria/django-openinghours/blob/master/openinghours/templates/openinghours/index.html) you will find a lot of examples of how to use this app.

## Remarks 

Opening hours is built using datetime's isoweekday. This means Monday is represented by number 1 and Sunday by 7.


## History and Change Log

### Latest/Development Version

Please check the latest commits for development version.

### 0.0.27

* Adding [django-threadlocals](https://pypi.python.org/pypi/django-threadlocals/0.8) allows for live testing of the rules defined.
* Bugfix if closed on Sunday and open later during the day. Next opening showed Monday.

### 0.0.8 .. 0.0.26 
* Added template tag ``isoDayToWeekday``, returns 'today' in case of today.
+ Added template tag ``toWeekday`` to handle next weeks 'today'.
* Partial closing/opening hours with overlapping support
* Added template tag ``getCompanyClosingRuleForNow``.
* Bugfix

### 0.0.7
* Bugfix

### 0.0.6
* Added attribut access in template tags.

### 0.0.5
* Returning the OpeningHours when company is open (instead of True).

### 0.0.4
* Added some template tags: ``getCompanyNextOpeningHour`` and  ``hasCompanyClosingRuleForNow``.

### 0.0.3 
* "Next time opened" function returning when (eg.) shop is open for the next time

### 0.0.2
* Handle midnight, allow hours like MON 21h00 to 01h00. Eg. used for Night Clubs, etc.
* Implemented closing hours.

### 0.0.1
* Inital version


## TODOs and planned Features
Priority 1 = high/must have, 2 =  and 3 = low/nice to have

* (1) Migrate to Django's timezone
* (1) Add tests
* (2) Docus for live testing of defined rules
* (3) Shortcut for everyday (1-7) = 0 in WEEKDAYS, or 8 = monday to friday, etc.
* (3) Global closing hours to override all companies. Use cases: close a whole shopping centre

## Contribute

Just send us your pull request. File and issue. Use it. Talk about [it](https://github.com/arteria/django-openinghours). Thank you
 
 
