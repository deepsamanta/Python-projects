from selenium import webdriver
from selenium.webdriver import common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

opt = Options()
opt.add_argument(
    r"user-data-dir=C:\\Users\\Deepsamanta\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

browser = webdriver.Chrome(
    "C:\\Users\\Deepsamanta\\Desktop\\WhatsApp Tracker\\Selenium\\chromedriver.exe", options=opt)
browser.get("https://google.com",)

wait = WebDriverWait(browser, 5)
search_bar = wait.until(EC.presence_of_element_located((
    By.XPATH, "//body/div[1]/div[3]/form[1]/div[1]/div[1]/div[1]/div[1]/div[2]/input[1]")))

# search_bar = browser.find_element_by_xpath(
#     "//body/div[1]/div[3]/form[1]/div[1]/div[1]/div[1]/div[1]/div[2]/input[1]")
search_bar.send_keys("WhatsApp Web")

enter_action = ActionChains(browser)
enter_action.send_keys(Keys.ENTER)
enter_action.perform()

# whatsapp_link = browser.find_element_by_xpath(
#     "//body/div[@id='main']/div[@id='cnt']/div[@id='rcnt']/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/h3[1]")
whatsapp_link = wait.until(EC.presence_of_element_located((
    By.XPATH,  "//body/div[@id='main']/div[@id='cnt']/div[@id='rcnt']/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/h3[1]")))
whatsapp_link.click()
# C:\Users\Deepsamanta\AppData\Local\Google\Chrome\User Data\Default
