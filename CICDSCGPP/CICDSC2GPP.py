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


sc_url = 'https://svt6lb01a.rtp.raleigh.ibm.com/sales/salesconnect/#'
gpp_url = 'https://www-sso.toronto.ca.ibm.com/partnerworld/gpp/atlanta/bwg3/us/en'

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

# Login...

driver.get(sc_url)
driver.implicitly_wait(20)
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
driver.find_element_by_xpath('//ul/li[@id="createList"]').click()
sleep(1)
driver.find_element_by_xpath('//span/a[@data-module="Opportunities"]').click()
sleep(1)
driver.find_element_by_css_selector('textarea[name="description"]').send_keys(
    'Test Case '+ctime())  # input Opportunity Description
# active Sales Stage dropdown list
driver.find_element_by_xpath('//div/span/div/a/span').click()
# Select 04 in Sales Stage
driver.find_element_by_xpath("//ul/li[4]/div[@role='option']").click()

driver.find_element_by_xpath(
    "//div[2][@class='row-fluid panel_left']/div/span/span/div/a/span[1]").click()  # Click on Contact
driver.find_element_by_xpath("//ul[2]/li/div").click()  # Click to search more
sleep(5)

driver.find_element_by_css_selector(
    "a[name='create']").click()  # click to create new contact
sleep(1)
# Swith to Contact setup page
switchWin(u'Create Contact \xbb SalesConnect')
# Setup new Contactor
driver.find_element_by_id("first_name").send_keys("Test001")
driver.find_element_by_id("last_name").send_keys(
    "Test002")  # Setup new Contactor
driver.find_element_by_id("phone_work").send_keys("999888777")
driver.find_element_by_id("phone_mobile").send_keys("999")
emailaddr = str(random.randint(100, 999))+'@test.com'
driver.find_element_by_id("Contacts0emailAddress0").send_keys(emailaddr)
driver.find_element_by_id("btn_account_name").click()  # Open client selectr
# Switch to client selection page
switchWin(u'SalesConnect')
# Setup a related client with CMR number
driver.find_element_by_id("name_advanced").send_keys(
    '739061')  # Search for a client
driver.find_element_by_id('field_name_advanced').click()
driver.find_element_by_id('field_name_advanced').send_keys(Keys.DOWN)
driver.find_element_by_id('field_name_advanced').send_keys(Keys.DOWN)
#--driver.find_element_by_css_selector('option[label="CMR number"]').click()
checkBox_MyClients = driver.find_element_by_id(
    'current_user_only_advanced')  # Set searching range
if checkBox_MyClients.is_selected():
    checkBox_MyClients.click()
sleep(2)
driver.find_element_by_id("search_form_submit").click()
sleep(4)
driver.find_element_by_css_selector("a[href='javascript:void(0);']").click()
sleep(2)
if is_alert_exist():
    driver.switch_to_alert().accept()
# Switch back to customer setup page
switchWin(u'Create Contact \xbb SalesConnect')
# Contact setup complete
driver.find_element_by_id("SAVE_WITH_SERVER_VALIDATION").click()
sleep(5)

# Indicate if there was existing similar contactor
# this indication checking is not working fine in CI some time if the
# function is not running
if is_element_exist_by_css('table[id="contentTable"]'):
    # ignore the samilar contactor and create new
    driver.find_element_by_css_selector(
        'input[value="Confirm create"]').click()

# Switch back to OP setup page
switchWin(u'Home \xbb SalesConnect')

i = 0
while not is_element_exist_by_xpath("//tbody/tr[1]/td[2][@data-type='fullname']/span/div"):
    sleep(10)
    i = i+1
    if i > 10:
        print 'Wait Contacts TimeOut'
        break
print 'Contact displayed'

# Select the newly setup contactor by filtering the email addr
emailList = driver.find_elements_by_css_selector(
    "div[class='ellipsis_inline'][rel='tooltip']")  # All emails
emailListText = []
for i in emailList:
    x = i.text
    emailListText.append(x)
radioBtnList = driver.find_elements_by_css_selector(
    "input[type='radio'][class='selection'][name='Contacts_select']")  # All radio button
contactList = dict(zip(emailListText, radioBtnList))
contactList.get(emailaddr).click()
sleep(3)
# Client Name (Verification - should be auto selected)
autoClientName = driver.find_element_by_xpath(
    "//div/span[@data-fieldname='account_name']/span/div/a/span[1]/div").text
i = 0
# Wait until the client is auto selected and will timeout after 10s.
while autoClientName == u'Required':
    sleep(1)
    i = i + 1
    if i > 10:
        print 'Wait Client Name TimeOut'
        break
print 'Client name is auto selected'


# Source
driver.find_element_by_xpath(
    "//div/span[@data-fieldname='lead_source']/span/div/a/span[1]").click()
driver.find_element_by_xpath(
    '/html/body/div[8]/div/input').send_keys('Business Partner')
driver.find_element_by_xpath(
    '/html/body/div[8]/div/input').send_keys(Keys.ENTER)

# OP code
driver.find_element_by_xpath(
    "//div/span[@data-fieldname='solution_codes_c']/span/div/ul/li/input").click()
driver.find_element_by_xpath(
    "//div/span[@data-fieldname='solution_codes_c']/span/div/ul/li/input").send_keys('10')
