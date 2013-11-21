from django.db import models
from django.utils.translation import ugettext_lazy as _

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


class Company(models.Model):
    '''
    '''
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.FileField(upload_to='logo', null=True, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.slug)


class OpeningHours(models.Model):
    '''
    '''
    company = models.ForeignKey(Company)
    weekday = models.IntegerField(choices=WEEKDAYS)
    fromHour = models.TimeField()
    toHour = models.TimeField()

    def __unicode__(self):
        return "%s %s (%s - %s)" % (self.company, self.weekday, self.fromHour, self.toHour)
    

class ClosingRules(models.Model):
    '''
    Used to overrule the OpeningHours. This will "close" the store due to 
    public holiday, annual closing or private party, etc.
    '''
    company = models.ForeignKey(Company)
    start = models.DateTimeField() 
    end = models.DateTimeField()
    reason = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s is closed from %s to %s due to %s" % (self.company.anme, str(self.start), str(self.end), self.reason)