import logging.handlers

import os

# 用当前的绝对路径作为基本路径，是以'/'分隔的
BASE_DIR = os.path.dirname(__file__)

MySQL_host = "localhost"
MySQL_port = 3306
MySQL_user = "root"
MySQL_password = "root"
MySQL_database = "tpshop2.0"


# 配置日志器
class GetLogger:
    __logger = None

    # 获取日志器的方法
    @classmethod
    def get_logger(cls):
        if cls.__logger is None:
            cls.__logger = logging.getLogger()
            cls.__logger.setLevel(logging.INFO)
            log_path = BASE_DIR + "/log/tpshop.log"
            # 获取日志处理器，将日志信息写到指定目录下
            fh = logging.handlers.TimedRotatingFileHandler(log_path,
                                                           when="midnight",
                                                           interval=1,
                                                           backupCount=7,
                                                           encoding="utf-8")

            fh.setLevel(logging.INFO)
            # 获取格式器
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            fm = logging.Formatter(fmt)
            # 将格式器添加到处理器中
            fh.setFormatter(fm)
            # 将处理器添加到日志器中
            cls.__logger.addHandler(fh)
            # 返回日志器
        return cls.__logger
