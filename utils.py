"""
SDESA Python库 - 工具模块

该模块包含SDESA的辅助工具，如随机数生成、数据导入导出等。
"""

import numpy as np
import random
import math


class RandomGenerator:
    """
    随机数生成器类
    
    提供各种概率分布的随机数生成功能。
    """
    
    @staticmethod
    def uniform(min_val, max_val):
        """
        生成均匀分布随机数
        
        参数:
            min_val (float): 最小值
            max_val (float): 最大值
        
        返回:
            float: 均匀分布随机数
        """
        return random.uniform(min_val, max_val)
    
    @staticmethod
    def normal(mean, std):
        """
        生成正态分布随机数
        
        参数:
            mean (float): 均值
            std (float): 标准差
        
        返回:
            float: 正态分布随机数
        """
        return random.normalvariate(mean, std)
    
    @staticmethod
    def triangular(min_val, mode, max_val):
        """
        生成三角分布随机数
        
        参数:
            min_val (float): 最小值
            mode (float): 众数
            max_val (float): 最大值
        
        返回:
            float: 三角分布随机数
        """
        return random.triangular(min_val, mode, max_val)
    
    @staticmethod
    def exponential(lambd):
        """
        生成指数分布随机数
        
        参数:
            lambd (float): 速率参数
        
        返回:
            float: 指数分布随机数
        """
        return random.expovariate(lambd)
    
    @staticmethod
    def beta(alpha, beta, min_val=0, max_val=1):
        """
        生成Beta分布随机数
        
        参数:
            alpha (float): Alpha参数
            beta (float): Beta参数
            min_val (float, optional): 最小值，默认为0
            max_val (float, optional): 最大值，默认为1
        
        返回:
            float: Beta分布随机数
        """
        # 生成[0,1]范围内的Beta分布随机数
        value = random.betavariate(alpha, beta)
        
        # 缩放到[min_val, max_val]范围
        return min_val + (max_val - min_val) * value
    
    @staticmethod
    def set_seed(seed):
        """
        设置随机数种子
        
        参数:
            seed (int): 随机数种子
        """
        random.seed(seed)
        np.random.seed(seed)


class Logger:
    """
    日志记录器类
    
    提供日志记录功能。
    
    属性:
        level (str): 日志级别，可以是'DEBUG', 'INFO', 'WARNING', 'ERROR'
        log_file (str): 日志文件路径，如果为None则输出到控制台
    """
    
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    
    def __init__(self, level=INFO, log_file=None):
        """
        初始化日志记录器
        
        参数:
            level (str, optional): 日志级别，默认为INFO
            log_file (str, optional): 日志文件路径，默认为None
        """
        self.level = level
        self.log_file = log_file
        self.level_order = {
            self.DEBUG: 0,
            self.INFO: 1,
            self.WARNING: 2,
            self.ERROR: 3
        }
    
    def _should_log(self, message_level):
        """
        检查是否应该记录日志
        
        参数:
            message_level (str): 消息级别
        
        返回:
            bool: 如果应该记录则为True，否则为False
        """
        return self.level_order.get(message_level, 0) >= self.level_order.get(self.level, 0)
    
    def _write_log(self, message_level, message):
        """
        写入日志
        
        参数:
            message_level (str): 消息级别
            message (str): 消息内容
        """
        import datetime
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] [{message_level}] {message}"
        
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(log_message + '\n')
        else:
            print(log_message)
    
    def debug(self, message):
        """
        记录调试信息
        
        参数:
            message (str): 消息内容
        """
        if self._should_log(self.DEBUG):
            self._write_log(self.DEBUG, message)
    
    def info(self, message):
        """
        记录信息
        
        参数:
            message (str): 消息内容
        """
        if self._should_log(self.INFO):
            self._write_log(self.INFO, message)
    
    def warning(self, message):
        """
        记录警告
        
        参数:
            message (str): 消息内容
        """
        if self._should_log(self.WARNING):
            self._write_log(self.WARNING, message)
    
    def error(self, message):
        """
        记录错误
        
        参数:
            message (str): 消息内容
        """
        if self._should_log(self.ERROR):
            self._write_log(self.ERROR, message)


class DataImporter:
    """
    数据导入器类
    
    提供从CSV、JSON等格式导入数据的功能。
    """
    
    @staticmethod
    def import_from_csv(filename):
        """
        从CSV导入数据
        
        参数:
            filename (str): CSV文件路径
        
        返回:
            pandas.DataFrame: 导入的数据
        """
        import pandas as pd
        return pd.read_csv(filename)
    
    @staticmethod
    def import_from_json(filename):
        """
        从JSON导入数据
        
        参数:
            filename (str): JSON文件路径
        
        返回:
            dict: 导入的数据
        """
        import json
        with open(filename, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def import_from_excel(filename, sheet_name=0):
        """
        从Excel导入数据
        
        参数:
            filename (str): Excel文件路径
            sheet_name (str or int, optional): 工作表名称或索引，默认为0
        
        返回:
            pandas.DataFrame: 导入的数据
        """
        import pandas as pd
        return pd.read_excel(filename, sheet_name=sheet_name)


# 创建全局随机数生成器实例
random_generator = RandomGenerator()
