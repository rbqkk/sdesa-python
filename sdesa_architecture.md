# SDESA Python库架构设计

## 1. 整体架构

SDESA Python库将采用模块化设计，主要包含以下几个核心模块：

### 1.1 核心模块（Core）
- 实现SDESA的基本数据结构和算法
- 包含流实体队列、资源实体队列和事件处理机制
- 提供模拟执行引擎

### 1.2 模型模块（Model）
- 提供模型定义和构建功能
- 支持活动、资源和流实体的定义
- 支持活动之间的逻辑关系定义

### 1.3 统计模块（Statistics）
- 收集和分析模拟结果
- 计算资源利用率、活动完成时间等关键指标
- 提供统计数据的导出功能

### 1.4 可视化模块（Visualization）
- 提供模拟过程和结果的可视化功能
- 支持甘特图、资源利用率图表等
- 支持动态模拟过程的可视化

### 1.5 工具模块（Utils）
- 提供辅助功能，如随机数生成、数据导入导出等
- 提供常用的概率分布函数（如Beta分布）
- 提供日志和调试工具

## 2. 核心组件和类结构

### 2.1 核心模块（Core）

#### 2.1.1 `FlowEntity` 类
- 属性：
  - `id`: 流实体ID
  - `activity_id`: 当前活动ID
  - `arrival_time`: 到达时间
  - `departure_time`: 离开时间
  - `attributes`: 自定义属性字典

#### 2.1.2 `ResourceEntity` 类
- 属性：
  - `id`: 资源实体ID
  - `type`: 资源类型
  - `ready_time`: 准备就绪时间
  - `available`: 是否可用
  - `disposable`: 是否为一次性资源
  - `attributes`: 自定义属性字典

#### 2.1.3 `FlowEntityQueue` 类
- 方法：
  - `add_entity(entity)`: 添加流实体
  - `get_next_unprocessed()`: 获取下一个未处理的流实体
  - `update_entity(entity_id, **kwargs)`: 更新流实体属性

#### 2.1.4 `ResourceEntityQueue` 类
- 方法：
  - `add_entity(entity)`: 添加资源实体
  - `get_resource(type)`: 获取指定类型的资源
  - `update_entity(entity_id, **kwargs)`: 更新资源实体属性

#### 2.1.5 `Event` 类
- 属性：
  - `time`: 事件发生时间
  - `type`: 事件类型（开始服务/结束服务）
  - `entity_id`: 相关流实体ID
  - `activity_id`: 相关活动ID

#### 2.1.6 `EventCalendar` 类
- 方法：
  - `schedule_event(event)`: 安排事件
  - `get_next_event()`: 获取下一个事件
  - `remove_event(event_id)`: 移除事件

#### 2.1.7 `SimulationClock` 类
- 属性：
  - `current_time`: 当前模拟时间
- 方法：
  - `advance(time)`: 推进时间

#### 2.1.8 `SimulationEngine` 类
- 方法：
  - `initialize()`: 初始化模拟
  - `run(duration)`: 运行模拟
  - `process_begin_service_event(entity)`: 处理服务开始事件
  - `process_end_service_event(entity)`: 处理服务结束事件

### 2.2 模型模块（Model）

#### 2.2.1 `Activity` 类
- 属性：
  - `id`: 活动ID
  - `name`: 活动名称
  - `duration_function`: 持续时间函数
  - `required_resources`: 所需资源列表
  - `released_resources`: 释放资源列表
  - `generated_resources`: 生成资源列表
  - `successor_activities`: 后继活动列表

#### 2.2.2 `Model` 类
- 属性：
  - `activities`: 活动字典
  - `initial_flow_entities`: 初始流实体列表
  - `initial_resources`: 初始资源列表
- 方法：
  - `add_activity(activity)`: 添加活动
  - `add_flow_entity(entity)`: 添加初始流实体
  - `add_resource(resource)`: 添加初始资源
  - `validate()`: 验证模型

### 2.3 统计模块（Statistics）

#### 2.3.1 `ActivityStatistics` 类
- 属性：
  - `activity_id`: 活动ID
  - `completion_count`: 完成次数
  - `waiting_times`: 等待时间列表
  - `service_times`: 服务时间列表
- 方法：
  - `calculate_average_waiting_time()`: 计算平均等待时间
  - `calculate_average_service_time()`: 计算平均服务时间

#### 2.3.2 `ResourceStatistics` 类
- 属性：
  - `resource_id`: 资源ID
  - `busy_periods`: 忙碌时间段列表
  - `idle_periods`: 空闲时间段列表
- 方法：
  - `calculate_utilization_rate()`: 计算利用率

#### 2.3.3 `SimulationStatistics` 类
- 属性：
  - `activity_statistics`: 活动统计字典
  - `resource_statistics`: 资源统计字典
  - `total_simulation_time`: 总模拟时间
