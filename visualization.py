"""
SDESA Python库 - 可视化模块

该模块包含SDESA的可视化功能，用于可视化模拟过程和结果。
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class GanttChart:
    """
    甘特图类
    
    用于绘制活动甘特图，显示活动的开始时间、持续时间和资源使用情况。
    """
    
    def __init__(self, figsize=(12, 8), dpi=100):
        """
        初始化甘特图
        
        参数:
            figsize (tuple, optional): 图形大小，默认为(12, 8)
            dpi (int, optional): 图形分辨率，默认为100
        """
        self.figsize = figsize
        self.dpi = dpi
        self.fig = None
        self.ax = None
    
    def plot(self, event_log, activities, resources=None, title="SDESA Simulation Gantt Chart"):
        """
        绘制甘特图
        
        参数:
            event_log (list): 事件日志
            activities (dict): 活动字典，键为活动ID，值为活动对象
            resources (dict, optional): 资源字典，键为资源ID，值为资源对象
            title (str, optional): 图表标题，默认为"SDESA Simulation Gantt Chart"
        
        返回:
            matplotlib.figure.Figure: 图形对象
        """
        # 创建图形
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # 提取活动开始和结束事件
        activity_events = {}
        for event in event_log:
            if event.activity_id not in activity_events:
                activity_events[event.activity_id] = {'begin': [], 'end': []}
            
            if event.type == 'begin_service':
                activity_events[event.activity_id]['begin'].append(event)
            elif event.type == 'end_service':
                activity_events[event.activity_id]['end'].append(event)
        
        # 为每个活动分配一个颜色
        colors = plt.cm.tab20.colors
        activity_colors = {activity_id: colors[i % len(colors)] for i, activity_id in enumerate(activities.keys())}
        
        # 绘制活动条
        y_pos = 0
        y_ticks = []
        y_labels = []
        
        for activity_id, events in activity_events.items():
            activity_name = activities[activity_id].name if activity_id in activities else activity_id
            y_labels.append(activity_name)
            y_ticks.append(y_pos)
            
            # 匹配开始和结束事件
            for begin_event in events['begin']:
                for end_event in events['end']:
                    if begin_event.entity_id == end_event.entity_id:
                        # 绘制活动条
                        duration = end_event.time - begin_event.time
                        self.ax.barh(y_pos, duration, left=begin_event.time, height=0.5, 
                                     color=activity_colors[activity_id], alpha=0.8)
                        
                        # 添加活动标签
                        self.ax.text(begin_event.time + duration/2, y_pos, f"{activity_name} ({begin_event.entity_id})", 
                                     ha='center', va='center', color='black', fontsize=8)
                        
                        break
            
            y_pos += 1
        
        # 设置Y轴
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels(y_labels)
        
        # 设置X轴
        self.ax.set_xlabel('Time')
        
        # 设置标题
        self.ax.set_title(title)
        
        # 添加网格线
        self.ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        
        # 调整布局
        plt.tight_layout()
        
        return self.fig
    
    def save(self, filename):
        """
        保存甘特图
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 保存的文件名
        """
        if self.fig is None:
            raise ValueError("Please call plot() before save()")
        
        self.fig.savefig(filename)
        return filename


class ResourceUtilizationChart:
    """
    资源利用率图表类
    
    用于绘制资源利用率图表，显示资源的利用情况。
    """
    
    def __init__(self, figsize=(10, 6), dpi=100):
        """
        初始化资源利用率图表
        
        参数:
            figsize (tuple, optional): 图形大小，默认为(10, 6)
            dpi (int, optional): 图形分辨率，默认为100
        """
        self.figsize = figsize
        self.dpi = dpi
        self.fig = None
        self.ax = None
    
    def plot(self, resource_statistics, title="Resource Utilization"):
        """
        绘制资源利用率图表
        
        参数:
            resource_statistics (dict): 资源统计字典，键为资源ID，值为ResourceStatistics对象
            title (str, optional): 图表标题，默认为"Resource Utilization"
        
        返回:
            matplotlib.figure.Figure: 图形对象
        """
        # 创建图形
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # 提取资源ID和利用率
        resource_ids = []
        utilization_rates = []
        
        for resource_id, stats in resource_statistics.items():
            resource_ids.append(resource_id)
            utilization_rates.append(stats.calculate_utilization_rate())
        
        # 绘制条形图
        bars = self.ax.bar(resource_ids, utilization_rates, color='skyblue')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                         f'{height:.2f}', ha='center', va='bottom')
        
        # 设置Y轴范围
        self.ax.set_ylim(0, 1.1)
        
        # 设置标题和标签
        self.ax.set_title(title)
        self.ax.set_xlabel('Resource')
        self.ax.set_ylabel('Utilization Rate')
        
        # 添加网格线
        self.ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # 调整布局
        plt.tight_layout()
        
        return self.fig
    
    def save(self, filename):
        """
        保存资源利用率图表
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 保存的文件名
        """
        if self.fig is None:
            raise ValueError("Please call plot() before save()")
        
        self.fig.savefig(filename)
        return filename


class ActivityNetworkGraph:
    """
    活动网络图类
    
    用于绘制活动网络图，显示活动之间的关系。
    """
    
    def __init__(self, figsize=(12, 8), dpi=100):
        """
        初始化活动网络图
        
        参数:
            figsize (tuple, optional): 图形大小，默认为(12, 8)
            dpi (int, optional): 图形分辨率，默认为100
        """
        self.figsize = figsize
        self.dpi = dpi
        self.fig = None
        self.ax = None
    
    def plot(self, model, title="Activity Network"):
        """
        绘制活动网络图
        
        参数:
            model (Model): 模型对象
            title (str, optional): 图表标题，默认为"Activity Network"
        
        返回:
            matplotlib.figure.Figure: 图形对象
        """
        # 创建图形
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # 创建有向图
        G = nx.DiGraph()
        
        # 添加节点
        for activity_id, activity in model.activities.items():
            G.add_node(activity_id, label=activity.name)
        
        # 添加边
        for activity_id, activity in model.activities.items():
            for successor_id in activity.successor_activities:
                G.add_edge(activity_id, successor_id)
        
        # 设置节点位置
        pos = nx.spring_layout(G, seed=42)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500, alpha=0.8, ax=self.ax)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, ax=self.ax)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['label'] for n in G.nodes()}, 
                               font_size=10, font_weight='bold', ax=self.ax)
        
        # 设置标题
        self.ax.set_title(title)
        
        # 关闭坐标轴
        self.ax.axis('off')
        
        # 调整布局
        plt.tight_layout()
        
        return self.fig
    
    def save(self, filename):
        """
        保存活动网络图
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 保存的文件名
        """
        if self.fig is None:
            raise ValueError("Please call plot() before save()")
        
        self.fig.savefig(filename)
        return filename


class SimulationAnimator:
    """
    模拟动画类
    
    用于创建模拟过程的动画。
    """
    
    def __init__(self, figsize=(12, 8), dpi=100):
        """
        初始化模拟动画
        
        参数:
            figsize (tuple, optional): 图形大小，默认为(12, 8)
            dpi (int, optional): 图形分辨率，默认为100
        """
        self.figsize = figsize
        self.dpi = dpi
        self.fig = None
        self.ax = None
        self.model = None
        self.frames = []
    
    def initialize(self, model):
        """
        初始化动画
        
        参数:
            model (Model): 模型对象
        """
        self.model = model
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        self.frames = []
    
    def update(self, event):
        """
        更新动画
        
        参数:
            event (Event): 事件对象
        """
        if self.fig is None:
            raise ValueError("Please call initialize() before update()")
        
        # 清除当前轴
        self.ax.clear()
        
        # 绘制当前状态
        # 这里需要根据具体的模型和事件类型来绘制
        # 这只是一个示例
        self.ax.set_title(f"Time: {event.time:.2f}, Event: {event.type}, Activity: {event.activity_id}")
        
        # 保存当前帧
        self.fig.canvas.draw()
        frame = np.array(self.fig.canvas.renderer.buffer_rgba())
        self.frames.append(frame)
    
    def save(self, filename, fps=10):
        """
        保存动画
        
        参数:
            filename (str): 文件名
            fps (int, optional): 每秒帧数，默认为10
        
        返回:
            str: 保存的文件名
        """
        if not self.frames:
            raise ValueError("No frames to save")
        
        import matplotlib.animation as animation
        
        # 创建动画
        ani = animation.ArtistAnimation(self.fig, self.frames, interval=1000/fps, blit=True)
        
        # 保存动画
        ani.save(filename, writer='ffmpeg', fps=fps)
        
        return filename


class DashboardGenerator:
    """
    仪表板生成器类
    
    用于创建交互式仪表板，显示模拟结果。
    """
    
    def __init__(self):
        """
        初始化仪表板生成器
        """
        self.fig = None
    
    def create_dashboard(self, simulation_statistics):
        """
        创建仪表板
        
        参数:
            simulation_statistics (SimulationStatistics): 模拟统计对象
        
        返回:
            plotly.graph_objects.Figure: 图形对象
        """
        # 创建子图
        self.fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Resource Utilization", "Activity Completion Count", 
                           "Average Waiting Time", "Average Service Time"),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                  [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # 资源利用率
        resource_ids = []
        utilization_rates = []
        
        for resource_id, stats in simulation_statistics.resource_statistics.items():
            resource_ids.append(resource_id)
            utilization_rates.append(stats.calculate_utilization_rate(simulation_statistics.total_simulation_time))
        
        self.fig.add_trace(
            go.Bar(x=resource_ids, y=utilization_rates, name="Utilization Rate"),
            row=1, col=1
        )
        
        # 活动完成次数
        activity_ids = []
        completion_counts = []
        
        for activity_id, stats in simulation_statistics.activity_statistics.items():
            activity_ids.append(activity_id)
            completion_counts.append(stats.completion_count)
        
        self.fig.add_trace(
            go.Bar(x=activity_ids, y=completion_counts, name="Completion Count"),
            row=1, col=2
        )
        
        # 平均等待时间
        activity_ids = []
        avg_waiting_times = []
        
        for activity_id, stats in simulation_statistics.activity_statistics.items():
            activity_ids.append(activity_id)
            avg_waiting_times.append(stats.calculate_average_waiting_time())
        
        self.fig.add_trace(
            go.Bar(x=activity_ids, y=avg_waiting_times, name="Average Waiting Time"),
            row=2, col=1
        )
        
        # 平均服务时间
        activity_ids = []
        avg_service_times = []
        
        for activity_id, stats in simulation_statistics.activity_statistics.items():
            activity_ids.append(activity_id)
            avg_service_times.append(stats.calculate_average_service_time())
        
        self.fig.add_trace(
            go.Bar(x=activity_ids, y=avg_service_times, name="Average Service Time"),
            row=2, col=2
        )
        
        # 更新布局
        self.fig.update_layout(
            title_text="SDESA Simulation Dashboard",
            height=800,
            width=1200,
            showlegend=False
        )
        
        return self.fig
    
    def save(self, filename):
        """
        保存仪表板
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 保存的文件名
        """
        if self.fig is None:
            raise ValueError("Please call create_dashboard() before save()")
        
        self.fig.write_html(filename)
        return filename
