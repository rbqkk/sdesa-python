"""
SDESA Python库 - 模型模块

该模块包含SDESA的模型定义和构建功能，包括活动和模型类。
"""

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
        self.id = id
        self.name = name
        self.duration_function = duration_function
        self.required_resources = required_resources or []
        self.released_resources = released_resources or []
        self.generated_resources = generated_resources or []
        self.successor_activities = successor_activities or []
        self.priority = priority
    
    def get_duration(self):
        """
        获取活动持续时间
        
        调用持续时间函数获取活动持续时间。
        
        返回:
            float: 活动持续时间
        """
        return self.duration_function()
    
    def __str__(self):
        """返回活动的字符串表示"""
        return f"Activity(id={self.id}, name={self.name}, required_resources={self.required_resources})"


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
        self.name = name
        self.activities = {}
        self.initial_flow_entities = []
        self.initial_resources = []
    
    def add_activity(self, activity):
        """
        添加活动
        
        参数:
            activity (Activity): 要添加的活动
        
        返回:
            bool: 如果添加成功则为True，否则为False
        """
        if activity.id in self.activities:
            return False
        self.activities[activity.id] = activity
        return True
    
    def add_flow_entity(self, entity):
        """
        添加初始流实体
        
        参数:
            entity (FlowEntity): 要添加的流实体
        """
        self.initial_flow_entities.append(entity)
    
    def add_resource(self, resource):
        """
        添加初始资源
        
        参数:
            resource (ResourceEntity): 要添加的资源
        """
        self.initial_resources.append(resource)
    
    def get_activity(self, activity_id):
        """
        获取活动
        
        参数:
            activity_id (str): 活动ID
        
        返回:
            Activity or None: 指定ID的活动，如果没有则返回None
        """
        return self.activities.get(activity_id)
    
    def validate(self):
        """
        验证模型
        
        检查模型是否有效，包括：
        1. 所有活动的后继活动都存在
        2. 所有流实体的初始活动都存在
        
        返回:
            bool: 如果模型有效则为True，否则为False
        """
        # 检查所有活动的后继活动都存在
        for activity_id, activity in self.activities.items():
            for successor_id in activity.successor_activities:
                if successor_id not in self.activities:
                    return False
        
        # 检查所有流实体的初始活动都存在
        for entity in self.initial_flow_entities:
            if entity.activity_id not in self.activities:
                return False
        
        return True
    
    def __str__(self):
        """返回模型的字符串表示"""
        return f"Model(name={self.name}, activities={len(self.activities)}, initial_flow_entities={len(self.initial_flow_entities)}, initial_resources={len(self.initial_resources)})"
