import json
import random
import threading
import time
import queue

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from . import htmlMagic

class SnapchatCredentials:
    """
        class SnapchatCredentials:
            A class to represent Snapchat user credentials.

            Attributes:
                username (str): The Snapchat username.
                password (str): The Snapchat password.

            Methods:
                __init__(self, username, password):
                    Initializes a SnapchatCredentials object with username and password.

            __init__(username, password):
                Initializes the SnapchatCredentials with provided username and password.

                Arguments:
                    username (str): The Snapchat username.
                    password (str): The Snapchat password.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

class SnapchatClient:
    """
        class SnapchatClient:
    def __init__(self, driver, credentials: SnapchatCredentials, datapack: dict = None):
        """
    def __init__(self, driver, credentials:SnapchatCredentials, datapack: dict = None):
        """
        :param driver: The WebDriver instance used for automated browser interactions.
        :param credentials: An instance of SnapchatCredentials containing the username and password.
        :param datapack: A dictionary containing data pack information (default is None). If not provided, it will be generated using the class methods.
        """
        self.driver = driver
        if datapack is None:
            self.datapack = self.getDatapackFromTitle(self.getDatapackIdentifier())
        else:
            self.datapack = datapack
        self.username = credentials.username
        self.password = credentials.password
        self.login(self.username, self.password)
        self._lastConversations = self.listConversations()
        self.event_queue = queue.Queue()
        self.eventTickThread = threading.Thread(target=self._eventTick)
        self.eventTickThread.start()

    def _eventTick(self):
        newconvs = self.listConversations()

        if self._lastConversations != newconvs:
            for conversation in newconvs:
                if conversation not in self._lastConversations:
                    self.event_queue.put({"event": "newConversation", "conversation": conversation})
        self._lastConversations = newconvs

    def getDatapackFromTitle(self, title):
        """
        :param title: The title of the datapack to retrieve.
        :return: The datapack associated with the given title.
        """
        list = json.load(open("datapacks/by/title.json", "r"))
        return json.load(open("datapacks/" + list[title], "r"))

    def getDatapackIdentifier(self):
        """
        Fetches the title of the Snapchat homepage.

        :return: The title of the Snapchat homepage.
        """
        self.driver.get("https://www.snapchat.com")
        time.sleep(random.uniform(1, 2))
        return self.driver.title

    def login(self, username, password):
        """
        :param username: The username for the Snapchat account.
        :param password: The password for the Snapchat account.
        :return: None
        """

        self.driver.get("https://web.snapchat.com")

        time.sleep(random.uniform(5, 7))

        form = self.driver.find_element(By.XPATH, self.datapack["login"]["input_form"])
        form.send_keys(username)
        form.send_keys(Keys.ENTER)

        time.sleep(random.uniform(5, 7))

        accept_all_cookies_button = self.driver.find_element(By.XPATH, self.datapack["login"]["essentials_only"])
        accept_all_cookies_button.click()

        password_form = self.driver.find_element(By.XPATH, self.datapack["login"]["password_form"])
        password_form.send_keys(password)
        password_form.send_keys(Keys.ENTER)

        time.sleep(random.uniform(5, 7))

        self.driver.find_element(By.XPATH, self.datapack["login"]["not_now"]).click()

        time.sleep(random.uniform(5, 7))

    def listConversations(self):
        """
        Fetches and interprets the list of conversations available.

        :return: A list of interpreted conversations from the web driver.
        """
        return htmlMagic.interpret_conversations(self.driver.find_elements(By.XPATH, self.datapack["conversations"]["list_convs"]))


    def getMessagesBacklog(self, conversation: htmlMagic.Conversation):
        """
        Extracts and returns the list of messages from the web page.

        :return: List of extracted messages.
        """
        self.selectConversation(conversation)
        time.sleep(random.uniform(1, 2))
        messages =  htmlMagic.extract_messages(self.driver.find_elements(By.XPATH, self.datapack["messages"]["list_messages"]))
        time.sleep(random.uniform(1, 2))
        self.selectConversation(conversation)
        time.sleep(random.uniform(1, 2))

        return messages


    def selectConversation(self, conversation:htmlMagic.Conversation):
        """
        :param conversation: The conversation object to be selected, containing conversation details.
        :return: None
        """
        self.driver.find_element(By.XPATH, self.datapack["conversations"]["select_conv"].format(name=conversation.title)).click()

    def sendMessage(self, conversation:htmlMagic.Conversation, message, cool_down=True):
        """
        :param message: The message text to be sent.
        :param cool_down: Simulate human typing ?
        :return: None
        """
        self.selectConversation(conversation)
        time.sleep(random.uniform(1, 2))

        sendMsgElem: WebElement = self.driver.find_element(By.XPATH, self.datapack["messages"]["send_message"])
        if cool_down:
            for letter in message:
                sendMsgElem.send_keys(letter)
                time.sleep(random.uniform(0.005, 0.05))
        else:
            sendMsgElem.send_keys(message)
        sendMsgElem.send_keys(Keys.ENTER)

        time.sleep(random.uniform(1, 2))
        self.selectConversation(conversation)
        time.sleep(random.uniform(1, 2))

