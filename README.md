#Django Opening Hours


A reusable Django app to work with opening hours. Currently the main two use cases are: 

* to visualise if a company is currently open or not
* to list the opening hours, eg. MON 9h00 to 17h00, etc.


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
This app supports multiple company with multiple opening and closing hours. 

### Setting up opening hours
This is used to describe when sth. (eg. the shop) is open. This is done on a daily base (per day) by defining one or more 
start and end times of opening slots.

### Optionally, setting up the closing hour rules NOT IMPLEMENTED YET!

This is used to describe/define when sth. (eg. the shop) is closed (eg. due holiday, 
absences, sickness or whatever). Note that the closing hours overrules the opening hours!



In the index.html (https://github.com/arteria/django-openinghours/blob/master/openinghours/templates/openinghours/index.html) you will find a lot of examples how to use this app.

## TODOs and planned Features
Priority 1 = high/must have, 2 =  and 3 = low/nice to have

* (1) Implement closing hours, currently you can define them but, .. WIP
* (1) "Next time opened" function returning when (eg.) shop is open for the next time
* (2) Handle midnight, allow hours like MON 21h00 to 01h00, used for Clubs, etc.
* (3) Shortcut for everyday (1-7) = 0 in WEEKDAYS, or 8 = monday to friday, etc.
* (3) Global closing hours to overrule all companies. Use cases: close a complete shopping center

## Contribute

Just send us your pull request. Thanks. :)
 
 
