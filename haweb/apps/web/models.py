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


def next_faq():
    return next_index('FAQ')


def next_link():
    return next_index('HelpfulLink')


class FAQ(models.Model):
    index = models.PositiveIntegerField(default=next_faq)
    question = models.CharField(max_length=250)
    answer = models.TextField()

    def __unicode__(self):
        return self.question[:25]


class HelpfulLink(models.Model):
    index = models.PositiveIntegerField(default=next_link)
    title = models.CharField(max_length=250)
    url = models.URLField()
    description = models.TextField()

    def __unicode__(self):
        return self.title