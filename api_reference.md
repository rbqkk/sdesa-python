"""
SDESA Python库 - API参考文档
"""

# 核心模块 (sdesa.core)

## FlowEntity

```python
class FlowEntity:
    """
    流实体类
    
    流实体是在模拟系统中流动的实体，如卡车、道路部分等。
    每个流实体都有一个唯一的ID，当前所在的活动ID，到达时间和离开时间。
    
    属性:
        id (str): 流实体的唯一标识符
        activity_id (str): 当前活动的ID
        arrival_time (float): 到达当前活动的时间
        departure_time (float): 离开当前活动的时间，初始为0表示未处理
        attributes (dict): 自定义属性字典
    """
    
    def __init__(self, id, activity_id, arrival_time=0, departure_time=0, attributes=None):
        """
        初始化流实体
        
        参数:
            id (str): 流实体的唯一标识符
            activity_id (str): 当前活动的ID
            arrival_time (float, optional): 到达当前活动的时间，默认为0
            departure_time (float, optional): 离开当前活动的时间，默认为0
            attributes (dict, optional): 自定义属性字典，默认为None
        """
        
    def is_processed(self):
        """
        检查流实体是否已处理
        
        如果departure_time不为0，则表示流实体已处理
        
        返回:
            bool: 如果流实体已处理则为True，否则为False
        """
```

## ResourceEntity

```python
class ResourceEntity:
    """
    资源实体类
    
    资源实体是在模拟系统中被流实体使用的资源，如装载机、旗手等。
    每个资源实体都有一个唯一的ID，资源类型，准备就绪时间，可用性和是否为一次性资源。
    
    属性:
        id (str): 资源实体的唯一标识符
        type (str): 资源类型
        ready_time (float): 资源准备就绪的时间
        available (bool): 资源是否可用
        disposable (bool): 资源是否为一次性资源
        attributes (dict): 自定义属性字典
    """
    
    def __init__(self, id, type, ready_time=0, available=True, disposable=False, attributes=None):
        """
        初始化资源实体
        
        参数:
            id (str): 资源实体的唯一标识符
            type (str): 资源类型
            ready_time (float, optional): 资源准备就绪的时间，默认为0
            available (bool, optional): 资源是否可用，默认为True
            disposable (bool, optional): 资源是否为一次性资源，默认为False
            attributes (dict, optional): 自定义属性字典，默认为None
        """
```

## FlowEntityQueue

```python
class FlowEntityQueue:
    """
    流实体队列类
    
    流实体队列用于存储和管理流实体。
    它提供了添加流实体、获取下一个未处理的流实体和更新流实体属性的方法。
    
    属性:
        entities (list): 流实体列表
    """
    
    def __init__(self):
        """初始化流实体队列"""
        
    def add_entity(self, entity):
        """
        添加流实体到队列
        
        参数:
            entity (FlowEntity): 要添加的流实体
        """
        
    def get_next_unprocessed(self):
        """
        获取下一个未处理的流实体
        
        按照到达时间的先后顺序，获取下一个未处理的流实体。
        如果有多个流实体具有相同的到达时间，则随机选择一个。
        
        返回:
            FlowEntity or None: 下一个未处理的流实体，如果没有则返回None
        """
        
    def update_entity(self, entity_id, **kwargs):
        """
        更新流实体属性
        
        参数:
            entity_id (str): 要更新的流实体ID
            **kwargs: 要更新的属性和值
        
        返回:
            bool: 如果更新成功则为True，否则为False
        """
```

## ResourceEntityQueue

```python
class ResourceEntityQueue:
    """
    资源实体队列类
    
    资源实体队列用于存储和管理资源实体。
    它提供了添加资源实体、获取指定类型的资源和更新资源实体属性的方法。
    
    属性:
        entities (list): 资源实体列表
    """
    
    def __init__(self):
        """初始化资源实体队列"""
        
    def add_entity(self, entity):
        """
        添加资源实体到队列
        
        参数:
            entity (ResourceEntity): 要添加的资源实体
        """
        
    def get_resource(self, type):
        """
        获取指定类型的资源
        
        按照准备就绪时间的先后顺序，获取指定类型的可用资源。
        
        参数:
            type (str): 资源类型
        
        返回:
            ResourceEntity or None: 指定类型的资源，如果没有则返回None
        """
        
    def update_entity(self, entity_id, **kwargs):
        """
        更新资源实体属性
        
        参数:
            entity_id (str): 要更新的资源实体ID
            **kwargs: 要更新的属性和值
        
        返回:
            bool: 如果更新成功则为True，否则为False
        """
```

## Event

