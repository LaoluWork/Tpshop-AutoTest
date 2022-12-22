from selenium.webdriver.common.by import By

from page.base.base_page import BasePage, BaseHandle


# 支付页面
class PayPage(BasePage):
    def __init__(self):
        super().__init__()
        self.tips_info = By.CSS_SELECTOR, ".erhuh h3"
        self.pay_way_radio = By.NAME, "pay_radio"
        self.pay_btn = By.CSS_SELECTOR, ".button-confirm-payment"
        self.order_id = By.CSS_SELECTOR, ".succ-p"

    def find_tips_info(self):
        return super().get_element(self.tips_info)

    def find_pay_way_radio(self):
        return super().get_elements(self.pay_way_radio)[1]

    def find_pay_btn(self):
        return super().get_element(self.pay_btn)

    def find_order_id(self):
        return super().get_element(self.order_id)


class PayHandle(BaseHandle):
    def __init__(self):
        self.pay_page = PayPage()

    def get_tips_info(self):
        return self.pay_page.find_tips_info().text

    def select_pay_way(self):
        self.pay_page.find_pay_way_radio().click()

    def click_pay_btn(self):
        self.pay_page.find_pay_btn().click()

    def get_order_id(self):
        return self.pay_page.find_order_id().text.split("：")[1].split("|")[0].strip()


class PayService:
    def __init__(self):
        self.pay_handle = PayHandle()

    def get_tips_info(self):
        return self.pay_handle.get_tips_info()

    def get_order_id(self):
        return self.pay_handle.get_order_id()

    def pay(self):
        self.pay_handle.select_pay_way()
        self.pay_handle.click_pay_btn()