driver.find_element_by_xpath(
    "//div/span[@data-fieldname='solution_codes_c']/span/div/ul/li/input").send_keys(Keys.ENTER)

# Line Item1
# Offering
driver.find_element_by_xpath(
    "//div/span[@data-fieldname='level_search']/span/div/a/span[1]").click()
driver.find_element_by_xpath("/html/body/div[11]/div/input").send_keys('BFB60')
sleep(3)
driver.find_element_by_xpath(
    "/html/body/div[11]/div/input").send_keys(Keys.ENTER)
sleep(3)
# Competitor
driver.find_element_by_xpath(
    "//div/span[@data-fieldname='competitor']/span/div/ul/li/input").send_keys('Accept 360')
driver.find_element_by_xpath(
    "//div/span[@data-fieldname='competitor']/span/div/ul/li/input").send_keys(Keys.ENTER)
# Amount
driver.find_element_by_css_selector(
    "input[aria-label='Amount'][name ='revenue_amount']").send_keys('32100.98')

select_option('roadmap_status', 1)  # Select 'Stretch' in Roadmap Status
sleep(1)
select_option('probability', 4)  # Select '75%' in Probability
sleep(1)
# select_option('stg_fulfill_type',2) #Select 'Web' in Fullfillment Type

# Submit and Save the Opportunity
driver.find_element_by_css_selector('a[name="save_button"]').click()

print 'save successfully'

wait_element("//div/div[@class='alert alert-success alert-block']/a", 10)
opty_id = driver.find_element_by_xpath(
    "//div/div[@class='alert alert-success alert-block']/a").text

print opty_id  # Opporunity ID

opty_url = sc_url+'Opportunities/'+opty_id
driver.get(opty_url)

driver.find_element_by_xpath(
    "//span/a[@name='edit_button']").click()  # click on Eidt button
driver.find_element_by_xpath(
    "//div/span[1][@data-fieldname='assigned_user_name']/span/div/a/span[1]/div").click()   # Click on OO
search_more_buttons = driver.find_elements_by_xpath(
    "//ul[2]/li/div[@class='select2-result-label']")  # Click on Search more
for each in search_more_buttons:
    try:
        each.click()
    except:
        pass

module_filters = driver.find_elements_by_xpath(
    "//div/div[1]/span[1][@class='table-cell']/div[1]/a/span[1]/span")
for each in module_filters:
    try:
        each.click()
    except:
        pass

driver.find_element_by_xpath(
    "//ul[@role='listbox']/li[2]/div/div").click()  # click on bp


search_boxes = driver.find_elements_by_xpath(
    "//div[3]/div[1]/div[1]/div/div[1]/div/input[@class='search-name']")
for each in search_boxes:
    try:
        each.send_keys('PRM2005')
    except:
        pass

driver.find_element_by_xpath(
    "//table/tbody/tr/td[1]/span/input[@class='selection'][@type='radio']").click()  # click on radio button


if is_alert_exist():
    driver.find_element_by_xpath(
        "//div[2]/a[2][@data-action='confirm']").click()

switchWin(opty_id+u' \xbb Opportunities \xbb SugarCRM')

driver.find_element_by_xpath("//a[@name='save_button']").click()

wait_element("//div/ul/li/a[@data-tabid='tab_opportunity_overview']", 5)


sleep(10)

#Login GPP sys-------
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

driver.switch_to.frame(0)
driver.switch_to.frame(1)  # 2nd navigate bar

# Click Opportunity
driver.find_element_by_xpath(
    "//div[3]/table/tbody/tr/td[3]/a").click()  

driver.switch_to.default_content()
driver.switch_to.frame(0)
driver.switch_to.frame(2)
show_options = driver.find_element_by_xpath(
    '/html/body/table[1]/tbody/tr/td[2]/form/table/tbody/tr/td[1]/select')  # select all opportunity
Select(show_options).select_by_index(1)

driver.switch_to.default_content()
driver.switch_to.frame(0)
driver.switch_to.frame(3)
driver.switch_to.frame(0)
driver.find_element_by_xpath(
    "/html/body/div/form/span/div/table[1]/tbody/tr/td[7]/span/nobr/a").click()

driver.switch_to.default_content()
driver.switch_to.frame(0)
driver.switch_to.frame(3)
driver.switch_to.frame(0)
driver.find_element_by_xpath(
    '/html/body/div/form/div/table/tbody/tr/td/span/div/div/table/tbody/tr[3]/td[3]/div/nobr/input').send_keys('KW-TMSU3C7')  # input box
driver.find_element_by_xpath(
    '/html/body/div/form/div/table/tbody/tr/td/span/table[2]/tbody/tr/td[5]/span/nobr/a').click()  # Click Go

driver.switch_to.default_content()
driver.switch_to.frame(0)
driver.switch_to.frame(3)
driver.switch_to.frame(0)
gpp_opty = driver.find_element_by_xpath(
    '/html/body/div/form/span/div/table[2]/tbody/tr/td/table/tbody/tr[2]/td[2]/a').text

#Assert the flow from SC to GPP
if gpp_opty == opty_id:
    print opty_id+'flows to GPP successfully!'
else:
    print opty_id+'is failed to flow to GPP!'

#END


