```python
class Event:
    """
    事件类
    
    事件是模拟过程中的关键点，包括服务开始事件和服务结束事件。
    每个事件都有一个发生时间、事件类型、相关流实体ID和相关活动ID。
    
    属性:
        time (float): 事件发生时间
        type (str): 事件类型（'begin_service'或'end_service'）
        entity_id (str): 相关流实体ID
        activity_id (str): 相关活动ID
    """
    
    BEGIN_SERVICE = 'begin_service'
    END_SERVICE = 'end_service'
    
    def __init__(self, time, type, entity_id, activity_id):
        """
        初始化事件
        
        参数:
            time (float): 事件发生时间
            type (str): 事件类型（'begin_service'或'end_service'）
            entity_id (str): 相关流实体ID
            activity_id (str): 相关活动ID
        """
```

## EventCalendar

```python
class EventCalendar:
    """
    事件日历类
    
    事件日历用于存储和管理事件。
    它提供了安排事件、获取下一个事件和移除事件的方法。
    
    属性:
        events (list): 事件列表
    """
    
    def __init__(self):
        """初始化事件日历"""
        
    def schedule_event(self, event):
        """
        安排事件
        
        参数:
            event (Event): 要安排的事件
        """
        
    def get_next_event(self):
        """
        获取下一个事件
        
        返回:
            Event or None: 下一个事件，如果没有则返回None
        """
        
    def remove_event(self, event):
        """
        移除事件
        
        参数:
            event (Event): 要移除的事件
        
        返回:
            bool: 如果移除成功则为True，否则为False
        """
```

## SimulationClock

```python
class SimulationClock:
    """
    模拟时钟类
    
    模拟时钟用于跟踪模拟过程中的当前时间。
    
    属性:
        current_time (float): 当前模拟时间
    """
    
    def __init__(self, initial_time=0):
        """
        初始化模拟时钟
        
        参数:
            initial_time (float, optional): 初始时间，默认为0
        """
        
    def advance(self, time):
        """
        推进时间
        
        参数:
            time (float): 要推进到的时间
        
        返回:
            float: 推进后的当前时间
        """
```

# 模型模块 (sdesa.model)

## Activity

```python
class Activity:
    """
    活动类
    
    活动是模拟系统中的基本操作单元，如装载、运输、卸载等。
    每个活动都有一个唯一的ID，活动名称，持续时间函数，所需资源列表，
    释放资源列表，生成资源列表和后继活动列表。
    
    属性:
        id (str): 活动的唯一标识符
        name (str): 活动名称
        duration_function (callable): 返回活动持续时间的函数
        required_resources (list): 所需资源类型列表
        released_resources (list): 释放资源类型列表
        generated_resources (list): 生成资源类型列表
        successor_activities (list): 后继活动ID列表
        priority (int): 活动优先级，用于解决同时到达的流实体的处理顺序
    """
    
    def __init__(self, id, name, duration_function, required_resources=None, 
                 released_resources=None, generated_resources=None, 
                 successor_activities=None, priority=0):
        """
        初始化活动
        
        参数:
            id (str): 活动的唯一标识符
            name (str): 活动名称
            duration_function (callable): 返回活动持续时间的函数
            required_resources (list, optional): 所需资源类型列表，默认为None
            released_resources (list, optional): 释放资源类型列表，默认为None
            generated_resources (list, optional): 生成资源类型列表，默认为None
            successor_activities (list, optional): 后继活动ID列表，默认为None
            priority (int, optional): 活动优先级，默认为0
        """
        
    def get_duration(self):
        """
        获取活动持续时间
        
        调用持续时间函数获取活动持续时间。
        
        返回:
            float: 活动持续时间
        """
```

## Model

```python
class Model:
    """
    模型类
    
    模型是SDESA模拟的核心，包含活动、初始流实体和初始资源。
    
    属性:
        name (str): 模型名称
        activities (dict): 活动字典，键为活动ID，值为活动对象
        initial_flow_entities (list): 初始流实体列表
        initial_resources (list): 初始资源列表
    """
    
    def __init__(self, name):
        """
        初始化模型
        
        参数:
            name (str): 模型名称
        """
        
    def add_activity(self, activity):
        """
        添加活动
        
        参数:
            activity (Activity): 要添加的活动
        
        返回:
            bool: 如果添加成功则为True，否则为False
        """
        
    def add_flow_entity(self, entity):
        """
        添加初始流实体
        
        参数:
            entity (FlowEntity): 要添加的流实体
        """
        
    def add_resource(self, resource):
        """
        添加初始资源
        
        参数:
            resource (ResourceEntity): 要添加的资源
        """
        
    def get_activity(self, activity_id):
        """
        获取活动
        
        参数:
            activity_id (str): 活动ID
        
        返回:
            Activity or None: 指定ID的活动，如果没有则返回None
        """
        
    def validate(self):
        """
        验证模型
        
        检查模型是否有效，包括：
        1. 所有活动的后继活动都存在
        2. 所有流实体的初始活动都存在
        
        返回:
            bool: 如果模型有效则为True，否则为False
        """
```

