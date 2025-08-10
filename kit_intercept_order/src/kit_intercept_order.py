import requests
import json
from typing import Dict, Any, Optional
import logging
import time
import os
from mcp.server.fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建MCP服务器实例
mcp = FastMCP("kit-intercept-order")

@mcp.tool()    
def kit_intercept_order(order_id: str) -> str:
    """
    终止订单工具
    
    Args:
        order_id: 用户输入的查询的订单号，例如："ST-9012"
        
    Returns:
        str: 返回中断订单
    """
    return "intercept order "+ order_id +" has requested"

@mcp.tool()    
def kit_live_chat_support() -> str:
    """
    返回转人工的工具
    
    Returns:
        str: 专向人工支持
    """
    return "We will transfer you to a live support"

if __name__ == "__main__":
    logger.info("启动MCP数据预处理服务器")
    
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"服务器运行异常: {str(e)}")
        raise
