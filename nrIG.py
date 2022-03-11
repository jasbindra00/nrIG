from pydoc import Doc
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class nrIG:
    def __init__(self):
        self.TIMEOUT_DURATION  = 3
        self.IGURL = 'https://www.instagram.com/'
        print("Configuring browser options...")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        chromeProfileLocation = r"C:\Users\jasbi\AppData\Local\Google\Chrome\User Data\Default"

        options.add_argument("user-data-dir="+chromeProfileLocation)
        # options.add_experimental_option("prefs",{"download.default_directory" : EXPENDITURE_SAVE_LOCATION})

        print("Launching browser...")
        self.browser = webdriver.Chrome(r"D:\FILES\Desktop\other\Expenditure analysis\chromedriver.exe", chrome_options=options)

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
        

        try:
            # traverse the popup box.
            self.ScrollPopupBox(followersBox, 'li.wo9IH')
            followers = self.browser.find_elements_by_css_selector('li.wo9IH')
            print(str(len(followers)) + "found")

            # click close.
            WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/div/div/div/div[1]/div/div[2]/button'))).click()
            
            WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'))).click()
            followingBox =  WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div._1XyCr')))

            self.ScrollPopupBox(followingBox, 'body > div.RnEpo.Yx5HN > div > div > div > div.isgrP > ul > div > li:nth-child(1) > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.yC0tu')


        except(Exception):
            pass
        # keep scrolling until the size of the list is numFollowers

        # # we need to scroll until no more followers are loaded. 

        # get every li element.

        # do the same with following.


            
    def BypassAuthentification(self):
        pass

IGBot = nrIG()
IGBot.PullData("bathunisikhsoc")


while True:
    i = 3






