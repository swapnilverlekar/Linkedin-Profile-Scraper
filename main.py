from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

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



def extractProfile(source):
    #extracting intro
    info = []
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
    #extracting about me
    # about_block = about.find('span', {'class': 'visually-hidden'})
    abt = about.get_text().strip()
    # print(name, title, loc)
    # print(abt)

    experiences = source.find_all('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
    profile_details = []
    for x in experiences[1:]:
        alltext = x.getText().split('\n')
        profile_details.append([x for x in alltext if len(x)>=3])
        # print(alltext)
    # for i in profile_details:
    #     print(i)

    info.append([name])
    info.append([title])
    info.append([loc])
    info.append([abt])
    info.append(profile_details)
    return info

def convertToCSV(info):
    #converting data to csv file
    column_names = ["Full Name", "Title", "Current Location", 'About Section', 'Profile Information']

    df = pd.DataFrame(info, column_names)

    df_T = df.transpose()
    df_T.to_csv('data.csv', index=False)


login()
targetUrl = "https://www.linkedin.com/in/satyanadella/"
source = redirectAndScroll(targetUrl)
info = extractProfile(source)
convertToCSV(info)
print("**************** Linkedin Profile Extraction Complete ****************")
