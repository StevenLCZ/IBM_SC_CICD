#!/usr/bin/python
from STxlsdata import get_data

class SCLOGIN(object):
    def __init__(self, driver, env='',rol=''):
        self.driver = driver
        self.env = env
        self.role = role

    def login_gpp(self):
        driver.find_element_by_id('username').send_keys(get_data(4.3))
        driver.find_element_by_id('password').send_keys(get_data(4.4))
        driver.find_element_by_id('password').send_keys(Keys.ENTER)

    def login_sc_svt(self):
        driver.find_element_by_id('desktop').send_keys(get_data(2.3))
        driver.find_element_by_name('password').send_keys(get_data(2,4))
        driver.find_element_by_name('password').send_keys(Keys.ENTER)

    def login_sc_ci(self):
        pass

