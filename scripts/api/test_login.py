import allure
import pytest
import requests

from api.login_api import LoginApi
from scripts import logger
from utils import get_data


# @pytest.mark.skip()
@pytest.mark.run(order=7)
class TestLoginApi:
    def setup_class(self):
        self.login_api = LoginApi()
        self.session = requests.Session()

    def teardown_class(self):
        if self.session:
            self.session.close()

    @pytest.mark.parametrize("username, password, code, status, status_code, content_type, msg",
                             get_data("api/login_case.json"))
    def test_login(self, username, password, code, status, status_code, content_type, msg):
        try:
            logger.info("准备输入登录的接口测试用例：username={}，password={}，code={}".format(username, password, code))
            # 先获取验证码来断言
            response = self.login_api.get_verify_code(self.session)
            assert status_code == response.status_code
            assert content_type in response.headers.get("Content-Type")

            # 登录断言
            response = self.login_api.login(self.session, username, password, code)
            assert status_code == response.status_code
            assert status == response.json().get("status")
            assert msg in response.json().get("msg")

        except Exception as e:
            # 写入日志
            logger.error("登录成功的接口测试出错了，原因是：{}".format(e))
            # 抛出异常，否则全部都显示通过了
            raise
