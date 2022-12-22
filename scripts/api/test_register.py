import pytest
import requests

from api.register_api import RegisterApi
from scripts import logger
from utils import get_data


# @pytest.mark.skip()
@pytest.mark.run(order=6)
class TestRegisterApi:
    def setup(self):
        self.session = requests.Session()
        self.register_api = RegisterApi()

    def teardown(self):
        if self.session:
            self.session.close()

    @pytest.mark.parametrize("username, code, password, password2, status, msg", get_data("api/register_fail.json"))
    def test_register(self, username, code, password, password2, status, msg):
        try:
            self.register_api.get_verify_code(self.session)
            response = self.register_api.register(self.session, username, code, password, password2)
            assert status == response.json().get("status")
            assert msg in response.json().get("msg")

        except Exception as e:
            logger.error("接口测试的注册失败测试出错了，原因：{}".format(e))
            raise
