# coding: utf8
from __future__ import unicode_literals, print_function, division
from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException


@pytest.mark.selenium
def test_datatable(selenium):
    dt = selenium.get_datatable('/phylogenys')
    sleep(0.5)
    assert dt.get_info().filtered


@pytest.mark.selenium
def test_param(selenium):
    selenium.browser.get(selenium.url('/phylogenys/p?parameter=p2'))
    sleep(0.5)


@pytest.mark.selenium
def test_popover(selenium):
    selenium.browser.get(selenium.url('/phylogenys/p'))
    sleep(0.5)
    marker = selenium.browser.find_element_by_xpath(
        "//*[name()='svg']//*[name()='circle' and @id='m-tlpkcari1277-None']")
    marker.click()
    sleep(0.5)
    close = selenium.browser.find_element_by_xpath('//button[text()="Close"]')
    close.click()
    sleep(0.2)
    with pytest.raises(NoSuchElementException):
        selenium.browser.find_element_by_xpath('//button[text()="Close"]')
