from requests import options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import EdgeOptions, ChromeOptions
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

url = "http://localhost:4444/wd/hub"

desired_capabilities = DesiredCapabilities.EDGE

conn = RemoteConnection(
    remote_server_addr=url
)

options = ChromeOptions()

driver = WebDriver(
    command_executor=url,
    options=options
)