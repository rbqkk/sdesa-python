"""
SDESA Python库 - 建筑施工示例

该示例基于SDESA论文中的建筑施工案例，展示如何使用SDESA Python库进行离散事件模拟。
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# 添加库路径
sys.path.append('/home/ubuntu/sdesa_lib')

# 导入SDESA库
from sdesa.core import FlowEntity, ResourceEntity, Event
from sdesa.model import Activity, Model
from sdesa.engine import SimulationEngine
from sdesa.statistics import SimulationStatistics
from sdesa.utils import RandomGenerator
from sdesa.visualization import GanttChart, ResourceUtilizationChart, ActivityNetworkGraph, DashboardGenerator

# 设置随机数种子，确保结果可重现
RandomGenerator.set_seed(42)

def create_earthmoving_model():
    """
    创建土方工程模型
    
    基于SDESA论文中的土方工程案例，包括装载、运输、卸载和返回四个活动。
    
    返回:
        Model: 土方工程模型
    """
    print("创建土方工程模型...")
    
    # 创建模型
    model = Model(name="土方工程模型")
    
    # 定义活动
    # 1. 装载活动
    load_activity = Activity(
        id="load",
        name="装载",
        duration_function=lambda: RandomGenerator.triangular(5, 8, 12),
        required_resources=["loader"],
        released_resources=["loader"],
        successor_activities=["haul"]
    )
    
    # 2. 运输活动
    haul_activity = Activity(
        id="haul",
        name="运输",
        duration_function=lambda: RandomGenerator.triangular(15, 20, 30),
        required_resources=[],
        released_resources=[],
        successor_activities=["dump"]
    )
    
    # 3. 卸载活动
    dump_activity = Activity(
        id="dump",
        name="卸载",
        duration_function=lambda: RandomGenerator.triangular(3, 5, 8),
        required_resources=["spotter"],
        released_resources=["spotter"],
        successor_activities=["return"]
    )
    
    # 4. 返回活动
    return_activity = Activity(
        id="return",
        name="返回",
        duration_function=lambda: RandomGenerator.triangular(10, 15, 25),
        required_resources=[],
        released_resources=[],
        successor_activities=["load"]
    )
    
    # 添加活动到模型
    model.add_activity(load_activity)
    model.add_activity(haul_activity)
    model.add_activity(dump_activity)
    model.add_activity(return_activity)
    
    # 添加初始流实体（卡车）
    for i in range(5):
        truck = FlowEntity(
            id=f"truck_{i}",
            activity_id="load",
            arrival_time=0
        )
        model.add_flow_entity(truck)
    
    # 添加初始资源
    # 装载机
    loader = ResourceEntity(
        id="loader_1",
        type="loader",
        ready_time=0,
        available=True,
        disposable=False
    )
    
    # 指挥员
    spotter = ResourceEntity(
        id="spotter_1",
        type="spotter",
        ready_time=0,
        available=True,
        disposable=False
    )
    
    model.add_resource(loader)
    model.add_resource(spotter)
    
    # 验证模型
    if model.validate():
        print("模型验证成功！")
    else:
        print("模型验证失败！")
    
    return model

def run_simulation(model, duration=480):
    """
    运行模拟
    
    参数:
        model (Model): 模型对象
        duration (float, optional): 模拟持续时间，默认为480（8小时工作日）
    
    返回:
        SimulationEngine: 模拟引擎对象
    """
    print(f"运行模拟（持续时间：{duration}分钟）...")
    
    # 创建模拟引擎
    engine = SimulationEngine(model)
    
    # 运行模拟
    statistics = engine.run(duration=duration)
    
    # 打印模拟结果
    print(f"模拟完成！总模拟时间：{engine.clock.current_time:.2f}分钟")
    
    return engine

def analyze_results(engine):
    """
    分析模拟结果
    
    参数:
        engine (SimulationEngine): 模拟引擎对象
    """
    print("分析模拟结果...")
    
    # 获取统计数据
    stats = SimulationStatistics(
        activity_statistics=engine.statistics['activity_statistics'],
        resource_statistics=engine.statistics['resource_statistics'],
        total_simulation_time=engine.statistics['total_simulation_time']
    )
    
    # 打印资源利用率
    print("\n资源利用率:")
    for resource_id, resource_stats in stats.resource_statistics.items():
        utilization = resource_stats.calculate_utilization_rate(stats.total_simulation_time)
        print(f"  {resource_id}: {utilization:.2f}")
    
    # 打印活动完成次数
    print("\n活动完成次数:")
    for activity_id, activity_stats in stats.activity_statistics.items():
        print(f"  {activity_id}: {activity_stats.completion_count}")
    
    # 打印平均等待时间
    print("\n平均等待时间:")
    for activity_id, activity_stats in stats.activity_statistics.items():
        avg_waiting_time = activity_stats.calculate_average_waiting_time()
        print(f"  {activity_id}: {avg_waiting_time:.2f}分钟")
    
    # 打印平均服务时间
    print("\n平均服务时间:")
    for activity_id, activity_stats in stats.activity_statistics.items():
        avg_service_time = activity_stats.calculate_average_service_time()
        print(f"  {activity_id}: {avg_service_time:.2f}分钟")
    
    # 计算瓶颈活动
    bottlenecks = stats.calculate_bottleneck_activities()
    print("\n瓶颈活动（按等待时间排序）:")
    for activity_id, waiting_time in bottlenecks:
        print(f"  {activity_id}: {waiting_time:.2f}分钟")
    
    # 计算关键资源
    critical_resources = stats.calculate_critical_resources()
    print("\n关键资源（按利用率排序）:")
    for resource_id, utilization in critical_resources:
        print(f"  {resource_id}: {utilization:.2f}")
    
    return stats

def visualize_results(engine, stats, output_dir):
    """
    可视化模拟结果
    
    参数:
        engine (SimulationEngine): 模拟引擎对象
        stats (SimulationStatistics): 模拟统计对象
        output_dir (str): 输出目录
    
    返回:
        list: 生成的图表文件列表
    """
    print("可视化模拟结果...")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    files = []
    
    # 绘制甘特图
    gantt = GanttChart()
    gantt.plot(engine.event_log, engine.model.activities)
    gantt_file = os.path.join(output_dir, "gantt_chart.png")
    gantt.save(gantt_file)
    files.append(gantt_file)
    print(f"甘特图已保存到：{gantt_file}")
    
    # 绘制资源利用率图表
    resource_chart = ResourceUtilizationChart()
    resource_chart.plot(stats.resource_statistics)
    resource_file = os.path.join(output_dir, "resource_utilization.png")
    resource_chart.save(resource_file)
    files.append(resource_file)
    print(f"资源利用率图表已保存到：{resource_file}")
    
    # 绘制活动网络图
    network_graph = ActivityNetworkGraph()
    network_graph.plot(engine.model)
    network_file = os.path.join(output_dir, "activity_network.png")
    network_graph.save(network_file)
    files.append(network_file)
    print(f"活动网络图已保存到：{network_file}")
    
    # 创建仪表板
    dashboard = DashboardGenerator()
    dashboard.create_dashboard(stats)
    dashboard_file = os.path.join(output_dir, "simulation_dashboard.html")
    dashboard.save(dashboard_file)
    files.append(dashboard_file)
    print(f"仪表板已保存到：{dashboard_file}")
    
    # 导出统计数据
    csv_files = stats.export_to_csv(os.path.join(output_dir, "simulation"))
    files.extend(csv_files)
    print(f"统计数据已导出到CSV文件：{csv_files}")
    
    json_file = stats.export_to_json(os.path.join(output_dir, "simulation_results.json"))
    files.append(json_file)
    print(f"统计数据已导出到JSON文件：{json_file}")
    
    return files

def sensitivity_analysis(model, parameter_ranges, output_dir):
    """
    敏感性分析
    
    参数:
        model (Model): 模型对象
        parameter_ranges (dict): 参数范围字典
        output_dir (str): 输出目录
    """
    print("进行敏感性分析...")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 分析卡车数量对系统性能的影响
    if 'num_trucks' in parameter_ranges:
        truck_range = parameter_ranges['num_trucks']
        truck_results = []
        
        for num_trucks in truck_range:
            # 创建新模型
            new_model = Model(name=f"土方工程模型（{num_trucks}辆卡车）")
            
            # 复制活动
            for activity_id, activity in model.activities.items():
                new_model.add_activity(activity)
            
            # 添加卡车
            for i in range(num_trucks):
                truck = FlowEntity(
                    id=f"truck_{i}",
                    activity_id="load",
                    arrival_time=0
                )
                new_model.add_flow_entity(truck)
            
            # 复制资源
            for resource in model.initial_resources:
                new_model.add_resource(resource)
            
            # 运行模拟
            engine = SimulationEngine(new_model)
            engine.run(duration=480)
            
            # 获取统计数据
            stats = SimulationStatistics(
                activity_statistics=engine.statistics['activity_statistics'],
                resource_statistics=engine.statistics['resource_statistics'],
                total_simulation_time=engine.statistics['total_simulation_time']
            )
            
            # 计算总体资源利用率
            overall_utilization = stats.calculate_overall_resource_utilization()
            
            # 计算总完成次数
            total_completions = sum(stats.activity_statistics[activity_id].completion_count 
                                   for activity_id in stats.activity_statistics 
                                   if activity_id == 'dump')
            
            truck_results.append({
                'num_trucks': num_trucks,
                'overall_utilization': overall_utilization,
                'total_completions': total_completions
            })
        
        # 绘制敏感性分析图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # 资源利用率图表
        x = [result['num_trucks'] for result in truck_results]
        y1 = [result['overall_utilization'] for result in truck_results]
        ax1.plot(x, y1, 'o-', color='blue')
        ax1.set_xlabel('卡车数量')
        ax1.set_ylabel('资源利用率')
        ax1.set_title('卡车数量对资源利用率的影响')
        ax1.grid(True)
        
        # 完成次数图表
        y2 = [result['total_completions'] for result in truck_results]
        ax2.plot(x, y2, 'o-', color='green')
        ax2.set_xlabel('卡车数量')
        ax2.set_ylabel('完成次数')
        ax2.set_title('卡车数量对完成次数的影响')
        ax2.grid(True)
        
        plt.tight_layout()
        sensitivity_file = os.path.join(output_dir, "sensitivity_analysis.png")
        plt.savefig(sensitivity_file)
        print(f"敏感性分析图表已保存到：{sensitivity_file}")

def main():
    """
    主函数
    """
    print("SDESA Python库 - 建筑施工示例")
    print("=" * 50)
    
    # 创建输出目录
    output_dir = "/home/ubuntu/sdesa_lib/examples/output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建土方工程模型
    model = create_earthmoving_model()
    
    # 运行模拟
    engine = run_simulation(model)
    
    # 分析结果
    stats = analyze_results(engine)
    
    # 可视化结果
    visualize_results(engine, stats, output_dir)
    
    # 敏感性分析
    sensitivity_analysis(model, {'num_trucks': range(1, 11)}, output_dir)
    
    print("\n示例完成！所有结果已保存到：" + output_dir)

if __name__ == "__main__":
    main()
