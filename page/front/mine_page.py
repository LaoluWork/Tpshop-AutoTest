from selenium.webdriver.common.by import By

from page.base.base_page import BasePage, BaseHandle
from page.front.home_page import HomeService


class MinePage(BasePage):
    def __init__(self):
        super().__init__()
        self.current_user = By.CSS_SELECTOR, ".mu-m-phone"
        self.quit_btn = By.XPATH, "//*[@title='退出']"
        self.back_to_home = By.CSS_SELECTOR, ".home"

    def find_current_user(self):
        return super().get_element(self.current_user)

    def find_quit_btn(self):
        return super().get_element(self.quit_btn)

    def find_back_to_home(self):
        return super().get_element(self.back_to_home)


class MineHandle(BaseHandle):
    def __init__(self):
        self.mine_page = MinePage()

    def get_current_user(self):
        return self.mine_page.find_current_user().text

    def click_quit_btn(self):
        self.mine_page.find_quit_btn().click()

    def click_back_to_home(self):
        self.mine_page.find_back_to_home().click()


class MineService:
    def __init__(self):
        self.mine_handle = MineHandle()

    def get_current_username(self):
        return self.mine_handle.get_current_user()

    def login_out(self):
        self.mine_handle.click_quit_btn()

    def go_to_home_page(self):
        self.mine_handle.click_back_to_home()
