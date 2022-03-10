from pydoc import Doc
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



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

    def PullData(self, instagramName):
        self.browser.get(self.IGURL + instagramName)

        # click followers
        WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'))).click()

        # we need to scroll until no more followers are loaded. 

        # get every li element.

        # do the same with following.


            
    def BypassAuthentification(self):
        pass

IGBot = nrIG()
IGBot.PullData("bathunisikhsoc")


while True:
    i = 3






