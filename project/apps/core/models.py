# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from core import utility
from django.db import models


# Customr Model just for testing
class SystemVariable(models.Model):
    is_scraping_running = models.BooleanField(default=False)
    error_while_scraping = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "System Variable"
        verbose_name_plural = "System Variables"

    def __repr__(self):
        return f"{SystemVariable.__name__} <{self.id}>"


class Package(models.Model):
    package_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=200)
    app_name = models.CharField(max_length=100, null=True, blank=True)
    developer_name = models.CharField(max_length=100, null=True, blank=True)
    developer_site = models.TextField(null=True, blank=True)
    rating = models.CharField(max_length=100, null=True, blank=True)
    icon_url = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True, default=utility.get_current_time)
    refreshed_at = models.DateTimeField(null=True, blank=True)
    is_active_on_playstore = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"
        ordering = ('-created_at',)

    def __repr__(self):
        return f"{Package.__name__} <{self.package_name}>"


class PackageAttachment(models.Model):
    created_at = models.DateTimeField(null=True, blank=True, default=utility.get_current_time)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='attachments', related_query_name='attachment')
    url = models.TextField()
    type = models.CharField(max_length=20, choices=(('image', 'Image'), ('video', 'Video')))

    class Meta:
        verbose_name = "Package Attachment"
        verbose_name_plural = "Package Attachments"
        ordering = ('created_at',)

    def __repr__(self):
        return f"{PackageAttachment.__name__} <{self.package}>"
