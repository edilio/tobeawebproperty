from django.db import models
from django.db.models.loading import get_model


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

    def __unicode__(self):
        return self.title

    @property
    def short_description(self):
        return self.description[:250]


class ResourceCategory(models.Model):
    index = models.PositiveIntegerField(default=next_career_index)
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.title
