from selenium.webdriver.common.by import By

from page.base.base_page import BasePage, BaseHandle


# 对象层
class SearchInfoPage(BasePage):
    def __init__(self):
        super().__init__()
        self.goods_a_label = By.CSS_SELECTOR, ".shop_name2 a"
        self.goods_not_exists_info = By.XPATH, "//ul/p"
        self.search_input_box = By.CSS_SELECTOR, ".ecsc-search-input"
        self.search_btn = By.CSS_SELECTOR, ".ecsc-search-button"

    def find_goods_a_label(self):
        return super().get_element(self.goods_a_label)

    def find_goods_not_exists_info(self):
        return super().get_element(self.goods_not_exists_info)

    def find_search_input_box(self):
        return super().get_element(self.search_input_box)

    def find_search_btn(self):
        return super().get_element(self.search_btn)


# 操作层
class SearchInfoHandle(BaseHandle):
    def __init__(self):
        self.search_info_page = SearchInfoPage()

    def get_goods_keys(self):
        return self.search_info_page.find_goods_a_label().text

    def click_goods_a_label(self):
        self.search_info_page.find_goods_a_label().click()

    def get_goods_not_exists_info(self):
        return self.search_info_page.find_goods_not_exists_info().text

    def input_search_goods(self, text):
        super().input_text(self.search_info_page.find_search_input_box(), text)

    def click_search_btn(self):
        self.search_info_page.find_search_btn().click()


# 业务层
class SearchInfoService:
    def __init__(self):
        self.search_info_handle = SearchInfoHandle()

    def get_goods_outline(self, case):
        # 商品搜索成功的测试用例
        if case == "success":
            return self.search_info_handle.get_goods_keys()
        # 搜索的商品不存在的情况
        else:
            return self.search_info_handle.get_goods_not_exists_info()

    def search_goods(self, text):
        self.search_info_handle.input_search_goods(text)
        self.search_info_handle.click_search_btn()

    def go_goods_detail(self):
        self.search_info_handle.click_goods_a_label()

