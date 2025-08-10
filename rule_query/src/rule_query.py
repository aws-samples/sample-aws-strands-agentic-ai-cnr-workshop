import requests
import json
from typing import Dict, Any, Optional
import os
import sys
import logging
from mcp.server.fastmcp import FastMCP, Context

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/aws-strands-mcp-workshp/data_preprocess/server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

mcp = FastMCP("rule-query-server")

# 硅基流动 API 配置
SILICONFLOW_CONFIG = {
    "api_url": "https://api.siliconflow.cn/v1/chat/completions",
    "model": "deepseek-ai/DeepSeek-V3",
    "max_tokens": 2000,
    "timeout": 60
}
API_ENDPOINT = os.getenv('API_ENDPOINT')

ORDER_STATUS_URL = API_ENDPOINT + "/kit_box/order_status"
PURPOSE_URL = API_ENDPOINT + "/purpose"

# 从环境变量获取API密钥
def get_api_key():
    """获取硅基流动API密钥"""
    api_key = os.getenv('SILICONFLOW_API_KEY')
    if not api_key:
        print("警告: 未设置环境变量 SILICONFLOW_API_KEY")
        print("请运行: export SILICONFLOW_API_KEY='your_api_key_here'")
    return api_key


def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Get order status by order_id

    Args:
        order_id (str): The order ID to query
            
    Returns:
        Dict containing the API response
    """
    params = {"order_id": order_id}
        
    for attempt in range(3):
        try:
            response = requests.get(
                ORDER_STATUS_URL,
                params=params,
                timeout=30
            )
            
            return {
                "status_code": response.status_code,
                "body": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "headers": dict(response.headers)
            }
                
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                raise

def get_matched_rule(purpose: str) -> Dict[str, Any]:
    """
    Get matched rule by purpose
        
    Args:
        purpose (str): The purpose to query rules for
            
    Returns:
        Dict containing the API response
    """
    params = {"purpose": purpose}
    for attempt in range(3):
        try:
            response = requests.get(
                PURPOSE_URL,
                params=params,
                timeout=30
        )
                
            return {
                "status_code": response.status_code,
                "body": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "headers": dict(response.headers)
            }
                
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                raise

@mcp.tool()
def query_rule(order_id: str, purpose: str) -> Dict[str, Any]:
    """
    Main method to query matched rule based on order_id and purpose
    Implements the complete workflow from rule_query.yml
        
    Args:
        order_id (str): The order ID to query
        purpose (str): The purpose for rule matching
            
    Returns:
        Dict containing the final result
    """
    try:
        # Step 1: Get order status
        order_status_response = get_order_status(order_id)
        # Step 2: Check if order exists (status code = 200)
        if order_status_response["status_code"] == 200:
            # Step 3: Get matched rule
            rule_response = get_matched_rule(purpose)
            # Step 4: Filter rule using LLM
            filtered_rule = filter_rule_with_llm(
                rule_response["body"], 
                order_status_response["body"]
            )

            print(filtered_rule)

            return filtered_rule
        else:
            # Order doesn't exist
            return {
                "success": False,
                "result": "order_id is not exist, please check",
                "order_status": order_status_response
            }
                
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "result": "An error occurred while processing the request"
        }

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

def filter_rule_with_llm(rule_data: Any, order_status_data: Any) -> str:
    """
    Simulate LLM filtering of rules based on order status
    In a real implementation, this would call an actual LLM service
        
    Args:
        rule_data: Rule definition data
        order_status_data: Order status data for filtering
            
    Returns:
        Filtered rule in JSON format
    """
    # This is a simplified simulation of the LLM processing
    # In the actual workflow, this would call DeepSeek-V3 via SiliconFlow
        
    system_prompt = "you are an rule filter, your task is to filter rule based on input status"
    user_prompt = f"""rule definition is in {json.dumps(rule_data)}, filter condition is in {json.dumps(order_status_data)}

please just output matched rule, do not include purpose and status, expected format as below

{{"规则": {{rule_detail}}}}"""
        
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response_content = call_siliconflow_deepseek(messages, temperature=0.7)

    # Simplified rule matching logic (replace with actual LLM call)
    #if isinstance(rule_data, dict) and isinstance(order_status_data, dict):
        # Extract relevant rule information
    #    filtered_rule = {
    #        "规则": {
    #            "matched_rule": "Based on order status and purpose",
    #            "rule_data": rule_data,
    #            "filter_condition": order_status_data
    #        }
    #    }
    return json.dumps(response_content, ensure_ascii=False, indent=2)    
    

if __name__ == "__main__":
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"服务器运行异常: {str(e)}")
        raise