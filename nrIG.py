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
from datetime import datetime
import pyautogui as pag
from docutil import DocUtil



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

        self.FOLLOW_BUFFER_DURATION = 60



    def ScrollPopupBoxNew(self, pop_up_box, target_element_selector):
        num_elements_found_old = -1
        num_elements_found = 0

        ActionChains(self.browser).move_to_element(pop_up_box).click().send_keys(Keys.PAGE_DOWN).perform()
        sleep(3)
        ActionChains(self.browser).move_to_element(pop_up_box).click().perform()

        found_ig_accounts = []


        while num_elements_found_old != num_elements_found:
   
            for i in range(0,5):
                ActionChains(self.browser).move_to_element(pop_up_box).send_keys(Keys.PAGE_DOWN).perform()
                sleep(1)
            tmp = num_elements_found

            users_found = self.browser.find_elements(by=By.CSS_SELECTOR, value=target_element_selector)
            num_elements_found = len(users_found)
            num_elements_found_old = tmp


            start_index = num_elements_found_old - 1
            if start_index < 0: start_index = 0
            end_index = num_elements_found - 1
            
            found_ig_accounts_tmp = users_found[start_index: end_index]
            for found_ig_account in found_ig_accounts_tmp:
                try:
                    account_text = found_ig_account.text.upper().split("\n")
                    user_name = account_text[0]
                    following_status = account_text[2]
                    print("FOUND USER {} : {}".format(user_name, following_status))
                    if following_status != "FOLLOW":
                        continue

                    follow_button = found_ig_account.find_element(by=By.CSS_SELECTOR, value="div.{}".format("Pkbci button"))
                    follow_button.click()
                    sleep(2)
                    if follow_button.text.upper() == "FOLLOW":
                        print("LIMIT REACHED")
                        continue
                    print("FOLLOWED USER {}".format(user_name))
                    sleep(self.FOLLOW_BUFFER_DURATION)
                except Exception as e:
                    continue

            

            
 

    
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

    



    def ActOnFollowers(self, follower_file):
        print("ACTING ON {}".format(follower_file))
        
    
        FOLLOW_BOT_DELAY_IN_SECONDS = 60
        ig_accounts = eval(open(follower_file, "r").read())
        
        for ig_account in ig_accounts[120:]:
            self.browser.get(ig_account)
            try:
                header = WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.presence_of_element_located((By.TAG_NAME,'header')))
                follow_button = [button for button in header.find_elements(by=By.CSS_SELECTOR, value='button') if button.text.lower() == 'follow'][0]
                follow_button.click()

                new_follow_status = follow_button.text.lower()
                if new_follow_status != "follow":
                    print("FOLLOWED {}".format(ig_account))

                sleep(FOLLOW_BOT_DELAY_IN_SECONDS)
            except Exception as e:
                continue

   


IGBot = nrIG()



def Follow():
    txt_files = [file for file in DocUtil.ListAllFiles(DocUtil.GetWorkingDirectory()) if DocUtil.GetExtension(file) == ".txt"]
    for txt_file in txt_files:
        IGBot.ActOnFollowers(txt_file)

    

# Follow()





def Farm():
    # DONE_ACCOUNTS = ["bathindiandancesociety","bathindiansoc", "bathtamilsoc"]

    TARGET_ACCOUNTS = ["bathindiandancesociety","bathindiansoc", "bathtamilsoc", "bathhindusoc", "bathmalayaleesoc", "thesubath"]


    for target_account in TARGET_ACCOUNTS:
        print("INITIATING {}".format(target_account))
        try:
            followers_list = IGBot.ScrollFollowers(target_account)
            # time_stamp = datetime.now().strftime("%d%m%Y")
            # file_name_followers = "{}_followers_{}.txt".format(target_account, time_stamp)
            # followers = open(file_name_followers, "w")
            # followers.write(str(followers_list))
            # followers.close()
            # print("FOUND {} FOLLOWERS FOR {}".format(str(len(followers_list)), target_account))
        except Exception as e:
            print(e)
        
        try:
            following_list = IGBot.ScrollFollowing(target_account)
            # time_stamp = datetime.now().strftime("%d%m%Y")

            # file_name_following = "{}_following_{}.txt".format(target_account, time_stamp)
            # following = open(file_name_following, "w")
            # following.write(str(following_list))
            # following.close()
            # print("FOUND {} FOLLOWERS FOR {}".format(str(len(following_list)), target_account))

        except Exception as e:
            print(e)

        print("DONE_{}".format(target_account))


Farm()









