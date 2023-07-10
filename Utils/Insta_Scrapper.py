from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep 
import pandas as pd

from bs4 import BeautifulSoup

class instaScrapper():
    """
    Class dealing with instagram interactions
    - login
    - comments scrapping
    """

    def __init__(self):
        self.wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wd.maximize_window()
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
        
        self.wd.get(self.url)
        self.wd.implicitly_wait(5)

        sleep(0.5)

        cookie_button = WebDriverWait(self.wd,15).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Autoriser tous les cookies']")))
        cookie_button.click() 

        sleep(0.9)

        username_field = WebDriverWait(self.wd,12).until(EC.presence_of_element_located((By.NAME,'username')))
        username_field.send_keys(username)

        sleep(1.1)

        password_field = WebDriverWait(self.wd,10).until(EC.presence_of_element_located((By.NAME,'password')))
        password_field.send_keys(pw)

        sleep(2)

        login_button = WebDriverWait(self.wd,12).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
        login_button.click() 

        sleep(7)      

    def scrap_post_comments(self,postId="CszJv_oLchO", save=True):

        self.wd.get(self.url + "p/" + postId + "/")

        more_to_load = True
        i = 0

        while more_to_load: 
            try:
                see_more_button = WebDriverWait(self.wd,12).until(
                                        EC.presence_of_element_located((
                                            By.XPATH, 
                                            "//*[name()='svg' and @aria-label='Charger d’autres commentaires']")))
                if see_more_button:
                    see_more_button.click()
                    i +=1 
                else:
                    comments = WebDriverWait(self.wd,10).until(
                                        EC.presence_of_element_located((
                                            By.XPATH,
                                            '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul')))

                    soup = BeautifulSoup(comments.get_attribute('outerHTML') , 'html.parser') 

                    more_to_load = False

            except:
                comments = WebDriverWait(self.wd,10).until(
                                        EC.presence_of_element_located((
                                            By.XPATH,
                                            '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul')))

                soup = BeautifulSoup(comments.get_attribute('outerHTML') , 'html.parser') 

                more_to_load = False

            sleep(1)

 
        spans = soup.find_all('span', attrs={'class':'_aacl _aaco _aacu _aacx _aad7 _aade'})
        answers = [answer.getText().strip() for answer in spans]
        answers_df = pd.DataFrame({'answers':answers})

        if save:
            answers_df.to_csv(path_or_buf=f"./data/{postId}_comments.csv",index=False)

        return answers_df


