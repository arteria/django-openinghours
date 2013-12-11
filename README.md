#Django Opening Hours


A reusable Django app to work with opening hours that comes with the following features:

* Multiple company support.
* Able to visualise if a company is currently open or not ("Yes, we're open!", "Sorry, we're closed.").
* Able to list the opening hours, eg. MON 9h00 to 17h00, etc. for one or more companies.
* Posible to define opening hours that pass midnight.
* Posible to define closing hours, eg. for holiday. 



##Installation

To get the latest stable release from PyPi


    pip install django-openinghours

To get the latest commit from GitHub


    pip install -e git+git://github.com/arteria.ch/django-openinghours.git#egg=openinghours-master

TODO: Describe further installation steps (edit / remove the examples below):

Add ``openinghours`` to your ``INSTALLED_APPS``


    INSTALLED_APPS = (
        ...,
        'openinghours',
    )

Add the ``openinghours`` URLs to your ``urls.py``


    urlpatterns = patterns('',
        ...
        url(r'^openinghours/', include('openinghours.urls')),
    )

Before your tags/filters are available in your templates, load them by using


	{% load openinghours_tags %}


Don't forget to create your tables


    ./manage.py syncdb openinghours



Don't forget to set ``'TIME_ZONE'`` in your project settings.


## Usage


### Setup a company
This app supports multiple companies with multiple opening and closing hours. 

### Setting up opening hours
This is used to describe when sth. (eg. the shop) is open. This is done on a daily base (per day) by defining one or more 
start and end times of opening slots.

### Optionally, setting up the closing hour rules

This is used to describe/define when sth. (eg. the shop) is closed (eg. due holiday, 
absences, sickness or whatever). Note that the closing hours overrules the opening hours!



In the index.html (https://github.com/arteria/django-openinghours/blob/master/openinghours/templates/openinghours/index.html) you will find a lot of examples how to use this app.

## Remarks 

* Opening hours is build using datetime's isoweekday. This means Monday is represented by 1 and Sunday by 7.


## History and Change Log

### Latest/Development Version

Please check the latest commits for development version.

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

* (3) Shortcut for everyday (1-7) = 0 in WEEKDAYS, or 8 = monday to friday, etc.
* (3) Global closing hours to overrule all companies. Use cases: close a complete shopping center

## Contribute

Just send us your pull request. Thanks. :)
 
 
