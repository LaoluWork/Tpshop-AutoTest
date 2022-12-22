import time

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from typing import List

from config import BASE_DIR
from utils import DriverUtils


# 基本页面，其他页面继承之后就可以使用通用的方法和属性等
class BasePage:
    def __init__(self):
        # 获取浏览器驱动对象，提供给后面的页面使用
        self.driver = DriverUtils.get_driver()

    # 获取一个元素的公用方法
    def get_element(self, location: tuple) -> WebElement:
        # 使用显示等待来寻找元素对象
        wait = WebDriverWait(self.driver, 10, 1)
        return wait.until(lambda x: x.find_element(*location))

    # 获取一组元素的公用方法
    def get_elements(self, location: tuple) -> List[WebElement]:
        # 使用显示等待来寻找元素对象
        wait = WebDriverWait(self.driver, 10, 1)
        return wait.until(lambda x: x.find_elements(*location))


# 基本的操作层类，其他具体的页面操作层类继承之后就可以使用通用的方法和属性等
class BaseHandle:

    # 通用的对元素输入框输入信息的方法
    @staticmethod
    def input_text(element: WebElement, text):
        # 先清空原本可能留存的信息
        element.clear()
        element.send_keys(text)

    # 根据可选的文本内容对元素选择框进行选择的方法
    @staticmethod
    def select_option(element: WebElement, visible_text):
        select = Select(element)
        # 根据该商城系统的性能，添加强制等待时间，因为请求和响应都需要时间
        time.sleep(3)
        select.select_by_visible_text(visible_text)
