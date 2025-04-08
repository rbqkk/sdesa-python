"""
SDESA Python库 - 模拟引擎模块

该模块包含SDESA的模拟引擎，负责执行模拟过程。
"""

from .core import Event, EventCalendar, SimulationClock, FlowEntityQueue, ResourceEntityQueue
from .model import Model


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
        self.model = model
        self.flow_entity_queue = FlowEntityQueue()
        self.resource_entity_queue = ResourceEntityQueue()
        self.event_calendar = EventCalendar()
        self.clock = SimulationClock()
        self.event_log = []
        self.statistics = {
            'activity_statistics': {},
            'resource_statistics': {},
            'total_simulation_time': 0
        }
    
    def initialize(self):
        """
        初始化模拟
        
        初始化流实体队列、资源实体队列和事件日历。
        """
        # 初始化流实体队列
        for entity in self.model.initial_flow_entities:
            self.flow_entity_queue.add_entity(entity)
        
        # 初始化资源实体队列
        for resource in self.model.initial_resources:
            self.resource_entity_queue.add_entity(resource)
        
        # 初始化活动统计
        for activity_id in self.model.activities:
            self.statistics['activity_statistics'][activity_id] = {
                'completion_count': 0,
                'waiting_times': [],
                'service_times': []
            }
        
        # 初始化资源统计
        for resource in self.model.initial_resources:
            self.statistics['resource_statistics'][resource.id] = {
                'busy_periods': [],
                'idle_periods': []
            }
    
    def run(self, duration=float('inf')):
        """
        运行模拟
        
        参数:
            duration (float, optional): 模拟持续时间，默认为无限
        
        返回:
            dict: 模拟统计数据
        """
        # 初始化模拟
        self.initialize()
        
        # 处理初始流实体
        next_entity = self.flow_entity_queue.get_next_unprocessed()
        while next_entity and self.clock.current_time < duration:
            self.process_begin_service_event(next_entity)
            next_entity = self.flow_entity_queue.get_next_unprocessed()
        
        # 主模拟循环
        while self.event_calendar.events and self.clock.current_time < duration:
            next_event = self.event_calendar.get_next_event()
            self.event_calendar.remove_event(next_event)
            
            # 推进模拟时钟
            self.clock.advance(next_event.time)
            
            # 记录事件
            self.event_log.append(next_event)
            
            # 处理事件
            if next_event.type == Event.BEGIN_SERVICE:
                # 查找对应的流实体
                for entity in self.flow_entity_queue.entities:
                    if entity.id == next_event.entity_id and entity.activity_id == next_event.activity_id:
                        self.process_begin_service_event(entity)
                        break
            elif next_event.type == Event.END_SERVICE:
                # 查找对应的流实体
                for entity in self.flow_entity_queue.entities:
                    if entity.id == next_event.entity_id and entity.activity_id == next_event.activity_id:
                        self.process_end_service_event(entity)
                        break
            
            # 处理下一个未处理的流实体
            next_entity = self.flow_entity_queue.get_next_unprocessed()
            while next_entity and self.clock.current_time < duration:
                self.process_begin_service_event(next_entity)
                next_entity = self.flow_entity_queue.get_next_unprocessed()
        
        # 记录总模拟时间
        self.statistics['total_simulation_time'] = self.clock.current_time
        
        return self.statistics
    
    def process_begin_service_event(self, entity):
        """
        处理服务开始事件
        
        参数:
            entity (FlowEntity): 要处理的流实体
        
        返回:
            bool: 如果处理成功则为True，否则为False
        """
        # 获取活动
        activity = self.model.get_activity(entity.activity_id)
        if not activity:
            return False
        
        # 如果活动不需要资源，直接处理
        if not activity.required_resources:
            # 设置开始时间为到达时间
            begin_time = entity.arrival_time
            
            # 生成活动持续时间
            duration = activity.get_duration()
            
            # 计算结束时间
            end_time = begin_time + duration
            
            # 安排服务结束事件
            end_event = Event(end_time, Event.END_SERVICE, entity.id, entity.activity_id)
            self.event_calendar.schedule_event(end_event)
            
            # 记录统计数据
            self.statistics['activity_statistics'][activity.id]['waiting_times'].append(0)
            self.statistics['activity_statistics'][activity.id]['service_times'].append(duration)
            
            return True
        
        # 尝试获取所需资源
        required_resources = []
        for resource_type in activity.required_resources:
            resource = self.resource_entity_queue.get_resource(resource_type)
            if not resource:
                # 如果无法获取所需资源，返回False
                return False
            required_resources.append(resource)
        
        # 计算开始时间
        begin_time = max(entity.arrival_time, max(r.ready_time for r in required_resources))
        
        # 生成活动持续时间
        duration = activity.get_duration()
        
        # 计算结束时间
        end_time = begin_time + duration
        
        # 更新资源就绪时间
        for resource in required_resources:
            # 记录资源忙碌时间段
            self.statistics['resource_statistics'][resource.id]['busy_periods'].append((begin_time, end_time))
            
            # 如果资源在活动结束后释放，更新就绪时间
            if resource.type in activity.released_resources:
                self.resource_entity_queue.update_entity(resource.id, ready_time=end_time)
            # 如果资源是一次性资源，标记为不可用
            elif resource.disposable:
                self.resource_entity_queue.update_entity(resource.id, available=False)
        
        # 安排服务结束事件
        end_event = Event(end_time, Event.END_SERVICE, entity.id, entity.activity_id)
        self.event_calendar.schedule_event(end_event)
        
        # 记录统计数据
        waiting_time = begin_time - entity.arrival_time
        self.statistics['activity_statistics'][activity.id]['waiting_times'].append(waiting_time)
        self.statistics['activity_statistics'][activity.id]['service_times'].append(duration)
        
        return True
    
    def process_end_service_event(self, entity):
        """
        处理服务结束事件
        
        参数:
            entity (FlowEntity): 要处理的流实体
        
        返回:
            bool: 如果处理成功则为True，否则为False
        """
        # 获取活动
        activity = self.model.get_activity(entity.activity_id)
        if not activity:
            return False
        
        # 获取事件时间
        event_time = self.clock.current_time
        
        # 更新流实体离开时间
        self.flow_entity_queue.update_entity(entity.id, departure_time=event_time)
        
        # 增加活动完成计数
        self.statistics['activity_statistics'][activity.id]['completion_count'] += 1
        
        # 生成一次性资源
        for resource_type in activity.generated_resources:
            resource_id = f"{resource_type}_{len(self.resource_entity_queue.entities)}"
            resource = ResourceEntity(
                id=resource_id,
                type=resource_type,
                ready_time=event_time,
                available=True,
                disposable=True
            )
            self.resource_entity_queue.add_entity(resource)
        
        # 创建后继活动的流实体
        for successor_id in activity.successor_activities:
            new_entity_id = f"{entity.id}_{successor_id}"
            new_entity = FlowEntity(
                id=new_entity_id,
                activity_id=successor_id,
                arrival_time=event_time,
                departure_time=0
            )
            self.flow_entity_queue.add_entity(new_entity)
        
        return True
    
    def get_activity_statistics(self, activity_id):
        """
        获取活动统计数据
        
        参数:
            activity_id (str): 活动ID
        
        返回:
            dict: 活动统计数据
        """
        return self.statistics['activity_statistics'].get(activity_id, {})
    
    def get_resource_statistics(self, resource_id):
        """
        获取资源统计数据
        
        参数:
            resource_id (str): 资源ID
        
        返回:
            dict: 资源统计数据
        """
        return self.statistics['resource_statistics'].get(resource_id, {})
    
    def calculate_resource_utilization(self, resource_id):
        """
        计算资源利用率
        
        参数:
            resource_id (str): 资源ID
        
        返回:
            float: 资源利用率（0-1之间的值）
        """
        resource_stats = self.get_resource_statistics(resource_id)
        if not resource_stats or not resource_stats.get('busy_periods'):
            return 0.0
        
        total_busy_time = sum(end - start for start, end in resource_stats['busy_periods'])
        return total_busy_time / self.statistics['total_simulation_time'] if self.statistics['total_simulation_time'] > 0 else 0.0
