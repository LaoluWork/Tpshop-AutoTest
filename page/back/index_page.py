from selenium.webdriver.common.by import By

from page.base.base_page import BasePage, BaseHandle
from utils import DriverUtils


class IndexPage(BasePage):
    def __init__(self):
        super().__init__()
        self.system = By.XPATH, "//*[@data-param='system']/a"
        self.member = By.XPATH, "//div[@id='admincpNavTabs_system']/dl[2]/dt/a"
        self.latest_register_phone = By.XPATH, "//tr[1]/td[10]/div"
        self.content_iframe = By.CSS_SELECTOR, "#workspace"
        self.shop = By.XPATH, "//*[@data-param='shop']/a"
        self.order = By.XPATH, "//div[@id='admincpNavTabs_shop']/dl[2]/dt/a"
        self.latest_order_id = By.XPATH, "//tr[1]/td[2]/div"

    def find_system(self):
        return super().get_element(self.system)

    def find_member(self):
        return super().get_element(self.member)

    def find_latest_register_phone(self):
        return super().get_element(self.latest_register_phone)

    def find_content_iframe(self):
        return super().get_element(self.content_iframe)

    def find_shop(self):
        return super().get_element(self.shop)

    def find_order(self):
        return super().get_element(self.order)

    def find_latest_order_id(self):
        return super().get_element(self.latest_order_id)


class IndexHandle(BaseHandle):
    def __init__(self):
        self.index_page = IndexPage()

    def click_system(self):
        self.index_page.find_system().click()

    def click_member(self):
        self.index_page.find_member().click()

    def get_latest_register_phone(self):
        return self.index_page.find_latest_register_phone().text

    def switch_to_content_iframe(self):
        DriverUtils.get_driver().switch_to.frame(self.index_page.find_content_iframe())

    def click_shop(self):
        self.index_page.find_shop().click()

    def click_order(self):
        self.index_page.find_order().click()

    def get_latest_order_id(self):
        return self.index_page.find_latest_order_id().text


class IndexService:
    def __init__(self):
        self.index_handle = IndexHandle()

    # 从index页面进入系统再点击会员，然后获取第一行的注册号码返回
    def get_latest_register_phone(self):
        self.index_handle.click_system()
        self.index_handle.click_member()
        # 要先切换到会员页面内嵌的iframe
        self.index_handle.switch_to_content_iframe()
        return self.index_handle.get_latest_register_phone()

    # 从index页面进入商城再点击订单，然后获取第一行的订单id返回
    def get_latest_order_id(self):
        self.index_handle.click_shop()
        self.index_handle.click_order()
        # 切换到订单页面的iframe
        self.index_handle.switch_to_content_iframe()
        return self.index_handle.get_latest_order_id()
