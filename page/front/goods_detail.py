import time

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from page.base.base_page import BasePage, BaseHandle


# 对象层
class GoodsDetailPage(BasePage):
    def __init__(self):
        super().__init__()
        self.add_to_cart = By.CSS_SELECTOR, ".addcar"
        self.my_cart = By.XPATH, "//span[text()='我的购物车']"
        self.buy_now = By.CSS_SELECTOR, "#join_cart_now"
        self.reduce_goods_count = By.XPATH, "//li/div/a[1]"
        self.add_goods_count = By.XPATH, "//li/div/a[2]"
        self.buy_count = By.CSS_SELECTOR, ".buyNum"
        self.goods_title = By.CSS_SELECTOR, ".detail-ggsl h1"
        self.goods_unit_price = By.CSS_SELECTOR, "#goods_price"
        self.iframe = By.CSS_SELECTOR, "#layui-layer-iframe1"
        self.continue_shopping = By.CSS_SELECTOR, ".add-cart-btn a"
        self.login_iframe_title = By.CSS_SELECTOR, ".layui-layer-title b"

    def find_add_to_cart(self):
        return super().get_element(self.add_to_cart)

    def find_my_cart(self):
        time.sleep(2)
        return super().get_element(self.my_cart)

    def find_buy_now(self):
        return super().get_element(self.buy_now)

    def find_reduce_goods_count(self):
        return super().get_element(self.reduce_goods_count)

    def find_add_goods_count(self):
        return super().get_element(self.add_goods_count)

    def find_buy_count(self):
        return super().get_element(self.buy_count)

    def find_goods_title(self):
        return super().get_element(self.goods_title)

    def find_goods_unit_price(self):
        return super().get_element(self.goods_unit_price)

    def find_iframe(self):
        return super().get_element(self.iframe)

    def find_continue_shopping(self):
        return super().get_element(self.continue_shopping)

    def find_login_iframe_title(self):
        return super().get_element(self.login_iframe_title)


# 操作层
class GoodsDetailHandle(BaseHandle):
    def __init__(self):
        self.goods_detail_page = GoodsDetailPage()

    def click_add_to_cart(self):
        self.goods_detail_page.find_add_to_cart().click()

    def click_my_cart(self):
        self.goods_detail_page.find_my_cart().click()

    def click_buy_now(self):
        self.goods_detail_page.find_buy_now().click()

    def click_reduce_goods_count(self):
        self.goods_detail_page.find_reduce_goods_count().click()

    def click_add_goods_count(self):
        self.goods_detail_page.find_add_goods_count().click()

    def get_buy_count(self):
        return self.goods_detail_page.find_buy_count().get_attribute('value')

    def edit_buy_count(self, count):
        # clear()操作完失去焦点后会出错
        # super().input_text(self.goods_detail_page.find_buy_count(), count)

        # 删除和输入属于一次性操作，中途不会触发失去焦点的校验
        self.goods_detail_page.find_buy_count().send_keys(Keys.BACK_SPACE, count)

    def get_goods_title(self):
        return self.goods_detail_page.find_goods_title().text

    def get_goods_unit_price(self):
        return float(self.goods_detail_page.find_goods_unit_price().text.replace('￥', ''))

    def switch_to_iframe(self, driver: WebDriver):
        driver.switch_to.frame(self.goods_detail_page.find_iframe())

    def click_continue_shopping(self):
        self.goods_detail_page.find_continue_shopping().click()

    def get_login_iframe_title(self):
        return self.goods_detail_page.find_login_iframe_title().text


# 业务层
class GoodsDetailService:
    def __init__(self):
        self.goods_detail_handle = GoodsDetailHandle()

    def go_my_cart(self):
        self.goods_detail_handle.click_my_cart()

    def add_to_cart(self, driver: WebDriver):
        self.goods_detail_handle.click_add_to_cart()
        self.goods_detail_handle.switch_to_iframe(driver)
        self.goods_detail_handle.click_continue_shopping()
        # 切换回原来的页面控制
        driver.switch_to.default_content()

    def buy_now(self, case="已登录"):
        self.goods_detail_handle.click_buy_now()
        # 在当前商品详情页，如果处于未登录的状态，点击立即购买会弹出登录框
        if case == "未登录":
            return self.goods_detail_handle.get_login_iframe_title()

    def edit_buy_count(self, count):
        if count > 0:
            self.goods_detail_handle.edit_buy_count(count)

    # 返回当前商品的简要信息：标题，单价，购买数量
    def get_goods_general_info(self):
        expect_goods_info = {
            "goods_title": self.goods_detail_handle.get_goods_title(),
            "unit_price": self.goods_detail_handle.get_goods_unit_price(),
            "buy_count": self.goods_detail_handle.get_buy_count(),
            "total_price": self.goods_detail_handle.get_goods_unit_price() * float(
                self.goods_detail_handle.get_buy_count())
        }
        return expect_goods_info
