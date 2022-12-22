import allure
import pytest

from page.front.goods_detail import GoodsDetailService
from page.front.home_page import HomeService
from page.front.my_cart_page import MyCartService
from page.front.search_info_page import SearchInfoService
from scripts import logger
from utils import DriverUtils, get_data


@pytest.mark.skip()
@pytest.mark.run(order=4)
class TestAddToCart:
    # 统计购物车页多种商品的总计
    __all_goods_total_fee = 0.0

    @classmethod
    def setup_class(cls):
        cls.home_service = HomeService()
        cls.goods_detail_service = GoodsDetailService()
        cls.search_info_service = SearchInfoService()
        cls.my_cart_service = MyCartService()
        cls.driver = DriverUtils.get_driver()

    def setup(self):
        self.driver.get("http://localhost")

    @staticmethod
    def teardown_class():
        DriverUtils.quit_driver()

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("target_goods, buy_count", get_data("ui/add_to_cart_case.json"))
    def test_add_to_cart(self, target_goods, buy_count):
        try:
            # 直接在首页搜索进入某个商品的详情页
            self.home_service.search_goods(target_goods)
            self.search_info_service.go_goods_detail()

            # 设置购买数量，添加到购物车，同时查询得到当前商品的简要信息
            self.goods_detail_service.edit_buy_count(buy_count)
            self.goods_detail_service.add_to_cart(self.driver)
            expect_goods_info = self.goods_detail_service.get_goods_general_info()

            TestAddToCart.__all_goods_total_fee += expect_goods_info["total_price"]

            # 进入我的购物车页面，判断对应商品是否正确地被添加
            self.goods_detail_service.go_my_cart()
            actual_goods_info = self.my_cart_service.get_newest_item_info()

            assert expect_goods_info["goods_title"] in actual_goods_info["goods_title"]
            assert expect_goods_info["unit_price"] == actual_goods_info["unit_price"]
            assert expect_goods_info["buy_count"] == actual_goods_info["buy_count"]
            assert expect_goods_info["total_price"] == actual_goods_info["total_price"]
            assert self.__all_goods_total_fee == actual_goods_info["all_goods_total_fee"]

        except Exception as e:
            logger.error("添加商品到购物车的测试用例执行失败了，原因是：{}".format(e))
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "添加商品到购物车的测试用例执行失败", allure.attachment_type.PNG)
            raise
