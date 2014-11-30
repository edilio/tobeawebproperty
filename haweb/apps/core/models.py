from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from localflavor.us.models import *


class UserProfile(AbstractUser):
    photo = models.ImageField(upload_to='users', blank=True, null=True)
    title = models.CharField(max_length=250)
    edit_date = models.DateTimeField(default=timezone.now)
    phone = PhoneNumberField(default="")

    def save(self, *args, **kwargs):
        self.edit_date = timezone.now()
        super(UserProfile, self).save(*args, **kwargs)

    @property
    def order_on(self):
        return self.last_name + ', ' + self.first_name


class City(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'Cities'

    def __unicode__(self):
        return self.name


class ZipCode(models.Model):
    zip_code = models.CharField(max_length=10, db_index=True)
    state = USStateField()
    city = models.ForeignKey(City)

    @property
    def city_state_zip(self):
        return "{}, {} {}".format(self.city.name, self.get_state_display(), self.zip_code)

    def __unicode__(self):
        return self.city_state_zip


class Unit(models.Model):
    unit_id = models.CharField(max_length=7, null=True, blank=True, db_index=True)
    address = models.CharField(max_length=100, db_index=True)
    apartment = models.CharField(max_length=7, null=True, blank=True)
    zip_code = models.ForeignKey(ZipCode)

    def __unicode__(self):
        if self.apartment:
            return "{}, {}".format(self.apartment, self.address)
        else:
            return self.address


class Tenant(models.Model):
    tenant_id = models.CharField(max_length=7, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50, db_index=True)
    mi = models.CharField(max_length=1, null=True, blank=True)

    cell_phone = PhoneNumberField(null=True, blank=True, db_index=True)
    home_phone = PhoneNumberField(null=True, blank=True, db_index=True)
    work_phone = PhoneNumberField(null=True, blank=True, db_index=True)

    @property
    def order_on(self):
        if self.mi:
            return "{}, {} {}.".format(self.last_name, self.first_name, self.mi)
        else:
            return "{}, {}".format(self.last_name, self.first_name)

    def __unicode__(self):
        if self.tenant_id:
            return "{} - {}".format(self.tenant_id, self.order_on)
        else:
            return self.order_on


class Contract(models.Model):
    first_day = models.DateField()
    last_day = models.DateField()

    tenant = models.ForeignKey(Tenant)
    unit = models.ForeignKey(Unit)

    def __unicode__(self):
        return "{} at {}".format(self.tenant.order_on, unicode(self.unit))

