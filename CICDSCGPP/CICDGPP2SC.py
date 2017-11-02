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


# Initial
sc_url = 'https://svt6lb01a.rtp.raleigh.ibm.com/sales/salesconnect/#'
gpp_url = 'https://www-sso.toronto.ca.ibm.com/partnerworld/gpp/atlanta/bwg3/us/en'
driver = webdriver.Firefox()
driver.implicitly_wait(20)

# Defination
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


# Login GPP to setup a BP opportunity
driver.get(gpp_url)
driver.find_element_by_id('username').send_keys('BCCSME40@us.ibm.com')
driver.find_element_by_id('password').send_keys('pass1word')
driver.find_element_by_id('password').send_keys(Keys.ENTER)

sleep(5)

i = 0
while i < 10:
    if is_element_exist_by_xpath("/html/body"):
        driver.refresh()
        i = i+1
    else:
        break

sleep(5)

# Click Menu Opportunity
driver.switch_to.frame(0)
driver.switch_to.frame(1)  # 2nd navigate bar
driver.find_element_by_xpath(
    "//div[3]/table/tbody/tr/td[3]/a").click()

# Click button NEW
driver.switch_to.default_content()
driver.switch_to.frame(0)
driver.switch_to.frame(3)
driver.switch_to.frame(0)

driver.find_element_by_xpath(
    "/html/body/div/form/span/div/table[1]/tbody/tr/td[4]/span/nobr/a").click()
gpp_opty = driver.find_element_by_xpath("//form//table//table/tbody/tr[3]/td[3]/div/span").text

# Input details
driver.switch_to.default_content()
driver.switch_to.frame(0)
driver.switch_to.frame(3)
driver.switch_to.frame(0)
driver.find_element_by_xpath(
    '//div/div/table/tbody/tr[4]/td[3]/div/nobr/a/img').click()  # Account
switchWin('Pick Account')
driver.find_element_by_xpath("//table//table[1]//table/tbody/tr/td[3]/span/nobr/a").click()
driver.find_element_by_xpath("//table//table[1]//table[2]/tbody/tr[1]/td[2]/nobr/input").send_keys('GE HEALTHCARE')
driver.find_element_by_xpath("//tbody//tbody/tr/td[4]/span/nobr/a").click() # Button Go
driver.find_element_by_xpath("//table//tbody/tr/td[2]/span/nobr/a").click() # Button OK

switchWin('IBM Global Partner Portal')
driver.find_element_by_xpath(
    "//div/div/table/tbody/tr[7]/td[3]/div/nobr/textarea").send_keys('Test for GPP to SC')  # Description

gpp_sales_stage_options=driver.find_element_by_xpath(
    '//div/div/table/tbody/tr[4]/td[6]/div/nobr/select')    # Sales Stage
Select(gpp_sales_stage_options).select_by_index(1)

driver.find_element_by_xpath(
    '//div/div/table/tbody/tr[3]/td[8]/div/nobr/input').clear()  # Revenue
driver.find_element_by_xpath(
    '//div/div/table/tbody/tr[3]/td[8]/div/nobr/input').send_keys('9988')
driver.find_element_by_xpath(
    '//div/div/table/tbody/tr[3]/td[8]/div/nobr/input').send_keys(Keys.TAB)
sleep(2)

gpp_probabillity_options=driver.find_element_by_xpath(
    '//div/div/table/tbody/tr[5]/td[8]/div/nobr/select')  # Probabillity
Select(gpp_probabillity_options).select_by_index(3)

#Save the gpp opportunity
driver.find_element_by_xpath("//form/div/table///table[2]/tbody/tr/td[3]/span/a").click()

if is_alert_exist():
    driver.switch_to.alert.accept()

try:
    gpp_error = driver.find_element_by_xpath("//table//table[4]//td[@class='error']")
    print gpp_error.text
except:
    pass

if is_element_exist_by_xpath("//table//table[4]//td[@class='error']"):
    gpp_error = driver.find_element_by_xpath("//table//table[4]//td[@class='error']").text
    print gpp_error
    driver.quite()

i = 0
while i<61:
    sleep(1)
    print 'Waiting for data transfer from GPP to SC...'+'('+str(i)+')'
    i = i+1

# Verify in SC after waiting for 60s
# Login SC
driver.get(sc_url)
driver.find_element_by_id('desktop').send_keys('seller_stg_006@cn.ibm.com')
driver.find_element_by_name('password').send_keys('zuo123nico')
driver.find_element_by_name('password').send_keys(Keys.ENTER)

# Indicate if this is a new user
sleep(5)
driver.find_element_by_id('arrow').click()  # Close the bottom banner

if is_element_exist_by_css('h3'):
    if driver.find_element_by_css_selector("h3").text == "User Locale Settings":
        driver.find_element_by_class_name('btn-primary').click()
        sleep(2)
        if driver.find_element_by_css_selector('h3').text == "Setup Complete":
            driver.find_element_by_css_selector(
                'a[class="btn btn-primary"]').click()
sleep(10)

#Navigate to Opportunities module
driver.find_element_by_xpath("//body/div[1]//div[1]/ul/li[2]//a[@aria-label='Opportunities']").click()
driver.find_element_by_xpath("//body/div[1]//div[1]/a/span[1]/span").click()
driver.find_element_by_xpath("//div[6]/ul/li[2]/div/div").click()


#Assert the flow from SC to GPP
if gpp_opty == opty_id:
    print opty_id+'flows to SC successfully!'
else
    print opty_id+'is failed to flow to SC!'

#END






















