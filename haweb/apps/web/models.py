from django.db import models
from django.db.models.loading import get_model
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.conf import settings

from pygeocoder import Geocoder

# from haweb.libs.image import resize

from haweb.apps.core.states import STATE_CHOICES


def gen_resizing_help(width, height):
    video_url = "https://www.youtube.com/watch?v=lMd6nQeryjs"
    return "Please, use this video {} to crop the img to {}x{} pixels".format(video_url, width, height)


def next_index(model_name, app='web'):
    model = get_model(app, model_name)

    qs = model.objects
    try:
        m = qs.reverse()[0]
        return m.index + 1
    except IndexError:
        return 1


def next_faq_index():
    return next_index('FAQ')


class FAQ(models.Model):
    index = models.PositiveIntegerField(default=next_faq_index)
    question = models.CharField(max_length=250, unique=True)
    answer = models.TextField()
    slug = models.SlugField(editable=False, max_length=280, default='')

    class Meta:
        ordering = ['index']

    def __unicode__(self):
        return self.question[:25]

    @property
    def short_answer(self):
        return self.answer[:250]

    @models.permalink
    def get_absolute_url(self):
        return ('faq', (), {
            'slug': slugify(self.question)
        })

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(FAQ, self).save(*args, **kwargs)


def next_helpful_link_index():
    return next_index('HelpfulLink')


class HelpfulLink(models.Model):
    index = models.PositiveIntegerField(default=next_helpful_link_index)
    title = models.CharField(max_length=250)
    url = models.URLField()
    description = models.TextField()

    class Meta:
        ordering = ['index']

    def __unicode__(self):
        return self.title

    @property
    def short_description(self):
        return self.description[:250]


def next_career_index():
    return next_index('Career')


class Career(models.Model):
    index = models.PositiveIntegerField(default=next_career_index)
    title = models.CharField(max_length=250)
    description = models.TextField()

    class Meta:
        ordering = ['index']

    def __unicode__(self):
        return self.title

    @property
    def short_description(self):
        return self.description[:250]


class ResourceCategory(models.Model):
    index = models.PositiveIntegerField(default=next_career_index)
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ['index']
        verbose_name_plural = "categories"
        verbose_name = "category"

    def __unicode__(self):
        return self.name


def next_resource_index():
    return next_index('ResourceForm')


class ResourceForm(models.Model):
    index = models.PositiveIntegerField(default=next_resource_index)
    name = models.CharField(max_length=250)
    description = models.TextField()
    resource = models.FileField(upload_to="resources")
    visible = models.BooleanField(default=True)
    category = models.ForeignKey(ResourceCategory)

    class Meta:
        ordering = ['index']

    def __unicode__(self):
        return self.name

    @property
    def short_description(self):
        return self.description[:250]


THEMES_OPTIONS = (
    ('default', 'Default'),
    ('cerulean', 'Cerulean'),
    ('cosmo', 'Cosmo')
)


class Organization(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip = models.CharField(max_length=11)
    logo = models.ImageField(upload_to="logos", help_text=gen_resizing_help(140, 140))
    home_page = models.TextField()
    about_us_page = models.TextField(default="")
    contact_us_page = models.TextField(default="")
    five_year_plan = models.FileField(null=True, blank=True)
    selected_theme = models.CharField(max_length=100, default='default', choices=THEMES_OPTIONS)
    lat = models.FloatField(default=25.8649876, blank=True, help_text="latitude... put 0 if you don't know")
    lng = models.FloatField(default=-80.26423799999999, blank=True, help_text="longitude... put 0 if you don't know")

    @property
    def city_state_zip(self):
        return '{0}, {1} {2}'.format(self.city, self.state, self.zip)

    @property
    def carousel_info(self):
        result = self.carousel.all()
        return enumerate(result)

    def __unicode__(self):
        return self.name

    def is_lat_long_valid(self):
        lat = self.lat
        lng = self.lng
        invalid = ((lat == 25.8649876) and (lng == -80.264238)) or (lat == 0 and lng == 0)
        return not invalid

    def save(self, *args, **kwargs):
        # meaning the user left the fields in blank
        if not self.is_lat_long_valid():
            full_address = "{0} {1}".format(self.address, self.city_state_zip)
            results = Geocoder.geocode(full_address)
            self.lat, self.lng = results[0].coordinates
        super(Organization, self).save(*args, **kwargs)


class Menu(models.Model):
    index = models.PositiveSmallIntegerField(default=1)
    name = models.CharField(max_length=50)
    link = models.CharField(default="#", max_length=250)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    @property
    def is_divider(self):
        return self.name.lower() == 'divider'

    @property
    def how_many_children(self):
        return self.children.count()

    @property
    def children_orderby_index(self):
        return self.children.all().order_by('index')

    def __unicode__(self):
        return self.name


class CarouselInfo(models.Model):
    picture = models.ImageField(upload_to="photos", help_text=gen_resizing_help(1024, 300))
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    organization = models.ForeignKey(Organization, related_name="carousel")

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(CarouselInfo, self).save(force_insert, force_update, using, update_fields)
        # resize(self.picture)


class Content(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    slug = models.SlugField(editable=False, max_length=280)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, related_name="created_content")
    created_on = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, related_name="modified_content", null=True)
    modified_on = models.DateTimeField(null=True, blank=True, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return ('content', (), {
            'slug': self.slug
        })

    def gen_slug(self):
        base = '{0}-{1}'.format(self.id, self.title)
        return slugify(base)

    def save(self, *args, **kwargs):
        first_time = self.id is None
        self.slug = self.gen_slug()
        if self.modified_by:
            self.modified_on = timezone.now()

        super(Content, self).save(*args, **kwargs)
        if first_time:
            self.save(*args, **kwargs)

    def __unicode__(self):
        return self.title


# PRIORITY_CHOICES = (
#     (1, 'High'),
#     (2, 'Medium'),
#     (3, 'Low'),
# )
#
#
# class WorkOrder(models.Model):
#     work_order_no = models.CharField(max_length=12)
#     priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES)
#     scheduled = models.DateTimeField(default=timezone.now())
#
#     def __unicode__(self):
#         return self.work_order_no