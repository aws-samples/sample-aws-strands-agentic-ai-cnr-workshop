# AWS Strands MCP Workshop

A comprehensive workshop project demonstrating the implementation of Model Context Protocol (MCP) servers for various business scenarios. This project showcases how to build and integrate MCP servers with AI agents to handle real-world business workflows.

## 项目概述 / Project Overview

本项目包含多个MCP服务器实现，用于演示如何将业务逻辑封装为MCP协议服务，让AI代理能够理解和执行复杂的业务流程。本项目为workshop https://catalog.us-east-1.prod.workshops.aws/workshops/93a2eb2c-7f00-463a-92f1-ab0e6e81f48b/zh-CN 动手实践的工程代码。

This project contains multiple MCP server implementations that demonstrate how to encapsulate business logic as MCP protocol services, enabling AI agents to understand and execute complex business workflows.

## 功能模块 / Feature Modules

### 1. 数据预处理服务器 / Data Preprocessing Server (`data_preprocess/`)
- **功能**: 时间服务器，为AI代理提供当前时间信息
- **用途**: 让Agent能够获取准确的时间信息进行时间相关的决策
- **技术栈**: Python 3.12+, MCP 1.6.0+

### 2. 规则查询服务器 / Rule Query Server (`rule_query/`)
- **功能**: 订单规则查询和状态管理
- **主要工具**:
  - `rule_query_workflow`: 完整的规则查询工作流
  - `fetch_order_status`: 订单状态查询
  - `fetch_matched_rules`: 规则匹配查询
- **应用场景**: 电商订单管理、业务规则验证

### 3. 工具包拦截订单 / Kit Intercept Order (`kit_intercept_order/`)
- **功能**: 订单拦截和处理逻辑
- **用途**: 实现订单流程中的拦截和特殊处理机制

### 4. 工具包地址检查 / Kit Address Check (`kit_address_check/`)
- **功能**: 地址验证和检查服务
- **用途**: 确保订单配送地址的准确性和有效性

## 快速开始 / Quick Start

### 环境要求 / Prerequisites
- Python 3.12 或更高版本
- uv 包管理器（推荐）或 pip
- MCP 客户端（如 Claude Desktop 或其他支持MCP的AI客户端）

### 安装依赖 / Installation

1. 克隆项目到本地:
```bash
git clone <repository-url>
cd aws-strands-mcp-workshp
```

2. 安装全局依赖:
```bash
pip install -r requirements.txt
```

3. 为每个模块安装特定依赖:
```bash
# 数据预处理模块
cd data_preprocess
uv sync

# 规则查询模块  
cd ../rule_query
uv sync

# 其他模块类似...
```

### 配置MCP客户端 / MCP Client Configuration

在你的MCP客户端配置文件中添加服务器配置：

```json
{
  "mcpServers": {
    "time-server": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/aws-strands-mcp-workshp/data_preprocess",
        "run", "server.py"
      ]
    },
    "rule-query-server": {
      "command": "uv", 
      "args": [
        "--directory", "/path/to/aws-strands-mcp-workshp/rule_query",
        "run", "server.py"
      ]
    }
  }
}
```

## 使用示例 / Usage Examples

### 时间查询示例
```python
# AI代理可以通过MCP调用获取当前时间
current_time = await time_server.get_current_time()
```

### 订单规则查询示例
```python
# 查询订单状态和适用规则
result = await rule_query_server.rule_query_workflow(
    order_id="ST-9012",
    purpose="修改配送时间"
)
```

## 项目结构 / Project Structure

```
aws-strands-mcp-workshp/
├── data_preprocess/          # 数据预处理MCP服务器
│   ├── src/                  # 源代码
│   ├── pyproject.toml        # 项目配置
│   └── README.md            # 模块说明
├── rule_query/              # 规则查询MCP服务器
│   ├── src/                 # 源代码
│   ├── README_MCP.md        # MCP服务器文档
│   └── pyproject.toml       # 项目配置
├── kit_intercept_order/     # 订单拦截工具包
├── kit_address_check/       # 地址检查工具包
├── requirements.txt         # 全局依赖
└── README.md               # 项目主文档
```

## 开发指南 / Development Guide

### 添加新的MCP服务器

1. 在项目根目录创建新的模块文件夹
2. 实现MCP服务器逻辑
3. 配置 `pyproject.toml`
4. 编写相应的README文档
5. 更新主配置文件

### 测试

每个模块都包含测试用例，可以独立运行：

```bash
cd <module_directory>
python test_server.py
```

## API文档 / API Documentation

详细的API文档请参考各个模块的README文件：
- [数据预处理服务器](./data_preprocess/README.md)
- [规则查询服务器](./rule_query/README_MCP.md)

## 技术栈 / Tech Stack

- **语言**: Python 3.12+
- **协议**: Model Context Protocol (MCP)
- **包管理**: uv / pip
- **HTTP客户端**: requests
- **异步支持**: asyncio

**注意**: 本项目为教学演示用途，生产环境使用前请进行充分测试和安全评估。

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

