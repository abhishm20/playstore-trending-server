# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db.models import Q

from celery_config import celery_app
from core.models import Package, SystemVariable
from core.scraper.main import AppScraper
from core.serializers import PackageSerializer, PackageAttachmentSerializer


@celery_app.task(name="scrap_app_detail_task", queue="default_queue")
def scrap_app_detail_task(package_names):
    scraper = AppScraper()
    for package_name in package_names:
        data = scraper.scrap_detail(package_name)
        attachments = data.get('attachments', [])
        instance = Package.objects.get(package_name=package_name)
        ser = PackageSerializer(instance, data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        for attachment in attachments:
            attachment.update({'package': instance.id})
            s = PackageAttachmentSerializer(data=attachment)
            s.is_valid(raise_exception=True)
            s.save()

    SystemVariable.objects.all().update(is_scraping_running=False)


@celery_app.task(name="scrap_listing_task", queue="default_queue")
def scrap_listing_task():
    instance = AppScraper()
    data = instance.scrap_list()
    refreshed_at = data['refreshed_at']
    found_packages = []
    new_packages = []
    SystemVariable.objects.all().update(is_scraping_running=True)
    for item in data['packages']:
        found_packages.append(item['package_name'])
        if Package.objects.filter(package_name=item['package_name']).exists():
            Package.objects.filter(package_name=item['package_name']).update(refreshed_at=refreshed_at)
        else:
            d = {
                'package_name': item['package_name'],
                'category': item['category'],
                'refreshed_at': refreshed_at
            }
            ser = PackageSerializer(data=d)
            ser.is_valid(raise_exception=True)
            ser.save()
            new_packages.append(item['package_name'])
    Package.objects.select_for_update().filter(~Q(package_name__in=found_packages)).update(refreshed_at=refreshed_at,
                                                                                           is_active_on_playstore=False)
    scrap_app_detail_task.delay(new_packages)


@celery_app.task(name="scrap_app_detail_for_pending_task", queue="default_queue")
def scrap_app_detail_for_pending_task():
    SystemVariable.objects.all().update(is_scraping_running=True)
    package_names = Package.objects.filter(Q(app_name__isnull=True) | Q(app_name='')).values_list('package_name', flat=True)
    scrap_app_detail_task.delay(list(package_names))