# 模拟引擎模块 (sdesa.engine)

## SimulationEngine

```python
class SimulationEngine:
    """
    模拟引擎类
    
    模拟引擎是SDESA的核心，负责执行模拟过程。
    它管理流实体队列、资源实体队列、事件日历和模拟时钟，
    处理服务开始事件和服务结束事件，并收集模拟统计数据。
    
    属性:
        model (Model): 模拟模型
        flow_entity_queue (FlowEntityQueue): 流实体队列
        resource_entity_queue (ResourceEntityQueue): 资源实体队列
        event_calendar (EventCalendar): 事件日历
        clock (SimulationClock): 模拟时钟
        event_log (list): 事件日志
        statistics (dict): 模拟统计数据
    """
    
    def __init__(self, model):
        """
        初始化模拟引擎
        
        参数:
            model (Model): 模拟模型
        """
        
    def initialize(self):
        """
        初始化模拟
        
        初始化流实体队列、资源实体队列和事件日历。
        """
        
    def run(self, duration=float('inf')):
        """
        运行模拟
        
        参数:
            duration (float, optional): 模拟持续时间，默认为无限
        
        返回:
            dict: 模拟统计数据
        """
        
    def process_begin_service_event(self, entity):
        """
        处理服务开始事件
        
        参数:
            entity (FlowEntity): 要处理的流实体
        
        返回:
            bool: 如果处理成功则为True，否则为False
        """
        
    def process_end_service_event(self, entity):
        """
        处理服务结束事件
        
        参数:
            entity (FlowEntity): 要处理的流实体
        
        返回:
            bool: 如果处理成功则为True，否则为False
        """
        
    def get_activity_statistics(self, activity_id):
        """
        获取活动统计数据
        
        参数:
            activity_id (str): 活动ID
        
        返回:
            dict: 活动统计数据
        """
        
    def get_resource_statistics(self, resource_id):
        """
        获取资源统计数据
        
        参数:
            resource_id (str): 资源ID
        
        返回:
            dict: 资源统计数据
        """
        
    def calculate_resource_utilization(self, resource_id):
        """
        计算资源利用率
        
        参数:
            resource_id (str): 资源ID
        
        返回:
            float: 资源利用率（0-1之间的值）
        """
```

# 统计模块 (sdesa.statistics)

## ActivityStatistics

```python
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
        
    def calculate_average_waiting_time(self):
        """
        计算平均等待时间
        
        返回:
            float: 平均等待时间
        """
        
    def calculate_average_service_time(self):
        """
        计算平均服务时间
        
        返回:
            float: 平均服务时间
        """
        
    def calculate_total_time(self):
        """
        计算总时间（等待时间 + 服务时间）
        
        返回:
            float: 总时间
        """
        
    def calculate_waiting_time_percentiles(self, percentiles=[25, 50, 75, 90, 95]):
        """
        计算等待时间百分位数
        
        参数:
            percentiles (list, optional): 百分位数列表，默认为[25, 50, 75, 90, 95]
        
        返回:
            dict: 百分位数字典，键为百分位数，值为对应的等待时间
        """
        
    def calculate_service_time_percentiles(self, percentiles=[25, 50, 75, 90, 95]):
        """
        计算服务时间百分位数
        
        参数:
            percentiles (list, optional): 百分位数列表，默认为[25, 50, 75, 90, 95]
        
        返回:
            dict: 百分位数字典，键为百分位数，值为对应的服务时间
        """
        
    def to_dict(self):
        """
        转换为字典
        
        返回:
            dict: 活动统计字典
        """
```

## ResourceStatistics

```python
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
        
    def calculate_utilization_rate(self, total_time=None):
        """
        计算利用率
        
        参数:
            total_time (float, optional): 总时间，默认为None
        
        返回:
            float: 利用率（0-1之间的值）
        """
        
    def calculate_average_busy_period(self):
        """
        计算平均忙碌时间段长度
        
        返回:
            float: 平均忙碌时间段长度
        """
        
    def calculate_average_idle_period(self):
        """
        计算平均空闲时间段长度
        
        返回:
            float: 平均空闲时间段长度
        """
        
    def calculate_busy_time_percentiles(self, percentiles=[25, 50, 75, 90, 95]):
        """
        计算忙碌时间段长度百分位数
        
        参数:
            percentiles (list, optional): 百分位数列表，默认为[25, 50, 75, 90, 95]
        
        返回:
            dict: 百分位数字典，键为百分位数，值为对应的忙碌时间段长度
        """
        
    def to_dict(self, total_time=None):
        """
        转换为字典
        
        参数:
            total_time (float, optional): 总时间，默认为None
        
        返回:
            dict: 资源统计字典
        """
```

