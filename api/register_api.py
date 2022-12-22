from requests import Session, Response


class RegisterApi:
    def __init__(self):
        self.url_register = "http://localhost/index.php/Home/user/reg.html"
        self.url_verify = "http://localhost/index.php/Home/User/verify/type/user_reg.html"

    def get_verify_code(self, session: Session):
        return session.get(self.url_verify)

    def register(self, session: Session, username, code, password, password2) -> Response:
        register_data = {
            "username": username,
            "code": code,
            "password": password,
            "password2": password2
        }
        return session.post(self.url_register, data=register_data)
