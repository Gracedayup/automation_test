import logging
from common import project_path
from common.handle_data import HandleFileData
import datetime
import os


class HandleLog(object):
    def __init__(self):
        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.log_file_name = os.path.join(project_path.logs_path, ''.join([date, '.log']))
        self.log_formatter = "%(asctime)s-[%(levelname)s]-[msg]:%(message)s [Lineno]:%(lineno)d module-%(module)s"
        self.log_level = HandleFileData("config\config.yml").read_yaml()["logger"]["level"]

    def handle_log(self):
        logger = logging.getLogger("log")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            # 文件日志
            file_handler = logging.FileHandler(self.log_file_name, encoding="utf-8")
            # 设置文件日志的格式
            file_handler.setFormatter(logging.Formatter(self.log_formatter))
            # 控制台日志
            console_handler = logging.StreamHandler()
            # 设置控制台日志的格式
            console_handler.setFormatter(logging.Formatter(self.log_formatter))
            # 设置日志级别
            if self.log_level == "DEBUG":
                file_handler.setLevel(logging.DEBUG)
                console_handler.setLevel(logging.DEBUG)
            elif self.log_level == "CRITICAL":
                file_handler.setLevel(logging.CRITICAL)
                console_handler.setLevel(logging.CRITICAL)
            elif self.log_level == "ERROR":
                file_handler.setLevel(logging.ERROR)
                console_handler.setLevel(logging.ERROR)
            elif self.log_level == "WARNING":
                file_handler.setLevel(logging.WARNING)
                console_handler.setLevel(logging.WARNING)
            elif self.log_level == "INFO":
                file_handler.setLevel(logging.INFO)
                console_handler.setLevel(logging.INFO)
                # 将文件日志控制器加入到日志对象
            logger.addHandler(file_handler)
            # 将控制台日志控制器加入到日志对象
            logger.addHandler(console_handler)
            return logger


logger = HandleLog().handle_log()

if __name__ == '__main__':
    logger.info("测试")
    logger.error("测试")
    logger.critical("测试")
