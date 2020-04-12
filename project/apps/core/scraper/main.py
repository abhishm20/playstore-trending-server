import json
import os
import pathlib

from selenium import webdriver

from core import utility
from settings import RESOURCE_DIR, app_logger

CONFIG_FILE = os.path.join(pathlib.Path(__file__).parent.absolute(), "config.json")
CONFIG_DATA = json.load(open(CONFIG_FILE, 'r'))


class AppScraper(object):
    def __init__(self):
        self.browser = webdriver.Chrome(os.path.join(RESOURCE_DIR, "chromedriver"))

    def scrap_detail(self, package_name):
        data = dict()
        self.browser.get(CONFIG_DATA['PLAYSTORE_DETAIL_PAGE_LINK'].replace("PACKAGE_NAME", package_name))

        try:
            name = self.browser.find_element_by_tag_name(CONFIG_DATA['DETAIL_APP_NAME'])
            data['app_name'] = name.text
        except Exception as e:
            app_logger.exception(e)

        try:
            icon = self.browser.find_element_by_css_selector(CONFIG_DATA['DETAIL_ICON_URL'])
            data['icon_url'] = icon.get_attribute('src')
        except Exception as e:
            app_logger.exception(e)

        try:
            screen_shot_div = self.browser.find_element_by_css_selector(CONFIG_DATA['DETAIL_SCREENSHOT_DIV'])
            attachments = []
            for child_div in screen_shot_div.find_elements_by_css_selector('*'):
                if child_div.tag_name == 'div':
                    try:
                        video_div = child_div.find_element_by_css_selector('div > button')
                        if video_div.get_attribute('data-trailer-url'):
                            attachments.append({
                                'url': video_div.get_attribute('data-trailer-url'),
                                'type': 'video'
                            })
                    except Exception as e:
                        app_logger.exception(e)

                elif child_div.tag_name == 'img' and child_div.get_attribute('data-src'):
                    attachments.append({
                        'url': child_div.get_attribute('data-src'),
                        'type': 'image'
                    })
            data['attachments'] = attachments
        except Exception as e:
            app_logger.exception(e)

        try:
            developer_tag = self.browser.find_element_by_css_selector(CONFIG_DATA['DETAIL_DEVELOPER'])
            data['developer_site'] = developer_tag.get_attribute('href')
            data['developer_name'] = developer_tag.text
        except Exception as e:
            app_logger.exception(e)

        try:
            data['rating'] = self.browser.find_element_by_css_selector(CONFIG_DATA['DETAIL_RATING']).get_attribute(
                'aria-label')
        except Exception as e:
            app_logger.exception(e)
        app_logger.info(data)
        return data

    def scrap_list(self):
        data = {
            'refreshed_at': utility.get_current_time(),
            'packages': []
        }
        self.browser.get(CONFIG_DATA['PLAYSTORE_LIST_PAGE_LINK'])

        for category in ['TOP_FREE_APP', 'TOP_PAID_APP', 'TOP_GROSSING_APP',
                         'TOP_FREE_GAMES', 'TOP_PAID_GAMES', 'TOP_GROSSING_GAMES']:
            try:
                category_div = self.browser.find_element_by_css_selector(CONFIG_DATA[f"LIST_{category}"])
            except Exception as e:
                app_logger.exception(e)
                continue

            for child in category_div.find_elements_by_css_selector('*'):
                if child.tag_name == 'a':
                    link = child.get_attribute('href')
                    if link and 'details?id=' in link and len(link.split("details?id=")) > 1:
                        package_name = link.split("details?id=")[-1]
                        if package_name not in [a['package_name'] for a in data['packages']]:
                            data['packages'].append({
                                'category': category,
                                'package_name': package_name
                            })
        app_logger.info(data)
        return data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()