## SimulationStatistics

```python
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
        
    def get_activity_statistics(self, activity_id):
        """
        获取活动统计
        
        参数:
            activity_id (str): 活动ID
        
        返回:
            ActivityStatistics: 活动统计对象
        """
        
    def get_resource_statistics(self, resource_id):
        """
        获取资源统计
        
        参数:
            resource_id (str): 资源ID
        
        返回:
            ResourceStatistics: 资源统计对象
        """
        
    def calculate_overall_resource_utilization(self):
        """
        计算总体资源利用率
        
        返回:
            float: 总体资源利用率（0-1之间的值）
        """
        
    def calculate_bottleneck_activities(self):
        """
        计算瓶颈活动
        
        返回:
            list: 瓶颈活动列表，按等待时间降序排序
        """
        
    def calculate_critical_resources(self):
        """
        计算关键资源
        
        返回:
            list: 关键资源列表，按利用率降序排序
        """
        
    def to_dict(self):
        """
        转换为字典
        
        返回:
            dict: 模拟统计字典
        """
        
    def export_to_csv(self, filename_prefix):
        """
        导出统计数据到CSV
        
        参数:
            filename_prefix (str): 文件名前缀
        
        返回:
            list: 导出的文件列表
        """
        
    def export_to_json(self, filename):
        """
        导出统计数据到JSON
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 导出的文件名
        """
```

# 工具模块 (sdesa.utils)

## RandomGenerator

```python
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
        
    @staticmethod
    def exponential(lambd):
        """
        生成指数分布随机数
        
        参数:
            lambd (float): 速率参数
        
        返回:
            float: 指数分布随机数
        """
        
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
        
    @staticmethod
    def set_seed(seed):
        """
        设置随机数种子
        
        参数:
            seed (int): 随机数种子
        """
```

## Logger

```python
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
        
    def debug(self, message):
        """
        记录调试信息
        
        参数:
            message (str): 消息内容
        """
        
    def info(self, message):
        """
        记录信息
        
        参数:
            message (str): 消息内容
        """
        
    def warning(self, message):
        """
        记录警告
        
        参数:
            message (str): 消息内容
        """
        
    def error(self, message):
        """
        记录错误
        
        参数:
            message (str): 消息内容
        """
```

## DataImporter

```python
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
        
    @staticmethod
    def import_from_json(filename):
        """
        从JSON导入数据
        
        参数:
            filename (str): JSON文件路径
        
        返回:
            dict: 导入的数据
        """
        
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
```

# 可视化模块 (sdesa.visualization)

## GanttChart

```python
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
        
    def save(self, filename):
        """
        保存甘特图
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 保存的文件名
        """
```

## ResourceUtilizationChart

```python
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
        
    def plot(self, resource_statistics, title="Resource Utilization"):
        """
        绘制资源利用率图表
        
        参数:
            resource_statistics (dict): 资源统计字典，键为资源ID，值为ResourceStatistics对象
            title (str, optional): 图表标题，默认为"Resource Utilization"
        
        返回:
            matplotlib.figure.Figure: 图形对象
        """
        
    def save(self, filename):
        """
        保存资源利用率图表
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 保存的文件名
        """
```

## ActivityNetworkGraph

```python
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
        
    def plot(self, model, title="Activity Network"):
        """
        绘制活动网络图
        
        参数:
            model (Model): 模型对象
            title (str, optional): 图表标题，默认为"Activity Network"
        
        返回:
            matplotlib.figure.Figure: 图形对象
        """
        
    def save(self, filename):
        """
        保存活动网络图
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 保存的文件名
        """
```

## SimulationAnimator

```python
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
        
    def initialize(self, model):
        """
        初始化动画
        
        参数:
            model (Model): 模型对象
        """
        
    def update(self, event):
        """
        更新动画
        
        参数:
            event (Event): 事件对象
        """
        
    def save(self, filename, fps=10):
        """
        保存动画
        
        参数:
            filename (str): 文件名
            fps (int, optional): 每秒帧数，默认为10
        
        返回:
            str: 保存的文件名
        """
```

## DashboardGenerator

```python
class DashboardGenerator:
    """
    仪表板生成器类
    
    用于创建交互式仪表板，显示模拟结果。
    """
    
    def __init__(self):
        """
        初始化仪表板生成器
        """
        
    def create_dashboard(self, simulation_statistics):
        """
        创建仪表板
        
        参数:
            simulation_statistics (SimulationStatistics): 模拟统计对象
        
        返回:
            plotly.graph_objects.Figure: 图形对象
        """
        
    def save(self, filename):
        """
        保存仪表板
        
        参数:
            filename (str): 文件名
        
        返回:
            str: 保存的文件名
        """
```