- 方法：
  - `export_to_csv(filename)`: 导出统计数据到CSV
  - `export_to_json(filename)`: 导出统计数据到JSON

### 2.4 可视化模块（Visualization）

#### 2.4.1 `GanttChart` 类
- 方法：
  - `plot(activities, resources)`: 绘制甘特图
  - `save(filename)`: 保存图表

#### 2.4.2 `ResourceUtilizationChart` 类
- 方法：
  - `plot(resource_statistics)`: 绘制资源利用率图表
  - `save(filename)`: 保存图表

#### 2.4.3 `SimulationAnimator` 类
- 方法：
  - `initialize(model)`: 初始化动画
  - `update(event)`: 更新动画
  - `save(filename)`: 保存动画

#### 2.4.4 `DashboardGenerator` 类
- 方法：
  - `create_dashboard(simulation_statistics)`: 创建仪表板
  - `save(filename)`: 保存仪表板

### 2.5 工具模块（Utils）

#### 2.5.1 `RandomGenerator` 类
- 方法：
  - `uniform(min, max)`: 生成均匀分布随机数
  - `normal(mean, std)`: 生成正态分布随机数
  - `beta(alpha, beta, min, max)`: 生成Beta分布随机数

#### 2.5.2 `DataImporter` 类
- 方法：
  - `import_from_csv(filename)`: 从CSV导入数据
  - `import_from_json(filename)`: 从JSON导入数据

#### 2.5.3 `Logger` 类
- 方法：
  - `info(message)`: 记录信息
  - `warning(message)`: 记录警告
  - `error(message)`: 记录错误

## 3. API接口设计

### 3.1 模型构建API

```python
# 创建模型
model = sdesa.Model(name="Road Construction")

# 添加活动
load_activity = sdesa.Activity(
    id="load",
    name="Load Truck",
    duration_function=lambda: sdesa.random.beta(2, 3, 5, 10),
    required_resources=["loader"],
    released_resources=["loader"],
    successor_activities=["travel"]
)
model.add_activity(load_activity)

# 添加初始流实体
for i in range(10):
    truck = sdesa.FlowEntity(
        id=f"truck_{i}",
        activity_id="load",
        arrival_time=0
    )
    model.add_flow_entity(truck)

# 添加初始资源
loader = sdesa.ResourceEntity(
    id="loader_1",
    type="loader",
    ready_time=0,
    available=True,
    disposable=False
)
model.add_resource(loader)
```

### 3.2 模拟执行API

```python
# 创建模拟引擎
engine = sdesa.SimulationEngine(model)

# 初始化模拟
engine.initialize()

# 运行模拟
statistics = engine.run(duration=480)  # 运行8小时模拟
```

### 3.3 结果分析API

```python
# 获取活动统计
activity_stats = statistics.get_activity_statistics("load")
avg_waiting_time = activity_stats.calculate_average_waiting_time()
avg_service_time = activity_stats.calculate_average_service_time()

# 获取资源统计
resource_stats = statistics.get_resource_statistics("loader_1")
utilization_rate = resource_stats.calculate_utilization_rate()

# 导出统计数据
statistics.export_to_csv("simulation_results.csv")
```

### 3.4 可视化API

```python
# 创建甘特图
gantt = sdesa.GanttChart()
gantt.plot(statistics.activity_statistics, statistics.resource_statistics)
gantt.save("gantt_chart.png")

# 创建资源利用率图表
util_chart = sdesa.ResourceUtilizationChart()
util_chart.plot(statistics.resource_statistics)
util_chart.save("resource_utilization.png")

# 创建动画
animator = sdesa.SimulationAnimator()
animator.initialize(model)
animator.replay(engine.event_log)
animator.save("simulation_animation.mp4")

# 创建仪表板
dashboard = sdesa.DashboardGenerator()
dashboard.create_dashboard(statistics)
dashboard.save("simulation_dashboard.html")
```

## 4. 依赖关系

SDESA Python库将依赖以下Python库：

- **NumPy**: 用于数学计算和数组操作
- **Pandas**: 用于数据处理和分析
- **Matplotlib**: 用于基本图表绘制
- **Plotly**: 用于交互式可视化
- **NetworkX**: 用于网络图和活动关系图
- **Dash**: 用于创建Web仪表板（可选）

## 5. 扩展性考虑

为了确保库的扩展性，我们将：

1. 使用抽象基类和接口定义核心组件
2. 提供钩子（hooks）和回调机制，允许用户自定义行为
3. 支持插件系统，允许用户扩展库的功能
4. 提供清晰的文档和示例，帮助用户理解如何扩展库

## 6. 性能考虑

为了确保库的性能，我们将：

1. 使用高效的数据结构（如堆）实现事件日历
2. 优化关键算法，如事件处理和资源分配
3. 使用NumPy进行数值计算，提高计算效率
4. 提供分析工具，帮助用户识别性能瓶颈
