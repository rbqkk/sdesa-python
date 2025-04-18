# SDESA Python库

基于SDESA（简化离散事件模拟方法）的Python库，用于建筑施工和其他离散事件系统的模拟。

## 简介

SDESA（简化离散事件模拟方法）Python库是一个用于离散事件模拟的工具包，基于Ming Lu在2003年提出的SDESA方法论。该库提供了一套简单而强大的工具，用于模拟和分析复杂的建筑施工系统和其他离散事件系统。

SDESA方法的核心思想是通过简化传统离散事件模拟方法，使其更易于使用，同时保持足够的灵活性和功能性。与传统的CPM（关键路径法）相比，SDESA能够处理循环过程、动态排队现象、跟踪单个资源性能，以及适应复杂的逻辑或技术约束。

## 安装

```bash
pip install sdesa
```

或者从源代码安装：

```bash
git clone https://github.com/rbqkk/sdesa-python.git
cd sdesa-python
pip install -e .
```

## 主要特性

- **简单而强大的API**：易于学习和使用，同时提供足够的灵活性
- **完整的模拟功能**：支持流实体、资源实体、活动和事件
- **丰富的统计分析**：收集和分析模拟结果
- **多种可视化选项**：甘特图、资源利用率图表、活动网络图和交互式仪表板
- **扩展性**：易于扩展和定制

## 快速入门

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

# 添加活动到模型
model.add_activity(load_activity)

# 添加初始流实体
truck = sdesa.FlowEntity(
    id="truck_1",
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

# 创建模拟引擎
engine = sdesa.SimulationEngine(model)

# 运行模拟
statistics = engine.run(duration=480)

# 可视化结果
gantt = sdesa.GanttChart()
gantt.plot(engine.event_log, model.activities)
gantt.save("gantt_chart.png")
```

## 文档

详细文档请参阅：

- [用户指南](docs/user_guide.md)
- [API参考文档](docs/api_reference.md)
- [示例](examples/)

## 示例

库中包含了多个示例，展示如何使用SDESA库进行不同类型的模拟：

- [建筑施工示例](examples/construction_example.py)：基于论文中的土方工程案例

## 依赖项

- Python 3.6+
- numpy
- pandas
- matplotlib
- networkx
- plotly

## 许可证

MIT

## 参考文献

- Lu, M. (2003). Simplified Discrete-Event Simulation Approach for Construction Simulation. Journal of Construction Engineering and Management, 129(5), 537-546.
#   s d e s a - p y t h o n 
 
 #   s d e s a - p y t h o n 
 
 
