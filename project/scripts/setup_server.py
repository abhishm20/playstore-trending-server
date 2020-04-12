# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from core.models import SystemVariable

from django.db import connection


def run():
    cursor = connection.cursor()
    cursor.execute("use play_store_replica;")
    cursor.execute("ALTER DATABASE play_store_replica CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
    cursor.execute("ALTER TABLE core_package CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
    if SystemVariable.objects.all().count() == 0:
        SystemVariable.objects.create(is_scraping_running=False)
