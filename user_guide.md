# SDESA Python库使用指南

## 简介

SDESA（简化离散事件模拟方法）Python库是一个用于离散事件模拟的工具包，基于Ming Lu在2003年提出的SDESA方法论。该库提供了一套简单而强大的工具，用于模拟和分析复杂的建筑施工系统和其他离散事件系统。

SDESA方法的核心思想是通过简化传统离散事件模拟方法，使其更易于使用，同时保持足够的灵活性和功能性。与传统的CPM（关键路径法）相比，SDESA能够处理循环过程、动态排队现象、跟踪单个资源性能，以及适应复杂的逻辑或技术约束。

## 安装

```bash
pip install sdesa
```

## 基本概念

SDESA模拟方法基于以下核心概念：

1. **流实体（Flow Entity）**：在系统中流动的实体，如卡车、道路部分等。
2. **资源实体（Resource Entity）**：被流实体使用的资源，如装载机、旗手等。
3. **活动（Activity）**：系统中的基本操作单元，如装载、运输、卸载等。
4. **事件（Event）**：模拟过程中的关键点，包括服务开始事件和服务结束事件。

## 快速入门

以下是一个简单的例子，展示如何使用SDESA库模拟一个基本的建筑施工系统：

```python
import sdesa
from sdesa.utils import random_generator

# 创建模型
model = sdesa.Model(name="简单建筑施工系统")

# 定义活动
load_activity = sdesa.Activity(
    id="load",
    name="装载卡车",
    duration_function=lambda: random_generator.triangular(5, 8, 12),
    required_resources=["loader"],
    released_resources=["loader"],
    successor_activities=["travel"]
)

travel_activity = sdesa.Activity(
    id="travel",
    name="运输",
    duration_function=lambda: random_generator.triangular(15, 20, 30),
    required_resources=[],
    released_resources=[],
    successor_activities=["dump"]
)

dump_activity = sdesa.Activity(
    id="dump",
    name="卸载",
    duration_function=lambda: random_generator.triangular(3, 5, 8),
    required_resources=["flagman"],
    released_resources=["flagman"],
    generated_resources=["truckload"],
    successor_activities=["return"]
)

return_activity = sdesa.Activity(
    id="return",
    name="返回",
    duration_function=lambda: random_generator.triangular(10, 15, 25),
    required_resources=[],
    released_resources=[],
    successor_activities=["load"]
)

# 添加活动到模型
model.add_activity(load_activity)
model.add_activity(travel_activity)
model.add_activity(dump_activity)
model.add_activity(return_activity)

# 添加初始流实体（卡车）
for i in range(5):
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

flagman = sdesa.ResourceEntity(
    id="flagman_1",
    type="flagman",
    ready_time=0,
    available=True,
    disposable=False
)

model.add_resource(loader)
model.add_resource(flagman)

# 创建模拟引擎
engine = sdesa.SimulationEngine(model)

# 运行模拟（8小时工作日）
statistics = engine.run(duration=480)

# 分析结果
print(f"总模拟时间: {statistics.total_simulation_time:.2f} 分钟")
print("\n资源利用率:")
for resource_id, stats in statistics.resource_statistics.items():
    utilization = stats.calculate_utilization_rate(statistics.total_simulation_time)
    print(f"  {resource_id}: {utilization:.2f}")

print("\n活动完成次数:")
for activity_id, stats in statistics.activity_statistics.items():
    print(f"  {activity_id}: {stats.completion_count}")

# 可视化结果
gantt = sdesa.GanttChart()
gantt.plot(engine.event_log, model.activities)
gantt.save("gantt_chart.png")

resource_chart = sdesa.ResourceUtilizationChart()
resource_chart.plot(statistics.resource_statistics)
resource_chart.save("resource_utilization.png")

dashboard = sdesa.DashboardGenerator()
dashboard.create_dashboard(statistics)
dashboard.save("simulation_dashboard.html")
```

## 模块概述

SDESA Python库由以下主要模块组成：

### 核心模块 (sdesa.core)

提供基本的数据结构和算法，包括：
- `FlowEntity`：流实体类
- `ResourceEntity`：资源实体类
- `FlowEntityQueue`：流实体队列类
- `ResourceEntityQueue`：资源实体队列类
- `Event`：事件类
- `EventCalendar`：事件日历类
- `SimulationClock`：模拟时钟类

### 模型模块 (sdesa.model)

提供模型定义和构建功能，包括：
- `Activity`：活动类
- `Model`：模型类

### 模拟引擎 (sdesa.engine)

提供模拟执行功能，包括：
- `SimulationEngine`：模拟引擎类

### 统计模块 (sdesa.statistics)

提供统计分析功能，包括：
- `ActivityStatistics`：活动统计类
- `ResourceStatistics`：资源统计类
- `SimulationStatistics`：模拟统计类

### 工具模块 (sdesa.utils)

提供辅助功能，包括：
- `RandomGenerator`：随机数生成器类
- `Logger`：日志记录器类
- `DataImporter`：数据导入器类

