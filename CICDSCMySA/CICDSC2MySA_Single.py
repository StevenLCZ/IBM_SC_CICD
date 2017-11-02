#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
from time import ctime
import random
import re
from selenium.webdriver.support.select import Select
from STxlsdata import get_data


sc4bp_url = 'https://svt5lb01bp.rtp.raleigh.ibm.com/sales/salesconnect/'


driver = webdriver.Firefox()
timeout = 20
driver.set_page_load_timeout(180)

def switchWin(windowTitle):
    windows = driver.window_handles
    for window in windows:
        driver.switch_to_window(window)
        if driver.title == windowTitle:
            break


def is_element_exist_by_css(element):
    try:
        driver.find_element_by_css_selector(element)
        return True
    except:
        print 'element '+element+' is not found'
        return False


def is_element_exist_by_xpath(element):
    try:
        driver.find_element_by_xpath(element)
        return True
    except:
        print 'element '+element+' is not found'
        return False


def is_element_visible(element):
    try:
        the_element = EC.visibility_of_element_located(element)
        assert the_element(driver)
        return True
    except:
        return False


def is_alert_exist():
    try:
        driver.switch_to_alert()
        print 'alert is existing'
        return True
    except:
        print 'alert is not existing'
        return False


def select_option(item, selection):
    eles = driver.find_elements_by_css_selector('div>span[data-fieldname]')
    op_page_items = []
    for ele in eles:  # get all valid items
        op_page_items.append(ele.get_attribute('data-fieldname'))
    if item in op_page_items:
        css_selector_item = 'span[data-fieldname="'+item+'"]'
        driver.find_element_by_css_selector(
            css_selector_item).location_once_scrolled_into_view
        driver.find_element_by_css_selector(css_selector_item).click()
        options = driver.find_elements_by_css_selector('li>div[role="option"]')
        sleep(3)
        options[selection].click()
    else:
        print 'Selected item is not on the page'


def wait_element(element, time):
    i = 0
    while not is_element_exist_by_xpath(element):
        sleep(1)
        i = i+1
        if i > time:
            print 'Wait time out'
            break

def login_sc_svt():
    driver.find_element_by_id('desktop').send_keys(get_data(2.3))
    driver.find_element_by_name('password').send_keys(get_data(2,4))
    driver.find_element_by_name('password').send_keys(Keys.ENTER)




driver.get(sc4bp_url)
login_sc_svt()

sleep(5)
driver.find_element_by_id('arrow').click()  # Close the bottom banner

if is_element_exist_by_css('h3'):
    if driver.find_element_by_css_selector("h3").text == "User Locale Settings":
        driver.find_element_by_class_name('btn-primary').click()
        sleep(2)
        if driver.find_element_by_css_selector('h3').text == "Setup Complete":
            driver.find_element_by_css_selector(
                'a[class="btn btn-primary"]').click()

driver.find_element_by_xpath('//div[2]//div[1]/ul/li[2]/span/a').click()

