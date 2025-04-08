"""
SDESA Python库 - 统计模块

该模块包含SDESA的统计功能，用于收集和分析模拟结果。
"""

import numpy as np
import pandas as pd
from collections import defaultdict


class ActivityStatistics:
    """
    活动统计类
    
    用于收集和分析活动的统计数据，包括完成次数、等待时间和服务时间。
    
    属性:
        activity_id (str): 活动ID
        completion_count (int): 完成次数
        waiting_times (list): 等待时间列表
        service_times (list): 服务时间列表
    """
    
    def __init__(self, activity_id, completion_count=0, waiting_times=None, service_times=None):
        """
        初始化活动统计
        
        参数:
            activity_id (str): 活动ID
            completion_count (int, optional): 完成次数，默认为0
            waiting_times (list, optional): 等待时间列表，默认为None
            service_times (list, optional): 服务时间列表，默认为None
        """
        self.activity_id = activity_id
        self.completion_count = completion_count
        self.waiting_times = waiting_times or []
        self.service_times = service_times or []
    
    def calculate_average_waiting_time(self):
        """
        计算平均等待时间
        
        返回:
            float: 平均等待时间
        """
        if not self.waiting_times:
            return 0.0
        return np.mean(self.waiting_times)
    
    def calculate_average_service_time(self):
        """
        计算平均服务时间
        
        返回:
            float: 平均服务时间
        """
        if not self.service_times:
            return 0.0
        return np.mean(self.service_times)
    
    def calculate_total_time(self):
        """
        计算总时间（等待时间 + 服务时间）
        
        返回:
            float: 总时间
        """
        return self.calculate_average_waiting_time() + self.calculate_average_service_time()
    
    def calculate_waiting_time_percentiles(self, percentiles=[25, 50, 75, 90, 95]):
        """
        计算等待时间百分位数
        
        参数:
            percentiles (list, optional): 百分位数列表，默认为[25, 50, 75, 90, 95]
        
        返回:
            dict: 百分位数字典，键为百分位数，值为对应的等待时间
        """
        if not self.waiting_times:
            return {p: 0.0 for p in percentiles}
        return {p: np.percentile(self.waiting_times, p) for p in percentiles}
    
    def calculate_service_time_percentiles(self, percentiles=[25, 50, 75, 90, 95]):
        """
        计算服务时间百分位数
        
        参数:
            percentiles (list, optional): 百分位数列表，默认为[25, 50, 75, 90, 95]
        
        返回:
            dict: 百分位数字典，键为百分位数，值为对应的服务时间
        """
        if not self.service_times:
            return {p: 0.0 for p in percentiles}
        return {p: np.percentile(self.service_times, p) for p in percentiles}
    
    def to_dict(self):
        """
        转换为字典
        
        返回:
            dict: 活动统计字典
        """
        return {
            'activity_id': self.activity_id,
            'completion_count': self.completion_count,
            'average_waiting_time': self.calculate_average_waiting_time(),
            'average_service_time': self.calculate_average_service_time(),
            'total_time': self.calculate_total_time(),
            'waiting_time_percentiles': self.calculate_waiting_time_percentiles(),
            'service_time_percentiles': self.calculate_service_time_percentiles()
        }
    
    def __str__(self):
        """返回活动统计的字符串表示"""
        return f"ActivityStatistics(activity_id={self.activity_id}, completion_count={self.completion_count}, avg_waiting_time={self.calculate_average_waiting_time():.2f}, avg_service_time={self.calculate_average_service_time():.2f})"


