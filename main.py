from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# from urllib.request import urlopen
import json


path = "/Users/swapn/Downloads/chromedriver_mac64.exe"

# Creating a webdriver instance
driver = webdriver.Chrome(path)


def login():
    #personal linkedin login code
    #create a seperate login file and keep credentials
    login = open('login.txt')
    line = login.readlines()

    email = line[0]
    password = line[1]

    driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    em = driver.find_element(by=By.ID, value="username")
    em.send_keys(email)
    pswrd = driver.find_element(by=By.ID, value="password")
    pswrd.send_keys(password)
    loginButton = driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginButton.click()
    time.sleep(3)

def redirectAndScroll(targetUrl):
    #function to get the required profile and scroll to the bottom so page loads
    time.sleep(1)
    driver.get(targetUrl)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    source = BeautifulSoup(driver.page_source, "html.parser")
    return source

def extractProfileIntro(source):
    intro = source.find('div', {'class': 'pv-text-details__left-panel'})
    location = source.find('div', {'class': 'pv-text-details__left-panel mt2'})
    about = source.find('div', {'class': 'pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center'})
    # print(intro)
    name_loc = intro.find("h1")
    name = name_loc.get_text().strip()
    title_block = intro.find('div', {'class': 'text-body-medium break-words'})
    title = title_block.get_text().strip()
    location_block = location.find('span', {'class': 'text-body-small inline t-black--light break-words'})
    loc = location_block.get_text().strip()

    about_block = about.find('span', {'class': 'visually-hidden'})
    abt = about_block.get_text().strip()
    print(name, title, loc)
    print(abt)
    # print("---------")
    # print(location)


login()
targetUrl = "https://www.linkedin.com/in/prathamesh-verlekar/"
source = redirectAndScroll(targetUrl)
extractProfileIntro(source)