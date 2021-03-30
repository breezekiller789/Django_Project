#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # 當使用者成功update文章，就帶他回去他的文章頁面。
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
