import time

import allure
import pytest

from page.back.index_page import IndexService
from page.front.check_order_page import CheckOrderService
from page.front.goods_detail import GoodsDetailService
from page.front.home_page import HomeService
from page.front.login_page import LoginService
from page.front.mine_page import MineService
from page.front.my_cart_page import MyCartService
from page.front.pay_page import PayService
from scripts import logger
from utils import DriverUtils, DBUtils, login_in_back


@pytest.mark.skip()
@pytest.mark.run(order=5)
class TestPlaceOrder:
    @classmethod
    def setup_class(cls):
        cls.home_service = HomeService()
        cls.goods_detail_service = GoodsDetailService()
        cls.my_cart_service = MyCartService()
        cls.login_service = LoginService()
        cls.mine_service = MineService()
        cls.check_order_service = CheckOrderService()
        cls.pay_service = PayService()
        cls.index_service = IndexService()
        cls.__driver = DriverUtils.get_driver()

    def setup(self):
        self.__driver.get("http://localhost")

    @staticmethod
    def teardown_class():
        DriverUtils.quit_driver()

    # 通过两种方式购买且下单的通用方法
    def go_to_check_order_page(self, case):
        # 先登录，然后回到首页(登录只需要一次，所以参数是第一个时才需要登录)
        if case == "goods_detail":
            self.home_service.go_login_page()
            # 登录一个纯净的账号
            self.login_service.login("13800138001", "123456", "8888")
            self.mine_service.go_to_home_page()
        self.home_service.go_goods_item_detail()
        # 直接在商品详情页就购买下单
        if case == "goods_detail":
            self.goods_detail_service.buy_now()
        else:  # 添加购物车后再在购物车页面下单
            self.goods_detail_service.add_to_cart(self.__driver)
            self.goods_detail_service.go_my_cart()
            self.my_cart_service.go_to_pay()

    # @pytest.mark.skip()
    # 未登录的状态下，结算购物车里的商品
    @allure.severity(allure.severity_level.NORMAL)
    def test_place_order_fail_in_myCart_when_not_logged_in(self):
        try:
            self.home_service.go_goods_item_detail()
            self.goods_detail_service.add_to_cart(self.__driver)
            self.goods_detail_service.go_my_cart()
            self.my_cart_service.go_to_pay()
            # 一定要加等待时间，因为未登录就结算需要经过一个提示页面才跳转到登录页
            time.sleep(5)
            assert "/User/login.html" in self.__driver.current_url
        except Exception as e:
            logger.error("未登录状态下单结算购物车的测试用例执行失败了，原因是：{}".format(e))
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "未登录状态下单结算购物车的测试用例执行失败",
                          allure.attachment_type.PNG)
            raise

    # @pytest.mark.skip()
    # 未登录的状态下，在某个商品详情页直接点击购买
    @allure.severity(allure.severity_level.NORMAL)
    def test_place_order_fail_in_goods_detail_when_not_logged_in(self):
        try:
            self.home_service.go_goods_item_detail()
            iframe_title = self.goods_detail_service.buy_now("未登录")
            assert "登陆TPshop网" in iframe_title
        except Exception as e:
            logger.error("未登录状态直接下单购买商品的测试用例执行失败了， 原因时：{}".format(e))
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "未登录状态直接下单购买商品的测试用例执行失败",
                          allure.attachment_type.PNG)
            raise

    # @pytest.mark.skip()
    # 已登录但未填写地址，下单时需要跳出添加收获地址的页面
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", ["goods_detail", "my_cart"])
    def test_place_order_fail_when_no_address(self, case):
        try:
            self.go_to_check_order_page(case)
            address_iframe_title = self.check_order_service.get_address_iframe_title()
            if case == "my_cart": # 最后一次的测试用例执行完后，退出登录状态，为下面的测试用例提供好环境
                self.__driver.get("http://localhost")
                self.home_service.quit_login()

            assert "添加收货地址" in address_iframe_title
        except Exception as e:
            logger.error("已登录但未填写收货地址下单的测试用例执行失败了， 原因时：{}".format(e))
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "未登录状态直接购买商品的测试用例执行失败",
                          allure.attachment_type.PNG)
            raise

    # 下单成功的业务流程
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("case", ["goods_detail", "my_cart"])
    def test_place_order_success(self, case):
        try:
            self.go_to_check_order_page(case)
            # 输入收获地址，然后提交订单
            self.check_order_service.add_receiving_address_then_place_order(self.__driver, "二师兄", "广东省", "广州市", "天河区",
                                                                            "沙河街道", "001号", "13800138001")
            assert "订单提交成功，请您尽快付款" in self.pay_service.get_tips_info()
            # 支付订单
            self.pay_service.pay()
            # 获取订单编号
            order_id = self.pay_service.get_order_id()
            assert "订单提交成功，我们将在第一时间给你发货" in self.pay_service.get_tips_info()
            # 删除地址，保持测试用例的可重复执行性
            DBUtils.exe_sql(
                "delete from tp_user_address where user_id = (select user_id from tp_users where mobile = '13800138001')"
            )
            # 进入后台管理系统，并获取最新的订单id号用来比较；同样的，仅第一次需要登录
            if case == "goods_detail":
                login_in_back()
            else:  # 第二次就直接在地址栏输入网站进入即可，session作用
                self.__driver.get("http://localhost/index.php/Admin/Index/index")

            assert self.index_service.get_latest_order_id() == order_id

        except Exception as e:
            logger.error("下单成功的测试用例执行失败了， 原因时：{}".format(e))
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "下单成功的测试用例执行失败",
                          allure.attachment_type.PNG)
            raise
