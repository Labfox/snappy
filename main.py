import random
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import htmlMagic


def login(driver, datapack, username, password):
    """
    :param driver: WebDriver instance used to interact with the web browser.
    :param datapack: A dictionary containing XPath selectors for various web elements required during the login process.
    :param username: Snapchat username used for login.
    :param password: Snapchat password used for login.
    :return: None
    """
    driver.get("https://web.snapchat.com")

    time.sleep(random.uniform(5, 7))

    form = driver.find_element(By.XPATH, datapack["login"]["input_form"])
    form.send_keys(username)
    form.send_keys(Keys.ENTER)

    time.sleep(random.uniform(5, 7))

    accept_all_cookies_button = driver.find_element(By.XPATH, datapack["login"]["essentials_only"])
    accept_all_cookies_button.click()

    password_form = driver.find_element(By.XPATH, datapack["login"]["password_form"])
    password_form.send_keys(password)
    password_form.send_keys(Keys.ENTER)

    time.sleep(random.uniform(5, 7))

    driver.find_element(By.XPATH, datapack["login"]["not_now"]).click()

    time.sleep(random.uniform(5, 7))

def listConversations(driver, datapack):
    """
    :param driver: WebDriver instance used to interact with the web browser.
    :param datapack: Dictionary containing XPath templates and other data configurations.
    :return: List of WebElement instances representing the conversations on the page.
    """
    return htmlMagic.interpret_conversations(driver.find_elements(By.XPATH, datapack["conversations"]["list_convs"]))


def getMessagesBacklog(driver, datapack):
    """
    :param driver: Selenium WebDriver instance used to interact with the web browser.
    :param datapack: Dictionary containing XPath configurations for locating elements.
    :return: List of web elements representing the message backlog.
    """
    return htmlMagic.extract_messages(driver.find_elements(By.XPATH, datapack["messages"]["list_messages"]))


def selectConversation(driver, datapack, name):
    """
    :param driver: The WebDriver instance used for browser automation.
    :param name: The name of the conversation to select.
    :param datapack: A dictionary containing the XPATH template for the conversation selection element.
    :return: None
    """
    driver.find_element(By.XPATH, datapack["conversations"]["select_conv"].format(name=name)).click()

def sendMessage(driver, datapack, message, cool_down=False):
    """
    :param driver: The WebDriver instance used to interact with the web browser.
    :param message: The message text to be sent.
    :param datapack: A dictionary containing data required for the function, including locators.
    :return: None
    """
    sendMsgElem: WebElement = driver.find_element(By.XPATH, datapack["messages"]["send_message"])
    if cool_down:
        for letter in message:
            sendMsgElem.send_keys(letter)
            time.sleep(random.uniform(0.005, 0.05))
    else:
        sendMsgElem.send_keys(message)
    sendMsgElem.send_keys(Keys.ENTER)