### 可视化模块 (sdesa.visualization)

提供可视化功能，包括：
- `GanttChart`：甘特图类
- `ResourceUtilizationChart`：资源利用率图表类
- `ActivityNetworkGraph`：活动网络图类
- `SimulationAnimator`：模拟动画类
- `DashboardGenerator`：仪表板生成器类

## 高级用法

### 自定义持续时间分布

SDESA库支持多种概率分布来模拟活动持续时间：

```python
from sdesa.utils import random_generator

# 均匀分布
duration_uniform = lambda: random_generator.uniform(5, 10)

# 正态分布
duration_normal = lambda: random_generator.normal(7, 1.5)

# 三角分布
duration_triangular = lambda: random_generator.triangular(5, 7, 10)

# 指数分布
duration_exponential = lambda: random_generator.exponential(0.2)

# Beta分布
duration_beta = lambda: random_generator.beta(2, 3, 5, 10)
```

### 资源约束和优先级

可以通过设置活动的优先级来控制资源分配：

```python
# 高优先级活动
high_priority_activity = sdesa.Activity(
    id="high_priority",
    name="高优先级活动",
    duration_function=lambda: random_generator.triangular(5, 8, 12),
    required_resources=["critical_resource"],
    released_resources=["critical_resource"],
    successor_activities=[],
    priority=10  # 高优先级
)

# 低优先级活动
low_priority_activity = sdesa.Activity(
    id="low_priority",
    name="低优先级活动",
    duration_function=lambda: random_generator.triangular(3, 5, 8),
    required_resources=["critical_resource"],
    released_resources=["critical_resource"],
    successor_activities=[],
    priority=1  # 低优先级
)
```

### 导出和分析结果

SDESA库提供了多种方式来导出和分析模拟结果：

```python
# 导出到CSV
statistics.export_to_csv("simulation_results")

# 导出到JSON
statistics.export_to_json("simulation_results.json")

# 分析瓶颈活动
bottlenecks = statistics.calculate_bottleneck_activities()
print("瓶颈活动（按等待时间排序）:")
for activity_id, waiting_time in bottlenecks:
    print(f"  {activity_id}: {waiting_time:.2f}")

# 分析关键资源
critical_resources = statistics.calculate_critical_resources()
print("关键资源（按利用率排序）:")
for resource_id, utilization in critical_resources:
    print(f"  {resource_id}: {utilization:.2f}")
```

## 最佳实践

1. **模型验证**：在运行完整模拟之前，使用`model.validate()`方法验证模型的有效性。

2. **随机数种子**：为了确保模拟结果的可重复性，可以设置随机数种子：
   ```python
   from sdesa.utils import random_generator
   random_generator.set_seed(42)
   ```

3. **多次运行**：为了获得统计上有意义的结果，建议多次运行模拟并分析平均结果。

4. **增量开发**：从简单模型开始，逐步添加复杂性，这样更容易调试和理解模型行为。

5. **日志记录**：使用`Logger`类记录模拟过程中的关键事件，有助于调试和分析。

## 常见问题

**Q: 如何处理资源不可用的情况？**

A: 当资源不可用时，模拟引擎会尝试处理下一个流实体。一旦资源变为可用，引擎会重新尝试处理之前跳过的流实体。

**Q: 如何模拟资源故障或维护？**

A: 可以通过在特定时间点更新资源的可用性来模拟故障或维护：
```python
# 在模拟过程中安排资源维护
maintenance_event = sdesa.Event(
    time=240,  # 4小时后
    type="maintenance",
    entity_id="loader_1",
    activity_id=None
)
engine.event_calendar.schedule_event(maintenance_event)

# 在处理事件时检查维护事件
if event.type == "maintenance":
    engine.resource_entity_queue.update_entity(
        event.entity_id, 
        available=False
    )
    # 安排维护结束事件
    end_maintenance = sdesa.Event(
        time=event.time + 60,  # 维护持续1小时
        type="end_maintenance",
        entity_id=event.entity_id,
        activity_id=None
    )
    engine.event_calendar.schedule_event(end_maintenance)
elif event.type == "end_maintenance":
    engine.resource_entity_queue.update_entity(
        event.entity_id, 
        available=True
    )
```

**Q: 如何处理条件分支？**

A: 可以使用自定义的决策函数来确定后继活动：
```python
def decide_next_activity(entity):
    # 基于某些条件决定下一个活动
    if some_condition:
        return "activity_a"
    else:
        return "activity_b"

# 在处理服务结束事件时使用决策函数
next_activity = decide_next_activity(entity)
new_entity = sdesa.FlowEntity(
    id=f"{entity.id}_{next_activity}",
    activity_id=next_activity,
    arrival_time=engine.clock.current_time
)
engine.flow_entity_queue.add_entity(new_entity)
```

## 参考资料

- Lu, M. (2003). Simplified Discrete-Event Simulation Approach for Construction Simulation. Journal of Construction Engineering and Management, 129(5), 537-546.
- SDESA Python库API文档：[链接到API文档]
- 更多示例和教程：[链接到示例库]
