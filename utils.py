import json
import os

import allure
from selenium.webdriver.common.by import By

import config

import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from config import BASE_DIR


# 浏览器驱动的工具类
class DriverUtils:
    __driver = None

    @classmethod
    def get_driver(cls) -> WebDriver:
        if cls.__driver is None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("excludeSwitches",
                                                   ['ignore-certificate-errors', 'ignore-ssl-errors'])
            cls.__driver = webdriver.Chrome(options=chrome_options)
            cls.__driver.maximize_window()

        return cls.__driver

    @classmethod
    def quit_driver(cls):
        if cls.__driver is not None:
            cls.__driver.quit()
            cls.__driver = None  # 将driver彻底置为空值


# 从json文件中提取测试数据
def get_data(filename):
    file_path = BASE_DIR + os.sep + "data" + os.sep + filename
    # 定义空列表 组装测试数据
    result = []
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for d in data.values():
            result.append(tuple(d.values()))

        return result


# 操作MySQL数据库的通用类
class DBUtils:
    __conn = None
    __cursor = None

    # 获取数据库连接
    @classmethod
    def get_conn(cls):
        if cls.__conn is None:
            cls.__conn = pymysql.connect(host=config.MySQL_host,
                                         port=config.MySQL_port,
                                         user=config.MySQL_user,
                                         password=config.MySQL_password,
                                         database=config.MySQL_database)

        return cls.__conn

    # 获取游标对象
    @classmethod
    def get_cursor(cls):
        if cls.__cursor is None:
            cls.__cursor = cls.get_conn().cursor()

        return cls.__cursor

    # 通用执行sql的方法
    @classmethod
    def exe_sql(cls, sql: str):
        try:
            cursor = cls.get_cursor()
            cursor.execute(sql)
            # 区分开查询和增删改
            if sql.split()[0].lower() == "select":
                # 查询操作，将所有数据返回
                return cursor.fetchall()
            else:
                # 是增删改操作，那就提交事务
                cls.__conn.commit()
                # 返回影响的行数
                return cursor.rowcount

        except Exception as e:
            # 出现异常，事务回滚
            cls.__conn.rollback()
            config.GetLogger.get_logger().error("执行SQL语句出现异常，原因为：{}".format(e))
            allure.attach(DriverUtils.get_driver().get_screenshot_as_png(), "执行SQL语句失败", allure.attachment_type.PNG)
            raise

        finally:
            # 关闭游标和连接对象
            cls.__close_cursor()
            cls.__close_conn()

    @classmethod
    def __close_cursor(cls):
        if cls.__cursor:
            cls.__cursor.close()
            cls.__cursor = None

    @classmethod
    def __close_conn(cls):
        if cls.__conn:
            cls.__conn.close()
            cls.__conn = None


# 登录后台管理系统的方法
def login_in_back():
    driver = DriverUtils.get_driver()
    driver.get("http://localhost/index.php/Admin/Admin/login.html")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "vertify").send_keys("8888")
    driver.find_element(By.NAME, "submit").click()
