from macharonte.whatsapp.enums.browser import Browsers
from macharonte.whatsapp.enums.status import Status

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
from io import BytesIO

import os.path
import time
import ast


class WhatsAppClient:

    def __init__(self, browser: Browsers, profile_path: str = None):
        options = Options()

        if profile_path is not None:
            options.add_argument(r"user-data-dir=" + profile_path)

        if browser == Browsers.CHROME:
            self.__webdriver = webdriver.Chrome("C:\\Users\\Deepsamanta\\Desktop\\WhatsApp Tracker\\Selenium\\chromedriver.exe", chrome_options=options)

        self.__chat = None

        self.__enter_action = ActionChains(self.__webdriver)
        self.__enter_action.send_keys(Keys.ENTER)

        self.__esc_action = ActionChains(self.__webdriver)
        self.__esc_action.send_keys(Keys.ESCAPE)

        my_path = os.path.abspath(os.path.dirname(__file__))
        self.__path = os.path.join(my_path, "xpaths.cfg")

    def connect(self) -> bool:
        try:
            self.__webdriver.get("https://web.whatsapp.com")
            self.__wait = WebDriverWait(self.__webdriver, 5)
        except:
            return False
        return True

    def close(self) -> bool:
        try:
            self.__webdriver.quit()
        except:
            return False
        return True

    def minimize_window(self):
        self.__webdriver.minimize_window()

    def maximize_window(self):
        self.__webdriver.maximize_window()

    def is_logged(self) -> bool:
        try:
            self.__webdriver.find_element_by_xpath(
                self.__get_xpath("IS_LOGGED"))
        except:
            return False
        return True

    def save_qrcode(self, filename: str) -> bool:
        im = self.__get_img_by_variable("QR_CODE")

        if im != None:
            im.save(filename)
            return True
        return False

    def save_header(self, filename: str) -> bool:
        im = self.__get_img_by_variable("HEADER")

        if im != None:
            im.save(filename)
            return True
        return False

    def get_header(self) -> bool:
        im = self.__get_img_by_variable("HEADER")

        if im == None:
            return None

        width, height = im.size
        im = im.crop((0, 0, width - width * 0.5, height))

        b = BytesIO()
        im.save(b, "PNG")
        b.seek(0)
        return b

    def open_chat(self, target: str) -> bool:
        if self.__chat == target.lower():
            return True

        try:
            new_chat_title = self.__wait.until(EC.presence_of_element_located(
                (By.XPATH, self.__get_xpath("NEW_CHAT_BTN"))))
            new_chat_title.click()

            search_box = self.__wait.until(EC.presence_of_element_located(
                (By.XPATH, self.__get_xpath("SEARCH_AREA"))))
            search_box.send_keys(target)

            time.sleep(1)

            try:
                chat_found = self.__wait.until(EC.presence_of_element_located(
                    (By.XPATH, self.__get_xpath("CONTACT_LIST"))))

                self.__enter_action.perform()
                self.__chat = target.lower()

                time.sleep(2)

            except:
                self.__esc_action.perform()
                self.__esc_action.perform()
                print("Incorrect name, no chat found.")
                return False
        except Exception as e:
            print(e)
            return False
        return True

    def get_user_status(self, target: str) -> Status:
        if self.open_chat(target):
            try:
                element = self.__webdriver.find_element_by_xpath(
                    self.__get_xpath("USER_STATUS"))

                if element.text == Status.ONLINE.value:
                    return Status.ONLINE
                elif element.text == Status.IS_WRITING.value:
                    return Status.IS_WRITING
            except:
                return Status.OFFLINE
        return Status.NOT_DEFINED

    def send_message(self, target, message: str) -> bool:
        if self.open_chat(target) == False:
            return False

        try:
            self.__webdriver.switch_to_active_element().send_keys(message)
            self.__enter_action.perform()
        except:
            return False
        return True

    def __get_img_by_variable(self, variable_name: str) -> str:
        try:
            element = self.__webdriver.find_element_by_xpath(
                self.__get_xpath(variable_name))
            location = element.location
            size = element.size
            png = self.__webdriver.get_screenshot_as_png()

            im = Image.open(BytesIO(png))

            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']

            im = im.crop((left, top, right, bottom))
            return im
        except:
            return None

    def __get_xpath(self, variable_name: str) -> str:
        xpaths = ast.literal_eval(open(self.__path).read())
        return xpaths[variable_name]
