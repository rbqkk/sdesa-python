"""
SDESA Python库 - 核心模块

该模块包含SDESA的核心数据结构和算法，包括流实体、资源实体、
流实体队列、资源实体队列、事件和事件日历等。
"""

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
        self.id = id
        self.activity_id = activity_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.attributes = attributes or {}
    
    def __str__(self):
        """返回流实体的字符串表示"""
        return f"FlowEntity(id={self.id}, activity_id={self.activity_id}, arrival_time={self.arrival_time}, departure_time={self.departure_time})"
    
    def is_processed(self):
        """
        检查流实体是否已处理
        
        如果departure_time不为0，则表示流实体已处理
        
        返回:
            bool: 如果流实体已处理则为True，否则为False
        """
        return self.departure_time > 0


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
        self.id = id
        self.type = type
        self.ready_time = ready_time
        self.available = available
        self.disposable = disposable
        self.attributes = attributes or {}
    
    def __str__(self):
        """返回资源实体的字符串表示"""
        return f"ResourceEntity(id={self.id}, type={self.type}, ready_time={self.ready_time}, available={self.available}, disposable={self.disposable})"


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
        self.entities = []
    
    def add_entity(self, entity):
        """
        添加流实体到队列
        
        参数:
            entity (FlowEntity): 要添加的流实体
        """
        self.entities.append(entity)
    
    def get_next_unprocessed(self):
        """
        获取下一个未处理的流实体
        
        按照到达时间的先后顺序，获取下一个未处理的流实体。
        如果有多个流实体具有相同的到达时间，则随机选择一个。
        
        返回:
            FlowEntity or None: 下一个未处理的流实体，如果没有则返回None
        """
        unprocessed = [e for e in self.entities if e.departure_time == 0]
        if not unprocessed:
            return None
        
        # 按照到达时间排序
        unprocessed.sort(key=lambda e: e.arrival_time)
        return unprocessed[0]
    
    def update_entity(self, entity_id, **kwargs):
        """
        更新流实体属性
        
        参数:
            entity_id (str): 要更新的流实体ID
            **kwargs: 要更新的属性和值
        
        返回:
            bool: 如果更新成功则为True，否则为False
        """
        for entity in self.entities:
            if entity.id == entity_id:
                for key, value in kwargs.items():
                    setattr(entity, key, value)
                return True
        return False
    
    def __len__(self):
        """返回队列中流实体的数量"""
        return len(self.entities)
    
    def __str__(self):
        """返回流实体队列的字符串表示"""
        return f"FlowEntityQueue(entities={len(self.entities)})"


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
        self.entities = []
    
    def add_entity(self, entity):
        """
        添加资源实体到队列
        
        参数:
            entity (ResourceEntity): 要添加的资源实体
        """
        self.entities.append(entity)
    
    def get_resource(self, type):
        """
        获取指定类型的资源
        
        按照准备就绪时间的先后顺序，获取指定类型的可用资源。
        
        参数:
            type (str): 资源类型
        
        返回:
            ResourceEntity or None: 指定类型的资源，如果没有则返回None
        """
        available_resources = [r for r in self.entities if r.type == type and r.available]
        if not available_resources:
            return None
        
        # 按照准备就绪时间排序
        available_resources.sort(key=lambda r: r.ready_time)
        return available_resources[0]
    
    def update_entity(self, entity_id, **kwargs):
        """
        更新资源实体属性
        
        参数:
            entity_id (str): 要更新的资源实体ID
            **kwargs: 要更新的属性和值
        
        返回:
            bool: 如果更新成功则为True，否则为False
        """
        for entity in self.entities:
            if entity.id == entity_id:
                for key, value in kwargs.items():
                    setattr(entity, key, value)
                return True
        return False
    
    def __len__(self):
        """返回队列中资源实体的数量"""
        return len(self.entities)
    
    def __str__(self):
        """返回资源实体队列的字符串表示"""
        return f"ResourceEntityQueue(entities={len(self.entities)})"


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
        self.time = time
        self.type = type
        self.entity_id = entity_id
        self.activity_id = activity_id
    
    def __str__(self):
        """返回事件的字符串表示"""
        return f"Event(time={self.time}, type={self.type}, entity_id={self.entity_id}, activity_id={self.activity_id})"
    
    def __lt__(self, other):
        """比较两个事件的发生时间，用于事件日历的排序"""
        return self.time < other.time


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
        self.events = []
    
    def schedule_event(self, event):
        """
        安排事件
        
        参数:
            event (Event): 要安排的事件
        """
        self.events.append(event)
        # 按照事件发生时间排序
        self.events.sort()
    
    def get_next_event(self):
        """
        获取下一个事件
        
        返回:
            Event or None: 下一个事件，如果没有则返回None
        """
        if not self.events:
            return None
        return self.events[0]
    
    def remove_event(self, event):
        """
        移除事件
        
        参数:
            event (Event): 要移除的事件
        
        返回:
            bool: 如果移除成功则为True，否则为False
        """
        if event in self.events:
            self.events.remove(event)
            return True
        return False
    
    def __len__(self):
        """返回日历中事件的数量"""
        return len(self.events)
    
    def __str__(self):
        """返回事件日历的字符串表示"""
        return f"EventCalendar(events={len(self.events)})"


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
        self.current_time = initial_time
    
    def advance(self, time):
        """
        推进时间
        
        参数:
            time (float): 要推进到的时间
        
        返回:
            float: 推进后的当前时间
        """
        if time < self.current_time:
            raise ValueError(f"Cannot advance clock to {time}, current time is {self.current_time}")
        self.current_time = time
        return self.current_time
    
    def __str__(self):
        """返回模拟时钟的字符串表示"""
        return f"SimulationClock(current_time={self.current_time})"
