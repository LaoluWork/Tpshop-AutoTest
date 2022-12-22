import allure
import pytest

from page.front.home_page import HomeService
from page.front.search_info_page import SearchInfoService
from scripts import logger
from utils import DriverUtils, get_data


# @pytest.mark.skip()
@pytest.mark.run(order=3)
class TestSearchInfo:
    __count = 0

    @classmethod
    def setup_class(cls):
        cls.home_service = HomeService()
        cls.search_info_service = SearchInfoService()
        cls.driver = DriverUtils.get_driver()

        cls.driver.get("http://localhost")

    @staticmethod
    def teardown_class():
        DriverUtils.quit_driver()

    # 搜索模块的测试方法
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("target_goods, expect_info, case", get_data("ui/search_info_case.json"))
    def test_search_info(self, target_goods, expect_info, case):
        try:
            # 第一次搜索直接在首页搜索，之后就在搜索页搜索
            if TestSearchInfo.__count < 1:
                self.home_service.search_goods(target_goods)
                TestSearchInfo.__count += 1
            else:
                self.search_info_service.search_goods(target_goods)
                TestSearchInfo.__count += 1

            actual_info = self.search_info_service.get_goods_outline(case)
            assert expect_info in actual_info

        except Exception as e:
            logger.error("搜索商品的测试用例失败了，原因是：{}".format(e))
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "搜索商品的测试用例失败了",
                          allure.attachment_type.PNG)
            raise
