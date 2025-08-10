#!/bin/bash

echo "=== MCP服务器日志查看工具 ==="
echo ""

LOG_FILE="/home/ubuntu/aws-strands-mcp-workshp/data_preprocess/server.log"

case "${1:-help}" in
    "tail")
        echo "实时查看日志 (按Ctrl+C退出):"
        echo "================================"
        tail -f "$LOG_FILE"
        ;;
    "last")
        echo "查看最后20行日志:"
        echo "================================"
        if [ -f "$LOG_FILE" ]; then
            tail -20 "$LOG_FILE"
        else
            echo "日志文件不存在: $LOG_FILE"
        fi
        ;;
    "all")
        echo "查看所有日志:"
        echo "================================"
        if [ -f "$LOG_FILE" ]; then
            cat "$LOG_FILE"
        else
            echo "日志文件不存在: $LOG_FILE"
        fi
        ;;
    "clear")
        echo "清空日志文件..."
        > "$LOG_FILE"
        echo "日志文件已清空"
        ;;
    "run")
        echo "启动服务器并显示日志:"
        echo "================================"
        cd /home/ubuntu/aws-strands-mcp-workshp/data_preprocess
        uv run src/server.py
        ;;
    "test")
        echo "运行测试并查看日志:"
        echo "================================"
        cd /home/ubuntu/aws-strands-mcp-workshp/data_preprocess
        uv run test_server.py
        ;;
    *)
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  tail    - 实时查看日志"
        echo "  last    - 查看最后20行日志"
        echo "  all     - 查看所有日志"
        echo "  clear   - 清空日志文件"
        echo "  run     - 启动服务器并显示日志"
        echo "  test    - 运行测试并查看日志"
        echo ""
        echo "示例:"
        echo "  $0 tail     # 实时查看日志"
        echo "  $0 last     # 查看最近的日志"
        echo "  $0 test     # 运行测试"
        ;;
esac
