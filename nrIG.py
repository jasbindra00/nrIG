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


    def PullData(self, instagramName):
        self.browser.get(self.IGURL + instagramName)

        numFollowers = int(WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span'))).text)
        numFollowing = int(WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/div/span'))).text)
        print(numFollowers)
        print(numFollowing)

        # click followers
        WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'))).click()
        followersBox =  WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.isgrP')))
     

        # traverse the popup box.
        self.ScrollPopupBox(followersBox, 'li.wo9IH')
        found_people = self.browser.find_elements(by=By.CSS_SELECTOR, value="a.{}".format("notranslate._0imsa "))

        # get the links to everyones profiles 
        found_links = []
        for follower in found_people:
            found_links.append(follower.get_attribute("href"))
        

        # get the following buttons for each person
            # if we're not following them, follow them

        following_statuses = self.browser.find_elements(by=By.CSS_SELECTOR, value="div.{}".format("Pkbci button"))      

        for following_status_wrapper in following_statuses:
            try:
                # following_status_button = following_status_wrapper.find_element(by=By.CSS_SELECTOR, value="button")
                following_status_value = following_status_wrapper.find_element(by=By.TAG_NAME, value="div").text.lower()
                if following_status_value == "following" or following_status_value == "requested":
                    continue
                print("requesting follow")
                following_status_wrapper.click()

            except Exception as e:
                print(e)





            
    def BypassAuthentification(self):
        pass

IGBot = nrIG()

IGBot.PullData("thasbath")


while True:
    i = 3






