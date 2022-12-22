import time

from selenium.webdriver.common.by import By

from page.base.base_page import BasePage, BaseHandle


class MyCartPage(BasePage):
    def __init__(self):
        super().__init__()
        self.single_item_title = By.CSS_SELECTOR, ".gwc-ys-pp a"
        self.single_item_unit_price = By.XPATH, "//td[contains(@id, 'goods_price')]"
        self.single_item_buy_count = By.XPATH, "//input[contains(@name, 'changeQuantity')]"
        self.single_item_total_price = By.XPATH, "//td[contains(@id, 'market_price')]"
        self.items_total_fee = By.CSS_SELECTOR, "#total_fee"
        self.buy_now = By.CSS_SELECTOR, ".gwc-qjs"

    def find_single_item_title(self) -> list:
        return super().get_elements(self.single_item_title)

    def find_single_item_unit_price(self) -> list:
        return super().get_elements(self.single_item_unit_price)

    def find_single_item_buy_count(self) -> list:
        return super().get_elements(self.single_item_buy_count)

    def find_single_item_total_price(self):
        return super().get_elements(self.single_item_total_price)

    def find_items_total_fee(self):
        return super().get_element(self.items_total_fee)

    def find_buy_now(self):
        return super().get_element(self.buy_now)


class MyCartHandle(BaseHandle):
    def __init__(self):
        self.my_cart_page = MyCartPage()

    # 获取最新添加的商品title
    def get_newest_item_title(self):
        return self.my_cart_page.find_single_item_title()[0].text

    # 获取最新添加的商品的购买单价
    def get_newest_item_unit_price(self):
        return float(self.my_cart_page.find_single_item_unit_price()[1].text.replace('￥', ''))

    # 获取最新添加的商品购买数量
    def get_newest_item_buy_count(self):
        return self.my_cart_page.find_single_item_buy_count()[0].get_attribute('value')

    # 获取最新添加的商品购买总价
    def get_newest_item_total_price(self):
        return float(self.my_cart_page.find_single_item_total_price()[0].text.replace('￥', ''))

    # 获取购物车里被选择的所有商品的价格总和
    def get_items_total_fee(self):
        time.sleep(5)
        return float(self.my_cart_page.find_items_total_fee().text.replace('￥', ''))

    def click_buy_now(self):
        self.my_cart_page.find_buy_now().click()


# 业务层
class MyCartService:
    def __init__(self):
        self.my_cart_handle = MyCartHandle()

    def get_newest_item_info(self):
        actual_goods_info = {
            "goods_title": self.my_cart_handle.get_newest_item_title(),
            "unit_price": self.my_cart_handle.get_newest_item_unit_price(),
            "buy_count": self.my_cart_handle.get_newest_item_buy_count(),
            "total_price": self.my_cart_handle.get_newest_item_total_price(),
            "all_goods_total_fee": self.my_cart_handle.get_items_total_fee()
        }
        return actual_goods_info

    def go_to_pay(self):
        self.my_cart_handle.click_buy_now()