class ResourceStatistics:
    """
    资源统计类
    
    用于收集和分析资源的统计数据，包括忙碌时间段和空闲时间段。
    
    属性:
        resource_id (str): 资源ID
        busy_periods (list): 忙碌时间段列表，每个时间段为(开始时间, 结束时间)
        idle_periods (list): 空闲时间段列表，每个时间段为(开始时间, 结束时间)
    """
    
    def __init__(self, resource_id, busy_periods=None, idle_periods=None):
        """
        初始化资源统计
        
        参数:
            resource_id (str): 资源ID
            busy_periods (list, optional): 忙碌时间段列表，默认为None
            idle_periods (list, optional): 空闲时间段列表，默认为None
        """
        self.resource_id = resource_id
        self.busy_periods = busy_periods or []
        self.idle_periods = idle_periods or []
    
    def calculate_utilization_rate(self, total_time=None):
        """
        计算利用率
        
        参数:
            total_time (float, optional): 总时间，默认为None
        
        返回:
            float: 利用率（0-1之间的值）
        """
        if not self.busy_periods:
            return 0.0
        
        total_busy_time = sum(end - start for start, end in self.busy_periods)
        
        if total_time is None:
            # 如果没有提供总时间，使用最后一个忙碌时间段的结束时间
            total_time = max(end for _, end in self.busy_periods)
        
        return total_busy_time / total_time if total_time > 0 else 0.0
    
    def calculate_average_busy_period(self):
        """
        计算平均忙碌时间段长度
        
        返回:
            float: 平均忙碌时间段长度
        """
        if not self.busy_periods:
            return 0.0
        return np.mean([end - start for start, end in self.busy_periods])
    
    def calculate_average_idle_period(self):
        """
        计算平均空闲时间段长度
        
        返回:
            float: 平均空闲时间段长度
        """
        if not self.idle_periods:
            return 0.0
        return np.mean([end - start for start, end in self.idle_periods])
    
    def calculate_busy_time_percentiles(self, percentiles=[25, 50, 75, 90, 95]):
        """
        计算忙碌时间段长度百分位数
        
        参数:
            percentiles (list, optional): 百分位数列表，默认为[25, 50, 75, 90, 95]
        
        返回:
            dict: 百分位数字典，键为百分位数，值为对应的忙碌时间段长度
        """
        if not self.busy_periods:
            return {p: 0.0 for p in percentiles}
        busy_times = [end - start for start, end in self.busy_periods]
        return {p: np.percentile(busy_times, p) for p in percentiles}
    
    def to_dict(self, total_time=None):
        """
        转换为字典
        
        参数:
            total_time (float, optional): 总时间，默认为None
        
        返回:
            dict: 资源统计字典
        """
        return {
            'resource_id': self.resource_id,
            'utilization_rate': self.calculate_utilization_rate(total_time),
            'average_busy_period': self.calculate_average_busy_period(),
            'average_idle_period': self.calculate_average_idle_period(),
            'busy_time_percentiles': self.calculate_busy_time_percentiles()
        }
    
    def __str__(self):
        """返回资源统计的字符串表示"""
        return f"ResourceStatistics(resource_id={self.resource_id}, utilization_rate={self.calculate_utilization_rate():.2f}, avg_busy_period={self.calculate_average_busy_period():.2f})"


