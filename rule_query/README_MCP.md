# Rule Query MCP Server

这是一个基于MCP（Model Context Protocol）协议的规则查询服务器，将原有的 `rule_query.py` 功能转换为MCP服务器模式。

## 功能特性

- **规则查询工作流**: 完整的订单规则查询流程
- **订单状态查询**: 获取指定订单的状态信息
- **规则匹配**: 根据查询目的获取匹配的规则
- **异步处理**: 支持异步操作，提高性能

## 安装依赖

```bash
pip install -r requirements.txt
```

## 可用工具

### 1. rule_query_workflow
执行完整的规则查询工作流

**参数:**
- `order_id` (string, 必需): 订单ID
- `purpose` (string, 必需): 查询目的

**示例:**
```json
{
  "order_id": "ST-9012",
  "purpose": "修改配送时间"
}
```

### 2. fetch_order_status
获取指定订单的状态信息

**参数:**
- `order_id` (string, 必需): 订单ID

**示例:**
```json
{
  "order_id": "ST-9012"
}
```

### 3. fetch_matched_rules
根据查询目的获取匹配的规则

**参数:**
- `purpose` (string, 必需): 查询目的

**示例:**
```json
{
  "purpose": "修改配送时间"
}
```

## 启动服务器

### 直接启动
```bash
python mcp_rule_query_server.py
```

### 作为MCP服务器启动
1. 将 `mcp_config.json` 配置添加到你的MCP客户端配置中
2. 启动MCP客户端，服务器将自动启动

## 配置文件

`mcp_config.json` 包含了MCP服务器的配置信息：

```json
{
  "mcpServers": {
    "rule-query-server": {
      "command": "python",
      "args": ["mcp_rule_query_server.py"],
      "cwd": "/path/to/your/project",
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      }
    }
  }
}
```

## 工作流程

1. **获取订单状态**: 调用API获取订单的当前状态
2. **验证订单存在性**: 检查订单是否存在（状态码200）
3. **获取匹配规则**: 根据查询目的获取相关规则
4. **过滤规则**: 基于订单状态和业务逻辑过滤规则
5. **返回结果**: 返回格式化的查询结果

## API端点

- 订单状态查询: `https://xxxxxxxxxx/prod/kit_box/order_status`
- 规则匹配查询: `https://xxxxxxxxxx/prod/purpose`

## 错误处理

服务器包含完善的错误处理机制：
- 参数验证
- API调用异常处理
- 超时处理
- 详细的错误日志

## 日志

服务器使用Python的logging模块记录运行日志，包括：
- API调用响应
- 错误信息
- 工具执行状态

## 注意事项

1. 当前版本在异步环境中仍使用 `requests` 库，生产环境建议替换为 `aiohttp`
2. 规则过滤逻辑为简化版本，实际使用时可能需要集成LLM API
3. 确保网络连接正常，能够访问API端点

## 测试

可以使用原有的测试用例来验证MCP服务器的功能：

```python
# 测试用例
test_cases = [
    {"order_id": "ST-9012", "purpose": "修改配送时间"},
    {"order_id": "nonexistent", "purpose": "取消订单"},
    {"order_id": "ABC123", "purpose": "修改订单"},
]
```

## 扩展

可以根据需要添加更多工具：
- 订单创建
- 订单修改
- 规则管理
- 统计分析等
