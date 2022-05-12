from multiprocessing.pool import RUN
import profile
from pydoc import Doc
from time import sleep
import re
from cv2 import accumulate

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from docutil import DocUtil

import atexit
import threading

class nrIG:
    def __init__(self, owner_account):
        self.SAVE_MODE = True
        self.owner_account = owner_account
        self.RUNNING = True
        self.REQUESTS_SENT = eval(open("requests_sent.txt", "r").read())


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

        self.IG_REQUEST_BUFFER_DURATION = 60


        listener_thread = threading.Thread(target=self.ListenForCommands)
        listener_thread.setDaemon(True)
        listener_thread.start()


    def ScrollOnElement(self, element, element_css_selector, sleep_duration = 0):
        JS_injection = '''
        var fDialog = document.querySelector('{}');
        fDialog.scrollTop = fDialog.scrollHeight
            '''.format(element_css_selector)

        self.browser.execute_script(JS_injection)
        if sleep_duration != 0:
            sleep(sleep_duration)


    def ScrollPopupBox(self,host_page,popup_box_link_xpath,popup_box_xpath,pop_up_box_element_selector, element_handler, additional_arguments):
        # navigate to the host page.
        self.browser.get(host_page)

        # click the link which activates the popup box
        if popup_box_link_xpath:
            WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,popup_box_link_xpath))).click()

        # obtain the pop_up_box
        pop_up_box =  WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.presence_of_element_located((By.CSS_SELECTOR,popup_box_xpath)))

        num_elements_found_old = -1
        num_elements_found = 0

        ActionChains(self.browser).move_to_element(pop_up_box).click().send_keys(Keys.PAGE_DOWN).perform()
        self.ScrollOnElement(pop_up_box, popup_box_xpath,3)

        found_ig_accounts = []

        while num_elements_found_old != num_elements_found and self.RUNNING:
            if not self.RUNNING: break
   
            for i in range(0,5): self.ScrollOnElement(pop_up_box,popup_box_xpath, 1)
            tmp = num_elements_found

            users_found = self.browser.find_elements(by=By.CSS_SELECTOR, value=pop_up_box_element_selector)
            num_elements_found = len(users_found)
            num_elements_found_old = tmp


            start_index = num_elements_found_old - 1
            if start_index < 0: start_index = 0
            end_index = num_elements_found - 1
            
            found_ig_accounts_tmp = users_found[start_index: end_index]
            if element_handler is not None:
                for found_ig_account in found_ig_accounts_tmp:
                    element_handler(found_ig_account, **additional_arguments, pop_up_box=pop_up_box)


    def __FollowUser(self, found_ig_account, **kwargs):
        try:
            account_text = found_ig_account.text.upper().split("\n")
            user_name = account_text[0]
            
            following_status = account_text[-1]
            print("FOUND USER {} : {}".format(user_name, following_status))
            
            if following_status != "FOLLOW": return
            if user_name in self.REQUESTS_SENT:
                print("SENT FOLLOW REQUEST TO {} ALREADY!".format(user_name))
                return
            try:
                follow_button = found_ig_account.find_element(by=By.CSS_SELECTOR, value="div.{}".format("Pkbci button"))
            except Exception as e:
                follow_button = found_ig_account.find_element(by=By.CSS_SELECTOR, value="button.{}".format("sqdOP.L3NKy._8A5w5"))
                                                                                     
            follow_button.click()
            sleep(2)
            if follow_button.text.upper() == "FOLLOW":
                print("FOLLOW LIMIT REACHED ON {}".format(user_name))
                return
            print("FOLLOWED USER {}".format(user_name))
            self.REQUESTS_SENT.append(user_name)
            self.SaveChanges()

            for i in range(self.IG_REQUEST_BUFFER_DURATION):
                print("SLEEPING {}TH SECOND".format(i))
                sleep(1)
        except Exception as e:
            print(e)

    def __AccrueUser(self, found_ig_account, **kwargs):
        list_of_followers = kwargs.get("list_of_followers")
        account_text = found_ig_account.text.upper().split("\n")
        user_name = account_text[0]
        user_link = 'https://www.instagram.com/{}/'.format(user_name.lower())
                    
        following_status = account_text[-1]
        print("FOUND USER {} : {}".format(user_name, following_status))
        list_of_followers.append(user_link)
            

    def __UnfollowUser(self,found_ig_account, **kwargs):
        try:
            list_of_followers = kwargs.get("list_of_followers")
            pop_up_box = kwargs.get("pop_up_box")

            account_text = found_ig_account.text.upper().split("\n")
            user_name = account_text[0]
            user_link = 'https://www.instagram.com/{}/'.format(user_name.lower())
            
            following_status = account_text[-1]
            print("FOUND USER {} : {}".format(user_name, following_status))
            try:
                follow_button = found_ig_account.find_element(by=By.CSS_SELECTOR, value="div.{}".format("Pkbci button"))
            except Exception as e:
                follow_button = found_ig_account.find_element(by=By.CSS_SELECTOR, value="button.{}".format("sqdOP.L3NKy._8A5w5"))
                      
            if user_link not in list_of_followers and following_status == "FOLLOWING":
                follow_button.click()
                try:
                    unfollow_button = [button for button in self.browser.find_elements(by=By.TAG_NAME, value='button') if button.text.lower() == "unfollow"][0]
                    unfollow_button.click()
                except Exception as e:
                    return
                sleep(2)

                if follow_button.text.upper() == "FOLLOW":
                    print("UNFOLLOWED USER {}".format(user_link))
                    self.REQUESTS_SENT.append(user_name)
                    self.SaveChanges()
                    ActionChains(self.browser).move_to_element(pop_up_box).click().perform()
                    for i in range(60):
                        print("SLEEPING {}TH SECOND".format(i))
                        sleep(1)
                    return
                
                print("LIMIT REACHED")

        except Exception as e:
            print(e)
            

    
    
    # MERGE TWO FUNCTIONS INTO ONE (V SIMILAR)
    def __ScrollFollowing(self, instagram_name, user_handler, **kwargs):
        self.ScrollPopupBox(additional_arguments = kwargs, host_page = self.IGURL + instagram_name, popup_box_link_xpath='//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a', 
        popup_box_xpath='div.isgrP', pop_up_box_element_selector='div.isgrP ul li', element_handler=user_handler)
        return self.__GetAllUserLinks()

    def __ScrollFollowers(self, instagram_name, user_handler, **kwargs):
        self.ScrollPopupBox(additional_arguments = kwargs, host_page = self.IGURL + instagram_name, popup_box_link_xpath='//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a', 
        popup_box_xpath='div.isgrP', pop_up_box_element_selector='div.isgrP ul li', element_handler=user_handler)
        return self.__GetAllUserLinks()

        
    def __GetAllUserLinks(self):
        return [element.get_attribute("href") for element in self.browser.find_elements(by=By.CSS_SELECTOR, value="a.notranslate._0imsa")]


    def FollowFollowers(self, target_account):
        followers = self.__ScrollFollowers(target_account, self.__FollowUser)
    
    def FollowFollowing(self, target_account):
        following = self.__ScrollFollowing(target_account, self.__FollowUser)



    def SaveChanges(self):
        if not self.SAVE_MODE:
            print("FAILED TO SAVE CHANGES, SAVE MODE IS DEACTIVATED")
        f = open("requests_sent.txt", "w")
        f.write(str(self.REQUESTS_SENT))
        f.close()

        print("SAVED CHANGES!")


    def ListenForCommands(self):
        while True:
            command = input("ENTER COMMAND:")
            if command.upper() == "SAVE":
                self.SaveChanges()
                print("SAVED CHANGES")
            
            if command.upper() == "EXIT":
                self.RUNNING = False
                self.SaveChanges()
                print("EXITING APPLICATION")




    def Farm(self):
        # DONE_ACCOUNTS = ["bathindiandancesociety","bathindiansoc", "bathtamilsoc"]


        TARGET_ACCOUNTS = ["bathhindusoc", "bathmalayaleesoc", "thesubath"]
        # TARGET_ACCOUNTS = ["bathindiandancesociety","bathindiansoc", "bathtamilsoc", "bathhindusoc", "bathmalayaleesoc", "thesubath"]


        for target_account in TARGET_ACCOUNTS:
            print("INITIATING {}".format(target_account))
            try:
                self.UnfollowNonFollowers()

                # self.FollowFollowers(target_account)
                # self.FollowFollowing(target_account)
            except Exception as e:
                print(e)
            print("DONE_{}".format(target_account))



    def UnfollowNonFollowers(self):


        # list_of_followers = eval(open("list_of_followers.txt", "r").read())
        list_of_followers = self.__ScrollFollowers(self.owner_account, None)
        # open("list_of_followers.txt", "w").write(str(list_of_followers))
        # list_of_followers = eval(open("list_of_followers.txt", "r").read())
        list_of_following = self.__ScrollFollowing(self.owner_account, self.__UnfollowUser, list_of_followers = list_of_followers)




        








