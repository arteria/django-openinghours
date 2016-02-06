# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

PREMISES_MODEL = getattr(settings, 'OPENINGHOURS_PREMISES_MODEL', 'openinghours.Company')

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
    """
    """
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True)
    logo = models.FileField(_('Logo'), upload_to='logo', null=True, blank=True)
    
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class OpeningHours(models.Model):
    """
    """
    class Meta:
        verbose_name = _('Opening Hours') # plurale tantum
        verbose_name_plural = _('Opening Hours')
        
    company = models.ForeignKey(PREMISES_MODEL, verbose_name=_('Company'))
    weekday = models.IntegerField(_('Weekday'), choices=WEEKDAYS)
    from_hour = models.TimeField(_('Opening'))
    to_hour = models.TimeField(_('Closing'))

    def __str__(self):
        return _("%(premises)s %(weekday)s (%(from_hour)s - %(to_hour)s)") % {
            premises: self.company,
            weekday: self.weekday,
            from_hour: self.from_hour,
            to_hour: self.to_hour
        }
    

@python_2_unicode_compatible
class ClosingRules(models.Model):
    """
    Used to overrule the OpeningHours. This will "close" the store due to 
    public holiday, annual closing or private party, etc.
    """
    class Meta:
        verbose_name = _('Closing Rule')
        verbose_name_plural = _('Closing Rules')
        
    company = models.ForeignKey(PREMISES_MODEL, verbose_name=_('Company'))
    start = models.DateTimeField(_('Start')) 
    end = models.DateTimeField(_('End'))
    reason = models.TextField(_('Reason'), null=True, blank=True)

    def __str__(self):
        return _("%(premises)s is closed from %(start)s to %(end)s due to %(reason)s") % {
            'premises': self.company.name,
            'start': str(self.start),
            'end': str(self.end),
            'reason': self.reason
        }
