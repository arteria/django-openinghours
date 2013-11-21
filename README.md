This Django app is in α state! Don't use it yet ...



#Django Opening Hours


A reusable Django app to work with opening hours.

##Installation

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-openinghours

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/arteria.ch/django-openinghours.git#egg=openinghours

TODO: Describe further installation steps (edit / remove the examples below):

Add ``openinghours`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'openinghours',
    )

Add the ``openinghours`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^openinghours/', include('openinghours.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load openinghours_tags %}


Don't forget to create your tables

.. code-block:: bash

    ./manage.py syncdb openinghours


Don't forget to set 'TIME_ZONE' in your project settings.


## Usage

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.
### Setup a company
This app supports multiple company with multiple opening and closing hours. 

### Setting up opening hours
This is used to describe when sth. (eg. the shop) is open. This is done on a daily base (per day) by defining one or more 
start and end times of opening slots.

### Setting up closing rules
This is used to describe when sth. (eg. the shop) is closed (eg. due holiday, 
absences, sickness or whatever). Note that the closing hours overrules the opening hours!


## TODO
* Template support for template tags, remove ugly string concating stuff
* Shortcut for everyday (1-7) = 0 in WEEKDAYS, or 8 = monday to friday, etc.
* Global closing hours to overrule all companies. Use cases: close a complete shopping center

## Contribute

Just send us your pull request. 