# owner_account = "jasbindra00"

owner_account = "bathsikhsoc"
IGBot = nrIG(owner_account)

def succeeded(target_account):

    try:
        print("TARGETING ACCOUNT {}".format(target_account))
        IGBot.FollowFollowers(target_account)
        IGBot.FollowFollowing(target_account)
        IGBot.UnfollowNonFollowers()
        IGBot.SaveChanges()
        
    except Exception as e:
        print("ERROR OCCURED ON TARGET ACCOUNT {}".format(target_account))
        error_array = eval(open("errors.txt", "r").read())
        error_array.append(target_account)
        open("errors.txt", "w").write(str(error_array))
        return False
    print("TARGET ACCOUNT: {}  - DONE".format(target_account))
    return True




def main():
    

    TARGET_ACCOUNTS = ["bristolsikhsoc", "cusikhsociety", "soassikhsociety", "ukcsikhsoc", "sussexsikhsociety", "oxfordsikhsoc", "ueasikhsociety", "manchestersikhsociety","nishkamswat", 
    "uonsikhsoc", "warwicksikhsoc", "essexsikhsoc", "uop_sikhsoc","keelesikhsoc","westminstersikhsociety", 
    "uolsikhsoc", "qmulsikhsoc", "lancaster_sikhsoc", "ulawsikhsociety",
    "lsesusikhpunjabsociety", "ntusikhsoc", "sgulsikhsoc", "gresikhsoc", "surreysikhsoc",
    "imperialsikhsoc", "hertssikhsoc", "uclsikhsoc", "sikh_soc", "livsikhsoc", 
    "uobsikhsociety", "lincolnsikhsociety", "bcusikhsociety", "rhulsikhsoc", 
    "uor_sikhsociety", "dmusikhsoc", "kingssikhs", "astonsikhs", "cusikhsoc", 
    "lsusikhsoc", "coventrysikhsociety", "sikhsocsheffield", "uwlsikhsociety", 
    "roesikhsoc", "nsikhsoc", "coventrysikhsoc", "arusikhsoc", "soassikhsoc",
    "exetersikhsociety","manchestersikhsociety"]
    IGBot.UnfollowNonFollowers()

    TARGET_ACCOUNTS.reverse()
    for target_account in TARGET_ACCOUNTS:
        while not succeeded(target_account):
            continue
 
main()








