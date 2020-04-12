# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os
import unittest
from core.scraper.main import AppScraper


class TestScraperUtil(unittest.TestCase):
    # def test_detail_page_name(self):
    #     data = AppScraper().scrap_detail("us.zoom.videomeetings")
    #     self.assertTrue(data)

    def test_list_page_name(self):
        data = AppScraper().scrap_list()
        self.assertTrue(data)
