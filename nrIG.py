import profile
from pydoc import Doc
from time import sleep
import re

from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
import datetime




TARGET_ACCOUNT = "thasbath"
class nrIG:
    def __init__(self):
        self.TIMEOUT_DURATION  = 3
        self.IGURL = 'https://www.instagram.com/'
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        
        user_data_dir = r"C:\Users\jasbi\AppData\Local\Microsoft\Edge\User Data\Selenium Dev"
        edge_options.add_argument("user-data-dir={}".format(user_data_dir)); 

        edge_options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        driver_location = r"D:\FILES\Desktop\other\IGTools\msedgedriver.exe"


        self.browser = Edge(executable_path=driver_location, options=edge_options)

        self.browser.get(self.IGURL)

    def ScrollPopupBoxNew(self, pop_up_box, target_element_selector):
        num_elements_found_old = -1
        num_elements_found = 0

        ActionChains(self.browser).move_to_element(pop_up_box).click().send_keys(Keys.PAGE_DOWN).perform()
        sleep(3)
        ActionChains(self.browser).move_to_element(pop_up_box).click().perform()






        while num_elements_found_old != num_elements_found:
   
            for i in range(0,5):
                ActionChains(self.browser).move_to_element(pop_up_box).send_keys(Keys.PAGE_DOWN).perform()
                sleep(0.5)
            tmp = num_elements_found

            users_found = self.browser.find_elements(by=By.CSS_SELECTOR, value=target_element_selector)
            num_elements_found = len(users_found)
            num_elements_found_old = tmp

            


    def ScrollPopupBox(self, popupBox, liCssSelector):
        numFoundOld = -1
        numFound = 0
        while numFound != numFoundOld:
            for i in range(0,5):
                self.browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',popupBox)
                sleep(1)
            tmp = numFound
            numFound = len([account for account in self.browser.find_elements_by_css_selector(liCssSelector)])
            numFoundOld = tmp


    
    def ScrollFollowing(self, instagramName):
        self.browser.get(self.IGURL + instagramName)
        WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'))).click()
        followersBox =  WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div._1XyCr')))
        self.ScrollPopupBoxNew(followersBox, 'div._1XyCr ul li')
        return [element.get_attribute("href") for element in self.browser.find_elements(by=By.CSS_SELECTOR, value="a.notranslate._0imsa")]


    def ScrollFollowers(self, instagramName):
        self.browser.get(self.IGURL + instagramName)
        WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'))).click()
        followersBox =  WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.isgrP')))
        self.ScrollPopupBoxNew(followersBox, 'div.isgrP ul li')
        return [element.get_attribute("href") for element in self.browser.find_elements(by=By.CSS_SELECTOR, value="a.notranslate._0imsa")]

    def PullData(self, instagramName):

        self.browser.get(self.IGURL + instagramName)
        links = self.ScrollFollowers()






        
        # found_people_following_statuses = self.browser.find_elements(by=By.CSS_SELECTOR, value="div.{}".format("Pkbci button"))
        # for following_status_button in found_people_following_statuses:
        #     following_status_value = following_status_button.find_element(by=By.TAG_NAME, value="div").text.lower()
        #     if following_status_value == "follow":
        #         # following_status_button.click()
        #         print("REQUESTED")


IGBot = nrIG()

TARGET_ACCOUNTS = ["bathindiansoc"]
for target_account in TARGET_ACCOUNTS:

    followers = IGBot.ScrollFollowers(target_account)
    following = IGBot.ScrollFollowing(target_account)

    time_stamp = datetime.now().strftime("%d/%m/%Y")
    file_name_followers = "{}_followers_{}.txt".format(target_account, time_stamp)
    file_name_following = "{}_following_{}.txt".format(target_account, time_stamp)

    followers = open(file_name_followers, "w")
    followers.write(str(followers))
    followers.close()

    following = open(file_name_following, "w")
    following.write(str(following))
    following.close()









