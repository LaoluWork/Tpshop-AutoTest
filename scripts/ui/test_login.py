import time

import allure
import pytest

from page.front.home_page import HomeService
from page.front.login_page import LoginService
from page.front.mine_page import MineService
from scripts import logger
from utils import DriverUtils, get_data


@pytest.mark.skip()
@pytest.mark.run(order=2)
class TestLogin:
    @classmethod
    def setup_class(cls):
        cls.home_service = HomeService()
        cls.login_service = LoginService()
        cls.mine_service = MineService()

    def setup(self):
        DriverUtils.get_driver().get("http://localhost")
        # 从首页进入登录页面
        self.home_service.go_login_page()

    @staticmethod
    def teardown_class():
        DriverUtils.quit_driver()

    # 登录失败的测试方法
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username, password, code, expect", get_data("ui/login_fail_case.json"))
    def test_login_fail(self, username, password, code, expect):
        logger.info("准备输入登录失败的用例：username={}，password={}，code={}".format(username, password, code))
        try:
            self.login_service.login(username, password, code)
            # 填入登录信息，并获取弹窗消息
            text = self.login_service.get_msg()
            assert expect in text
        except Exception as e:
            # 写入日志
            logger.error("登录失败的ui测试出错了，原因是：{}".format(e))
            # 使用allure来截图
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "登录失败的ui测试出错", allure.attachment_type.PNG)
            # 抛出异常
            raise

    # 登录成功的测试方法
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("username, password, code, expect", get_data("ui/login_success_case.json"))
    def test_login_success(self, username, password, code, expect):
        logger.info("准备输入登录成功的用例：username={}，password={}，code={}".format(username, password, code))
        try:
            self.login_service.login(username, password, code)
            # 因为服务器返回相应需要时间，所以这里使用强制等待
            time.sleep(2)
            current_username = self.mine_service.get_current_username()
            # 退出个人主页，为下一次输入登录案例准备
            self.mine_service.login_out()
            assert expect == current_username
        except Exception as e:
            # 写入日志
            logger.error("登录成功的ui测试出错了，原因是：{}".format(e))
            # 使用allure来截图
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "登录成功的ui测试出错", allure.attachment_type.PNG)
            # 抛出异常
            raise
