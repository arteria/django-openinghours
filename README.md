This Django app is in α state! Don't use it yet ...



#Django Opening Hours


A reusable Django app to work with opening hours. Currently the main two use cases are: 

* to visualise if a company is currently open or not
* to list the opening hours, eg. MON 9h00 to 17h00, etc.


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

## TODO
* Shortcut for everyday (1-7) = 0 in WEEKDAYS, or 8 = monday to friday, etc.
* Global closing hours to overrule all companies. Use cases: close a complete shopping center
* Implement closing hours, currently you can define them but, .. WIP

## Contribute


Just send us your pull request. 
=======
    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch


 
