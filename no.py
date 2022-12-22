from selenium.webdriver.common.by import By

from page.back.index_page import IndexService
from utils import DriverUtils, login_in_back

# driver = DriverUtils.get_driver()
# driver.get("http://localhost")
# ele = driver.find_element(By.CSS_SELECTOR, ".goods-pic")
# print(ele.text)
# DriverUtils.quit_driver()
login_in_back()
service = IndexService()
print(service.get_latest_order_id())
# print(service.get_latest_register_phone())
DriverUtils.quit_driver()
