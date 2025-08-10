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

API_ENDPOINT = os.getenv('API_ENDPOINT')

address_check_url = API_ENDPOINT + "/kit_box/address_check"
max_retries = 3
retry_interval = 0.1  # 100ms
timeout = 30

# 创建MCP服务器实例
mcp = FastMCP("kit-address-check")

# 从环境变量获取API密钥
def get_api_key():
    """获取硅基流动API密钥"""
    api_key = os.getenv('SILICONFLOW_API_KEY')
    if not api_key:
        print("警告: 未设置环境变量 SILICONFLOW_API_KEY")
        print("请运行: export SILICONFLOW_API_KEY='your_api_key_here'")
    return api_key

def get_original_address(order_id: str) -> Dict[str, Any]:
    """
    Get original address by order_id
        
    Args:
        order_id (str): The order ID to query
            
    Returns:
        Dict containing the API response
    """
    params = {"order_id": order_id}
        
    for attempt in range(max_retries):
        try:
            logger.info(f"Getting original address for order_id: {order_id}, attempt: {attempt + 1}")
            response = requests.get(
                address_check_url,
                params=params,
                timeout=30
            )
                
            return {
                "status_code": response.status_code,
                "body": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "headers": dict(response.headers),
                "success": response.status_code == 200
            }
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed on attempt {attempt + 1}: {str(e)}")
            if attempt == self.max_retries - 1:
                raise
    
def compare_addresses_with_llm(original_address_data: Any, input_address: str) -> str:
    """
    Compare addresses using LLM (simulated)
    In a real implementation, this would call DeepSeek-V3 via SiliconFlow
        
    Args:
        original_address_data: Original address data from API
        input_address: New input address to compare
            
    Returns:
        Comparison result string
    """
    system_prompt = "你是一个地址检查助手"
    user_prompt = f"""请提取{json.dumps(original_address_data)}中的地址，并检查是否和{input_address}是指代相同的地址，

输出的结果只包含下面两种情况，不要包括中间思考信息和其他任何内容

如果相同，返回

"待更改地址与原地址相同，无需更改"

如果不同，返回

"地址更新，将尝试拦截订单，并转人工客服处理"。

"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
        
    logger.info("Simulating LLM address comparison...")
    logger.info(f"System prompt: {system_prompt}")
    logger.info(f"User prompt: {user_prompt}")
        
    # 调用DeepSeek API
    response_content = call_siliconflow_deepseek(messages, temperature=0.7)
    
    if not response_content:
        # 如果API调用失败，使用备用方案
        # Simplified address comparison logic (replace with actual LLM call)
        if isinstance(original_address_data, dict):
            # Extract address information from the response
            original_address = _extract_address_from_data(original_address_data)
            # Simple comparison logic
            if _addresses_are_similar(original_address, input_address):
                return "待更改地址与原地址相同，无需更改"
            else:
                return "地址更新，将尝试拦截订单，并转人工客服处理"
    else:
        cleaned_content = response_content.strip()
        if cleaned_content.startswith('```json'):
            cleaned_content = cleaned_content[7:]
        if cleaned_content.endswith('```'):
            cleaned_content = cleaned_content[:-3]
        cleaned_content = cleaned_content.strip()
        
        result = json.loads(cleaned_content)
        return result
    return "地址更新，将尝试拦截订单，并转人工客服处理"

def call_siliconflow_deepseek(messages: list, temperature: float = 0.7) -> Optional[str]:
    """
    调用硅基流动 DeepSeek API
    
    Args:
        messages (list): 对话消息列表
        temperature (float): 温度参数，控制输出随机性
        
    Returns:
        Optional[str]: API响应内容
    """
    
    # 从环境变量获取API密钥
    api_key = os.getenv('SILICONFLOW_API_KEY')
    if not api_key:
        raise ValueError("请设置环境变量 SILICONFLOW_API_KEY")
    
    url = "https://api.siliconflow.cn/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2000,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        print(f"DeepSeek API调用失败: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"解析API响应失败: {e}")
        return None
        
def _extract_address_from_data(data: Dict[str, Any]) -> str:
    """Extract address from API response data"""
    # Try to find address in common fields
    possible_fields = ['address', 'shipping_address', 'delivery_address', 'addr', 'location']
        
    for field in possible_fields:
        if field in data:
            return str(data[field])
        
    # If no specific address field found, return the whole data as string
    return json.dumps(data, ensure_ascii=False)
    
def _addresses_are_similar(addr1: str, addr2: str) -> bool:
    """Simple address similarity check"""
    # Remove spaces and convert to lowercase for basic comparison
    addr1_clean = addr1.replace(" ", "").lower()
    addr2_clean = addr2.replace(" ", "").lower()
        
    # Simple similarity check - in real implementation, use more sophisticated logic
    return addr1_clean == addr2_clean or addr1_clean in addr2_clean or addr2_clean in addr1_clean
    
@mcp.tool()    
def check_address(order_id: str, input_address: str) -> Dict[str, Any]:
    """
    Main method to check address difference
    Implements the complete workflow from kit_address_check.yml
        
    Args:
        order_id (str): The order ID to query
        input_address (str): The new address to compare
            
    Returns:
        Dict containing the comparison result
    """
    try:
        # Step 1: Get original address from API
        logger.info(f"Starting address check for order_id: {order_id}, input_address: {input_address}")
        address_response = get_original_address(order_id)
            
        if not address_response["success"]:
            return {
                "success": False,
                "error": f"Failed to get original address: HTTP {address_response['status_code']}",
                "result": "无法获取原地址信息，请检查订单ID",
                "api_response": address_response
            }
            
        # Step 2: Compare addresses using LLM
        comparison_result = compare_addresses_with_llm(
            address_response["body"],
            input_address
        )
        
        return comparison_result
            
        #return {
        ##    "success": True,
        #    "result": comparison_result,
        #    "original_address_data": address_response["body"],
        #    "input_address": input_address,
        ##    "api_response": address_response
        #}
            
    except Exception as e:
        logger.error(f"Error in address check: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "result": "地址检查过程中发生错误，请稍后重试"
        }

#def main():
    # Example 1: Check address for a valid order
#    print("=== Example 1: Address check for valid order ===")
#    result1 = check_address("CD-5678", "南京西路888号")
#    print(json.dumps(result1, ensure_ascii=False, indent=2))

# 硅基流动 API 配置
SILICONFLOW_CONFIG = {
    "api_url": "https://api.siliconflow.cn/v1/chat/completions",
    "model": "deepseek-ai/DeepSeek-V3",
    "max_tokens": 2000,
    "timeout": 60
}

if __name__ == "__main__":
    logger.info("启动MCP数据预处理服务器")
    logger.info(f"服务器配置: {SILICONFLOW_CONFIG}")
    
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"服务器运行异常: {str(e)}")
        raise
