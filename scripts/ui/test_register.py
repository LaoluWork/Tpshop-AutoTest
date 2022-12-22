import time

import allure
import pytest

from page.back.index_page import IndexService
from page.front.home_page import HomeService
from page.front.register_page import RegisterService
from scripts import logger
from utils import DriverUtils, get_data, DBUtils, login_in_back


@pytest.mark.skip()
@pytest.mark.run(order=1)
class TestRegister:
    @classmethod
    def setup_class(cls):
        cls.home_service = HomeService()  # tpshop主页面
        cls.register_service = RegisterService()  # tpshop的注册页面
        cls.index_service = IndexService()  # 后台系统的首页

    @staticmethod
    def teardown_class():
        DriverUtils.quit_driver()

    def setup(self):
        # 每次执行方法前都需要重新进入商城首页，然后点击注册按钮
        DriverUtils.get_driver().get("http://localhost")
        self.home_service.go_register_page()

    # 注册成功的测试用例
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("username, password, confirm_password, code", get_data("ui/register_success.json"))
    def test_register_success(self, username, password, confirm_password, code):
        try:
            self.register_service.register(username, password, confirm_password, code)
            # 退出登录，相当于删除session，防止同一个driver对象下再次打开首页时处于登录状态，导致无法再次进入注册页
            self.home_service.quit_login()
            # 注册完之后，退出driver，登录后台系统查看是否注册的号码也存在，同时也查询数据库是否也已经插入
            login_in_back()  # 先登录进后台
            back_phone = self.index_service.get_latest_register_phone()  # 获取后台的第一条手机号
            db_phone = DBUtils.exe_sql("select * from tp_users where mobile = " + username)
            assert username == back_phone  # 校验后台与注册数据是否相同
            assert db_phone is not None  # 校验数据库中是否已经插入相对应的用户数据
            # 断言成功之后，要删除刚刚注册的数据，从而保证数据的可重复执行
            count = DBUtils.exe_sql("delete from tp_users where mobile = " + username)
            assert count

        except Exception as e:
            # 写入日志
            logger.error("注册成功的ui测试失败了，原因是：{}".format(e))
            # 使用allure来截图
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "注册成功的ui测试失败", allure.attachment_type.PNG)
            # 抛出异常
            raise

