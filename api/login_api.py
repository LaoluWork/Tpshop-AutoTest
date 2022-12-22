from requests import Response, Session


class LoginApi:
    def __init__(self):
        self.url_verify = "http://localhost/index.php?m=Home&c=User&a=verify"
        self.url_login = "http://localhost/index.php?m=Home&c=User&a=do_login"

    # 获取验证码接口
    def get_verify_code(self, session: Session) -> Response:
        return session.get(self.url_verify)

    # 登录接口
    def login(self, session: Session, username, password, code) -> Response:
        login_data = {
            "username": username,
            "password": password,
            "verify_code": code
        }

        return session.post(url=self.url_login, data=login_data)
