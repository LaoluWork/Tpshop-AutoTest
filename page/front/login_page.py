import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from page.base.base_page import BasePage, BaseHandle
from utils import DriverUtils


class LoginPage(BasePage):
    def __init__(self):
        super().__init__()
        self.username = By.ID, "username"
        self.password = By.ID, "password"
        self.verify_code = By.ID, "verify_code"
        self.login_btn = By.CSS_SELECTOR, ".J-login-submit"
        self.msg = By.CSS_SELECTOR, ".layui-layer-content"

    def find_username(self) -> WebElement:
        return super().get_element(self.username)

    def find_password(self) -> WebElement:
        return super().get_element(self.password)

    def find_verify_code(self) -> WebElement:
        return super().get_element(self.verify_code)

    def find_login_btn(self) -> WebElement:
        return super().get_element(self.login_btn)

    def find_msg(self):
        return super().get_element(self.msg)


# 操作层  --> 对元素操作
class LoginHandle(BaseHandle):
    def __init__(self):
        self.login_page = LoginPage()

    @allure.step(title="输入用户名")
    def input_username(self, username):
        super().input_text(self.login_page.find_username(), username)

    @allure.step(title="输入密码")
    def input_password(self, password):
        super().input_text(self.login_page.find_password(), password)

    @allure.step("输入验证码")
    def input_verify_code(self, code):
        super().input_text(self.login_page.find_verify_code(), code)

    @allure.step("点击登录")
    def click_login_btn(self):
        self.login_page.find_login_btn().click()
        # 因为提交的数据需要校验，所以强制等待后再进行下一步操作
        time.sleep(1)

    @allure.step("获取弹窗消息")
    def get_msg(self):
        return self.login_page.find_msg().text


# 业务层  --> 将多个操作结合，完成一个功能
class LoginService:
    def __init__(self):
        self.login_handle = LoginHandle()

    def login(self, username, password, code):
        self.login_handle.input_username(username)
        self.login_handle.input_password(password)
        self.login_handle.input_verify_code(code)
        self.login_handle.click_login_btn()

    def get_msg(self):
        msg = self.login_handle.get_msg()
        # 获取完弹窗消息之后，需要刷新页面，否则无法进行下一次的输入测试
        DriverUtils.get_driver().refresh()
        return msg
