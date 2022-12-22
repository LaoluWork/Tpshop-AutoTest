from selenium.webdriver.common.by import By

from page.base.base_page import BasePage, BaseHandle


# 对象层
class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        self.login_btn = By.CSS_SELECTOR, ".red"
        self.register_btn = By.XPATH, "//div[@class='fl nologin']/a[2]"
        self.quit_btn = By.XPATH, "//*[@title='退出']"
        self.search_input_box = By.CSS_SELECTOR, ".ecsc-search-input"
        self.search_btn = By.CSS_SELECTOR, ".ecsc-search-button"
        self.goods_item = By.CSS_SELECTOR, ".floor-goods-item"

    def find_login_btn(self):
        return super().get_element(self.login_btn)

    def find_register_btn(self):
        return super().get_element(self.register_btn)

    def find_quit_btn(self):
        return super().get_element(self.quit_btn)

    def find_search_input_box(self):
        return super().get_element(self.search_input_box)

    def find_search_btn(self):
        return super().get_element(self.search_btn)

    def find_goods_item(self):
        return super().get_element(self.goods_item)


# 操作层
class HomeHandle(BaseHandle):
    def __init__(self):
        self.home_page = HomePage()

    def click_login_btn(self):
        self.home_page.find_login_btn().click()

    def click_register_btn(self):
        self.home_page.find_register_btn().click()

    def click_quit_btn(self):
        self.home_page.find_quit_btn().click()

    def input_search_text(self, text):
        super().input_text(self.home_page.find_search_input_box(), text)

    def click_search_btn(self):
        self.home_page.find_search_btn().click()

    def click_goods_item(self):
        self.home_page.find_goods_item().click()


# 业务层
class HomeService:
    def __init__(self):
        self.home_handle = HomeHandle()

    def go_login_page(self):
        self.home_handle.click_login_btn()

    def go_register_page(self):
        self.home_handle.click_register_btn()

    def quit_login(self):
        self.home_handle.click_quit_btn()

    def search_goods(self, text):
        self.home_handle.input_search_text(text)
        self.home_handle.click_search_btn()

    def go_goods_item_detail(self):
        self.home_handle.click_goods_item()
