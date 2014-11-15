from django.db import models
from django.db.models.loading import get_model
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.conf import settings

from .states import STATE_CHOICES


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
    question = models.CharField(max_length=250)
    answer = models.TextField()

    class Meta:
        ordering = ['index']

    def __unicode__(self):
        return self.question[:25]

    @property
    def short_answer(self):
        return self.answer[:250]


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
        return self.title


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


class Organization(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip = models.CharField(max_length=11)
    logo = models.ImageField(upload_to="logos")
    home_page = models.TextField()
    five_year_plan = models.FileField(null=True, blank=True)
    selected_theme = models.CharField(max_length=100, default='default')

    @property
    def city_state_zip(self):
        return '{0}, {1} {2}'.format(self.city, self.state, self.zip)

    @property
    def carousel_info(self):
        return self.carousel.all()

    def __unicode__(self):
        return self.name


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
    picture = models.ImageField(upload_to="photos")
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    organization = models.ForeignKey(Organization, related_name="carousel")

    def __unicode__(self):
        return self.title


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