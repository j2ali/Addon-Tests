#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from time import strptime, mktime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from pages.desktop.base import Base


class ExtensionsHome(Base):

    _page_title = 'Featured Extensions :: Add-ons for Firefox'
    _extensions_locator = (By.CSS_SELECTOR, "div.items div.item.addon")
    _default_selected_tab_locator = (By.CSS_SELECTOR, "#sorter li.selected")
    _subscribe_link_locator = (By.CSS_SELECTOR, "a#subscribe")
    _featured_extensions_header_locator = (By.CSS_SELECTOR, "#page > .primary > h1")

    @property
    def extensions(self):
        return [Extension(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._extensions_locator)]

    @property
    def default_selected_tab(self):
        return self.selenium.find_element(*self._default_selected_tab_locator).text

    @property
    def subscribe_link_text(self):
        return self.selenium.find_element(*self._subscribe_link_locator).text

    @property
    def featured_extensions_header_text(self):
        return self.selenium.find_element(*self._featured_extensions_header_locator).text

    def sort_by(self, type):
        from pages.desktop.regions.result_sort import Sorter
        Sorter(self.testsetup).sort_by(type)

    @property
    def paginator(self):
        from pages.desktop.regions.paginator import Paginator
        return Paginator(self.testsetup)


class Extension(Page):
        _name_locator = (By.CSS_SELECTOR, "h3 a")
        _updated_date = (By.CSS_SELECTOR, 'div.info > div.vitals > div.updated')
        _featured_locator = (By.CSS_SELECTOR, 'div.info > h3 > span.featured')
        _user_count_locator = (By.CSS_SELECTOR, 'div.adu')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def featured(self):
            return self._root_element.find_element(*self._featured_locator).text

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        @property
        def user_count(self):
            return int(self._root_element.find_element(*self._user_count_locator).text.strip('user').replace(',', '').rstrip())

        def click(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.desktop.details import Details
            return Details(self.testsetup)

        @property
        def added_date(self):
            """Returns updated date of result in POSIX format."""
            date = self._root_element.find_element(*self._updated_date).text.replace('Added ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)

        @property
        def updated_date(self):
            """Returns updated date of result in POSIX format."""
            date = self._root_element.find_element(*self._updated_date).text.replace('Updated ', '')
            # convert to POSIX format
            date = strptime(date, '%B %d, %Y')
            return mktime(date)
