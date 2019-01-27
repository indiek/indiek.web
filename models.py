from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # this is the User model from django
from django.urls import reverse


class dbTopic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    level = models.PositiveSmallIntegerField(default=1)

    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    subtopics = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={'pk': self.pk}) # returns the full path as a string


class dbItem(models.Model):
    quickname = models.CharField(max_length=100)
    description = models.TextField()
    item_url = models.URLField(max_length=2083)

    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    children = models.ManyToManyField('self', symmetrical=False, blank=True)
    topics = models.ManyToManyField(dbTopic, blank=True, limit_choices_to={'author': self.author})

    def __str__(self):
        return self.quickname

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk}) # returns the full path as a string



