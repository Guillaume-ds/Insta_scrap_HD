from selenium import webdriver
import logging
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.chrome.options import Options

from time import sleep 
import pandas as pd
import os
import streamlit as st

from bs4 import BeautifulSoup

class instaScrapper():
    """
    Class dealing with instagram interactions
    - login
    - comments scrapping
    """

    def __init__(self):
        @st.cache_resource 
        def installff():
            os.system('sbase install geckodriver')
            os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

        _ = installff()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.wd = webdriver.Firefox(options=opts)
        
        logging.warning('init scrapper over')
       # except:
       #     print('exception')
        #    self.wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #self.wd.maximize_window()
        self.url = "https://www.instagram.com/"
        self.see_more = 0

    def login_instagram(self,username,pw):
        """
        Function that instanciates a web driver and connects the user to instagram

        INPUTS:
            username: str
                Instagram username
            pw: str
                Instagram password
        
        Note: sleeps are there to avoid bot detection
        """
        logging.warning('init login in ')
        self.wd.get(self.url)
        self.wd.implicitly_wait(5)
        logging.warning('got url ')
        sleep(0.5)

        # cookie_button = WebDriverWait(self.wd,15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]")))
        # cookie_button.click() 
        # print('got cookies ')
        # sleep(0.9)

        username_field = WebDriverWait(self.wd,12).until(EC.presence_of_element_located((By.NAME,'username')))
        username_field.send_keys(username)
        print('got user  ')
        sleep(1.1)

        password_field = WebDriverWait(self.wd,10).until(EC.presence_of_element_located((By.NAME,'password')))
        password_field.send_keys(pw)
        print('got password  ')
        sleep(2)

        login_button = WebDriverWait(self.wd,12).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
        login_button.click() 
        print('got login  ')
        sleep(7)      

    def scrap_post_comments(self,postId="CszJv_oLchO", save=True):

        self.wd.get(self.url + "p/" + postId + "/")

        more_to_load = True
        i = 0
        logging.warning('Scrap comment start')
        while more_to_load: 
            try:
                see_more_button = WebDriverWait(self.wd,12).until(
                                        EC.presence_of_element_located((
                                            By.XPATH, 
                                            "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul/li/div/button")))
                if see_more_button:
                    see_more_button.click()
                    i +=1 
                    logging.warning('Scrap comment on going')
                else:
                    comments = WebDriverWait(self.wd,10).until(
                                        EC.presence_of_element_located((
                                            By.XPATH,
                                            '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul')))

                    soup = BeautifulSoup(comments.get_attribute('outerHTML') , 'html.parser') 

                    more_to_load = False
                logging.warning('Scrap comment on going 2')
            except:
                logging.warning('Scrap comment failed')
                comments = WebDriverWait(self.wd,10).until(
                                        EC.presence_of_element_located((
                                            By.XPATH,
                                            '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul')))

                soup = BeautifulSoup(comments.get_attribute('outerHTML') , 'html.parser') 

                more_to_load = False

            sleep(1)

        logging.warning('Scrap comment finish')
        spans = soup.find_all('span', attrs={'class':'_aacl _aaco _aacu _aacx _aad7 _aade'})
        answers = [answer.getText().strip() for answer in spans]
        answers_df = pd.DataFrame({'answers':answers})
        logging.warning('Saving')
        if save:
            answers_df.to_csv(path_or_buf=f"./data/{postId}_comments.csv",index=False)
        logging.warning('Saved')
        return answers_df