class SimulationStatistics:
    """
    模拟统计类
    
    用于收集和分析模拟的统计数据，包括活动统计和资源统计。
    
    属性:
        activity_statistics (dict): 活动统计字典，键为活动ID，值为ActivityStatistics对象
        resource_statistics (dict): 资源统计字典，键为资源ID，值为ResourceStatistics对象
        total_simulation_time (float): 总模拟时间
    """
    
    def __init__(self, activity_statistics=None, resource_statistics=None, total_simulation_time=0):
        """
        初始化模拟统计
        
        参数:
            activity_statistics (dict, optional): 活动统计字典，默认为None
            resource_statistics (dict, optional): 资源统计字典，默认为None
            total_simulation_time (float, optional): 总模拟时间，默认为0
        """
        self.activity_statistics = {}
        if activity_statistics:
            for activity_id, stats in activity_statistics.items():
                if isinstance(stats, dict):
                    self.activity_statistics[activity_id] = ActivityStatistics(
                        activity_id=activity_id,
                        completion_count=stats.get('completion_count', 0),
                        waiting_times=stats.get('waiting_times', []),
                        service_times=stats.get('service_times', [])
                    )
                else:
                    self.activity_statistics[activity_id] = stats
        
        self.resource_statistics = {}
        if resource_statistics:
            for resource_id, stats in resource_statistics.items():
                if isinstance(stats, dict):
                    self.resource_statistics[resource_id] = ResourceStatistics(
                        resource_id=resource_id,
                        busy_periods=stats.get('busy_periods', []),
                        idle_periods=stats.get('idle_periods', [])
                    )
                else:
                    self.resource_statistics[resource_id] = stats
        
        self.total_simulation_time = total_simulation_time
    
    def get_activity_statistics(self, activity_id):
        """
        获取活动统计
        
        参数:
            activity_id (str): 活动ID
        
        返回:
            ActivityStatistics: 活动统计对象
        """
        return self.activity_statistics.get(activity_id)
    
    def get_resource_statistics(self, resource_id):
        """
        获取资源统计
        
        参数:
            resource_id (str): 资源ID
        
        返回:
            ResourceStatistics: 资源统计对象
        """
        return self.resource_statistics.get(resource_id)
    
    def calculate_overall_resource_utilization(self):
        """
        计算总体资源利用率
        
        返回:
            float: 总体资源利用率（0-1之间的值）
        """
        if not self.resource_statistics:
            return 0.0
        
        utilization_rates = [stats.calculate_utilization_rate(self.total_simulation_time) 
                            for stats in self.resource_statistics.values()]
        return np.mean(utilization_rates)
    
    def calculate_bottleneck_activities(self):
        """
        计算瓶颈活动
        
        返回:
            list: 瓶颈活动列表，按等待时间降序排序
        """
        if not self.activity_statistics:
            return []
        
        activities = [(activity_id, stats.calculate_average_waiting_time()) 
                     for activity_id, stats in self.activity_statistics.items()]
        activities.sort(key=lambda x: x[1], reverse=True)
        return activities
    
    def calculate_critical_resources(self):
        """
        计算关键资源
        
        返回:
            list: 关键资源列表，按利用率降序排序
        """
        if not self.resource_statistics:
            return []
        
        resources = [(resource_id, stats.calculate_utilization_rate(self.total_simulation_time)) 
                    for resource_id, stats in self.resource_statistics.items()]
        resources.sort(key=lambda x: x[1], reverse=True)
        return resources
    
    def to_dict(self):
        """
        转换为字典
        
        返回:
            dict: 模拟统计字典
        """
        return {
            'activity_statistics': {activity_id: stats.to_dict() for activity_id, stats in self.activity_statistics.items()},
            'resource_statistics': {resource_id: stats.to_dict(self.total_simulation_time) for resource_id, stats in self.resource_statistics.items()},
            'total_simulation_time': self.total_simulation_time,
            'overall_resource_utilization': self.calculate_overall_resource_utilization(),
            'bottleneck_activities': self.calculate_bottleneck_activities(),
            'critical_resources': self.calculate_critical_resources()
        }
    
    def export_to_csv(self, filename_prefix):
        """
        导出统计数据到CSV
        
        参数:
            filename_prefix (str): 文件名前缀
        
        返回:
            list: 导出的文件列表
        """
        files = []
        
        # 导出活动统计
        activity_data = []
        for activity_id, stats in self.activity_statistics.items():
            activity_data.append({
                'activity_id': activity_id,
                'completion_count': stats.completion_count,
                'average_waiting_time': stats.calculate_average_waiting_time(),
                'average_service_time': stats.calculate_average_service_time(),
                'total_time': stats.calculate_total_time()
            })
        
        if activity_data:
            activity_df = pd.DataFrame(activity_data)
            activity_file = f"{filename_prefix}_activity_statistics.csv"
            activity_df.to_csv(activity_file, index=False)
            files.append(activity_file)
        
        # 导出资源统计
        resource_data = []
        for resource_id, stats in self.resource_statistics.items():
            resource_data.append({
                'resource_id': resource_id,
                'utilization_rate': stats.calculate_utilization_rate(self.total_simulation_time),
                'average_busy_period': stats.calculate_average_busy_period(),
                'average_idle_period': stats.calculate_average_idle_period()
            })
        
        if resource_data:
            resource_df = pd.DataFrame(resource_data)
            resource_file = f"{filename_prefix}_resource_statistics.csv"
            resource_df.to_csv(resource_file, index=False)
            files.append(resource_file)
        
        # 导出总体统计
        summary_data = {
            'total_simulation_time': [self.total_simulation_time],
            'overall_resource_utilization': [self.calculate_overall_resource_utilization()]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_file = f"{filename_prefix}_summary_statistics.csv"
        summary_df.to_csv(summary_file, index=False)
        files.append(summary_file)
        
        return files
    
    def export_to_json(self, filename):
        """
        导出统计数据到JSON
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 导出的文件名
        """
        import json
        
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
        
        return filename
    
    def __str__(self):
        """返回模拟统计的字符串表示"""
        return f"SimulationStatistics(activities={len(self.activity_statistics)}, resources={len(self.resource_statistics)}, total_time={self.total_simulation_time:.2f})"
