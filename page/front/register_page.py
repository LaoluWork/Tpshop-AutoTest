import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from page.base.base_page import BasePage, BaseHandle
from utils import DriverUtils


class RegisterPage(BasePage):
    def __init__(self):
        super().__init__()
        self.username = By.ID, "username"
        self.password = By.ID, "password"
        self.confirm_password = By.ID, "password2"
        self.verify_code = By.NAME, "verify_code"
        self.register_btn = By.CSS_SELECTOR, ".regbtn"
        self.msg = By.CSS_SELECTOR, ".layui-layer-content"

    def find_username(self) -> WebElement:
        return super().get_element(self.username)

    def find_password(self) -> WebElement:
        return super().get_element(self.password)

    def find_confirm_password(self) -> WebElement:
        return super().get_element(self.confirm_password)

    def find_verify_code(self) -> WebElement:
        return super().get_element(self.verify_code)

    def find_register_btn(self) -> WebElement:
        return super().get_element(self.register_btn)

    def find_msg(self):
        return super().get_element(self.msg)


# 操作层  --> 对元素操作
class RegisterHandle(BaseHandle):
    def __init__(self):
        self.login_page = RegisterPage()

    @allure.step(title="输入注册用户名")
    def input_username(self, username):
        super().input_text(self.login_page.find_username(), username)

    @allure.step(title="输入注册密码")
    def input_password(self, password):
        super().input_text(self.login_page.find_password(), password)

    @allure.step(title="输入注册密码")
    def input_confirm_password(self, confirm_password):
        super().input_text(self.login_page.find_confirm_password(), confirm_password)

    @allure.step("输入注册验证码")
    def input_verify_code(self, code):
        super().input_text(self.login_page.find_verify_code(), code)

    @allure.step("点击注册")
    def click_register_btn(self):
        self.login_page.find_register_btn().click()
        # 因为提交的数据需要校验，所以强制等待后再进行下一步操作
        time.sleep(1)

    @allure.step("获取弹窗消息")
    def get_msg(self):
        return self.login_page.find_msg().text


# 业务层  --> 将多个操作结合，完成一个功能
class RegisterService:
    def __init__(self):
        self.register_handle = RegisterHandle()

    def register(self, username, password, confirm_password, code):
        self.register_handle.input_username(username)
        self.register_handle.input_password(password)
        self.register_handle.input_confirm_password(confirm_password)
        self.register_handle.input_verify_code(code)
        self.register_handle.click_register_btn()


    def get_msg(self):
        msg = self.register_handle.get_msg()
        # 获取完弹窗消息之后，需要刷新页面，否则无法进行下一次的输入测试
        DriverUtils.get_driver().refresh()
        return msg
