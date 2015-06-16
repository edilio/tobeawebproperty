from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import *


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    photo = models.ImageField(upload_to='users', blank=True, null=True)
    title = models.CharField(max_length=250)
    edit_date = models.DateTimeField(default=timezone.now)
    phone = PhoneNumberField(default="")

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['title']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def save(self, *args, **kwargs):
        self.edit_date = timezone.now()
        super(UserProfile, self).save(*args, **kwargs)

    @property
    def order_on(self):
        return self.last_name + ', ' + self.first_name

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


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

    @property
    def current_contract(self):
        now = timezone.now()
        contracts = self.contracts.filter(first_day__lt=now, last_day__gt=now)
        if contracts.exists():
            return contracts[0]
        else:
            return None

    @property
    def current_tenant(self):
        contract = self.current_contract
        if contract:
            return contract.tenant
        else:
            return None

    def active_contracts(self, first_day, last_day):
        # test a real active contracts based on http://c2.com/cgi/wiki?TestIfDateRangesOverlap
        # ( start1 <= end2 and start2 <= end1 )
        contracts = self.contracts.filter(first_day__lte=last_day, last_day__gte=first_day)
        return contracts

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
    email = models.EmailField(null=True)

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
    move_out_date = models.DateField(null=True, blank=True)

    tenant = models.ForeignKey(Tenant)
    unit = models.ForeignKey(Unit, related_name="contracts")

    @property
    def move_out(self):
        return True if self.move_out_date else False

    def __unicode__(self):
        return "{} at {}".format(self.tenant.order_on, unicode(self.unit))

