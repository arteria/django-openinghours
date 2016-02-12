# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


# isoweekday
WEEKDAYS = [
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
]


@python_2_unicode_compatible
class Company(models.Model):
    '''
    '''
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.FileField(upload_to='logo', null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.slug)


@python_2_unicode_compatible
class OpeningHours(models.Model):
    '''
    '''
    class Meta:
        verbose_name = 'Opening Hour'
        verbose_name_plural = 'Opening Hours'
        ordering = ['company', 'weekday', 'from_hour']

    company = models.ForeignKey(Company)
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return "%s %s (%s - %s)" % (self.company, self.weekday, self.from_hour, self.to_hour)


@python_2_unicode_compatible
class ClosingRules(models.Model):
    '''
    Used to overrule the OpeningHours. This will "close" the store due to
    public holiday, annual closing or private party, etc.
    '''
    class Meta:
        verbose_name = 'Closing Rule'
        verbose_name_plural = 'Closing Rules'

    company = models.ForeignKey(Company)
    start = models.DateTimeField()
    end = models.DateTimeField()
    reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s is closed from %s to %s due to %s" % (self.company.name, str(self.start), str(self.end), self.reason)
