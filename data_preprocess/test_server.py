#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

from server_with_logging import data_preprocess, get_order_categories, simulate_task_extraction

def test_functions():
    print("=== 测试服务器功能 ===")
    
    # 测试1: 获取订单分类
    print("\n1. 测试获取订单分类:")
    categories = get_order_categories()
    print(f"结果: {categories[:200]}...")  # 只显示前200个字符
    
    # 测试2: 模拟任务提取
    print("\n2. 测试模拟任务提取:")
    test_query = "我要调整订单ST-9012的配送时间"
    result = simulate_task_extraction(test_query)
    print(f"查询: {test_query}")
    print(f"结果: {result}")
    
    # 测试3: 数据预处理（可能会调用外部API）
    print("\n3. 测试数据预处理:")
    result = data_preprocess(test_query)
    print(f"查询: {test_query}")
    print(f"结果: {result}")

if __name__ == "__main__":
    test_functions()
