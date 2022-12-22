import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

from page.base.base_page import BasePage, BaseHandle


# 核对订单页面
class CheckOrderPage(BasePage):
    def __init__(self):
        super().__init__()
        self.address_iframe_title = By.CSS_SELECTOR, ".layui-layer-title"
        self.add_address_iframe = By.ID, "layui-layer-iframe1"
        self.consignee_name = By.NAME, "consignee"
        self.province_select = By.NAME, "province"
        self.city_select = By.NAME, "city"
        self.district_select = By.NAME, "district"
        self.twon_select = By.NAME, "twon"
        self.detailed_address = By.CSS_SELECTOR, ".re-no"
        self.phone_number = By.CSS_SELECTOR, ".wi40-BFB"
        self.save_address = By.CSS_SELECTOR, ".box-ok"
        self.submit_order = By.CSS_SELECTOR, ".Sub-orders"

    def find_address_iframe_title(self):
        return super().get_element(self.address_iframe_title)

    def find_add_address_iframe(self):
        return super().get_element(self.add_address_iframe)

    def find_consignee_name(self):
        return super().get_element(self.consignee_name)

    def find_province_select(self):
        return super().get_element(self.province_select)

    def find_city_select(self):
        return super().get_element(self.city_select)

    def find_district_select(self):
        return super().get_element(self.district_select)

    def find_twon_select(self):
        return super().get_element(self.twon_select)

    def find_detailed_address(self):
        return super().get_element(self.detailed_address)

    def find_phone_number(self):
        return super().get_element(self.phone_number)

    def find_save_address(self):
        return super().get_element(self.save_address)

    def find_submit_order(self):
        return super().get_element(self.submit_order)


class CheckOrderHandle(BaseHandle):
    def __init__(self):
        self.check_order_page = CheckOrderPage()

    def get_address_iframe_title(self):
        return self.check_order_page.find_address_iframe_title().text

    def switch_to_add_address_iframe(self, driver: WebDriver):
        driver.switch_to.frame(self.check_order_page.find_add_address_iframe())

    def input_consignee_name(self, name):
        super().input_text(self.check_order_page.find_consignee_name(), name)

    def select_province_by_visible_text(self, visible_text):
        super().select_option(self.check_order_page.find_province_select(), visible_text)

    def select_city_by_visible_text(self, visible_text):
        super().select_option(self.check_order_page.find_city_select(), visible_text)

    def select_district_by_visible_text(self, visible_text):
        super().select_option(self.check_order_page.find_district_select(), visible_text)

    def select_twon_by_visible_text(self, visible_text):
        super().select_option(self.check_order_page.find_twon_select(), visible_text)

    def input_detailed_address(self, detailed_address):
        super().input_text(self.check_order_page.find_detailed_address(), detailed_address)

    def input_phone_number(self, phone_number):
        super().input_text(self.check_order_page.find_phone_number(), phone_number)

    def click_save_address(self):
        self.check_order_page.find_save_address().click()

    def click_submit_order(self):
        self.check_order_page.find_submit_order().click()


class CheckOrderService:
    def __init__(self):
        self.check_order_handle = CheckOrderHandle()

    def get_address_iframe_title(self):
        return self.check_order_handle.get_address_iframe_title()

    def add_receiving_address_then_place_order(self, driver: WebDriver, name, province, city, district, twon,
                                               detailed_address, phone_number):
        # 进入添加收货地址的iframe
        self.check_order_handle.switch_to_add_address_iframe(driver)
        # 输入收获地址并保存
        self.check_order_handle.input_consignee_name(name)
        self.check_order_handle.select_province_by_visible_text(province)
        self.check_order_handle.select_city_by_visible_text(city)
        self.check_order_handle.select_district_by_visible_text(district)
        self.check_order_handle.select_twon_by_visible_text(twon)
        self.check_order_handle.input_detailed_address(detailed_address)
        self.check_order_handle.input_phone_number(phone_number)
        self.check_order_handle.click_save_address()
        time.sleep(3)  # 保存地址且识别出来需要时间
        # 返回原先的位置
        driver.switch_to.default_content()
        # 点击提交订单
        self.check_order_handle.click_submit_order()
