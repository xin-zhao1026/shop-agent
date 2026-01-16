import sqlite3
from typing import Dict, List, Optional
from datetime import datetime
from langchain.tools import tool
import json


def get_db_connection():
    """
    获取数据库连接

    Returns:
        sqlite3.Connection: 数据库连接对象
    """
    conn = sqlite3.connect(
        'E:/code/python/agent_demo/shop_agent/data/orders.db')
    return conn


@tool(description='根据订单号获取订单状态')
def get_order_status(order_id: str) -> Optional[Dict]:
    """
    根据订单号获取订单状态

    Args:
        order_id (str): 订单ID,订单的唯一标识

    Returns:
        Optional[Dict]: 包含订单状态信息，订单号、用户ID、商品名称、数量、总价、订单状态、物流单号、预计达到时间、发货时间
                        如果订单不存在则返回None
    """
    # order_id = json.loads(order_id).get('order_id')
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT order_id, user_id, product_name, quantity, total_price, 
                   order_status, tracking_number, estimated_delivery, order_date 
            FROM orders 
            WHERE order_id = ?
        """, (order_id,))

        row = cursor.fetchone()
        if row:
            return {
                'order_id': order_id,
                'user_id': row[1],
                'product_name': row[2],
                'quantity': row[3],
                'total_price': row[4],
                'order_status': row[5],
                'tracking_number': row[6],
                'estimated_delivery': row[7],
                'order_date': row[8]
            }
        return None
    finally:
        conn.close()


@tool
def return_order(order_id: str) -> bool:
    """
    退订单

    Args:
        order_id (str): 订单ID

    Returns:
        bool: 退货操作是否成功
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 首先检查订单是否存在以及当前状态
        cursor.execute(
            "SELECT order_status FROM orders WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()

        if not row:
            return False  # 订单不存在

        current_status = row[0]

        # 检查订单是否可以退货
        if current_status in ['已完成', '已发货']:
            # 更新订单状态为"退货中"
            cursor.execute(
                "UPDATE orders SET order_status = '退货中' WHERE order_id = ?", (order_id,))
            conn.commit()
            return True
        elif current_status == '退货中':
            # 订单已经在退货中
            return True
        else:
            # 订单状态不允许退货
            return False
    finally:
        conn.close()


@tool
def complain_order(order_id: str, complaint_reason: str) -> bool:
    """
    投诉订单

    Args:
        order_id (str): 订单ID
        complaint_reason (str): 投诉原因

    Returns:
        bool: 投诉是否成功提交
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 检查订单是否存在以及当前状态
        cursor.execute(
            "SELECT order_status FROM orders WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()

        if not row:
            return False  # 订单不存在

        current_status = row[0]

        # 如果订单状态是"待付款"，不能投诉
        if current_status == '待付款':
            return False

        # 不再保存投诉内容，直接返回成功
        return True
    finally:
        conn.close()


if __name__ == '__main__':
    # 测试代码
    # print(get_order_status('OD1008'))
    # print(return_order('OD1002'))
    print(complain_order('OD1008', '商品质量问题'))
