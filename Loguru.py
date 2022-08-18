import os
import time
import sys
from loguru import logger

class MyLogger:
    def __init__(self):
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(sys.stdout,
                        format="<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> "  # 颜色>时间
                               "[<level>{level}</level>] " # 日志等级
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                               ":<cyan>{line}</cyan> | "  # 行号
                               "<level>{message}</level>",  # 日志内容
                        )
        # 创建文件目录
        current_work_dir = os.path.dirname(__file__)
        logs_dir = current_work_dir+"/log"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = "log-%s.log" % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        # 输出到文件的格式,注释下面的add',则关闭日志写入
        self.logger.add(logfilepath, level='DEBUG',
                        format='[{time:YYYY-MM-DD HH:mm:ss}] '  # 时间
                               "[{level}] " # 日志等级
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               '{module}.{function}:{line} -- {message}',  # 模块名.方法名:行号
                        rotation="00:00", backtrace=True)
    def get_logger(self):
        return self.logger

my_logger = MyLogger().get_logger()