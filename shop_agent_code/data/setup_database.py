import sqlite3
import json
import os

from config import setting


def setup_database():
    db_path = setting.DB_PATH
    json_path = setting.ORDER_FILE
    # 连接到SQLite数据库（如果不存在会自动创建）
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建订单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_id TEXT,
            product_name TEXT,
            quantity INTEGER,
            total_price REAL,
            order_status TEXT,
            tracking_number TEXT,
            estimated_delivery TEXT,
            order_date TEXT
        )
    ''')

    # 读取JSON数据
    with open(json_path, 'r', encoding='utf-8') as file:
        orders_data = json.load(file)

    # 插入数据到数据库
    for order in orders_data:
        cursor.execute('''
            INSERT OR REPLACE INTO orders (
                order_id, user_id, product_name, quantity, total_price,
                order_status, tracking_number, estimated_delivery, order_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order['order_id'],
            order['user_id'],
            order['product_name'],
            order['quantity'],
            order['total_price'],
            order['order_status'],
            order['tracking_number'],
            order['estimated_delivery'],
            order['order_date']
        ))

    # 提交事务并关闭连接
    conn.commit()
    conn.close()

    print("数据导入完成！")


if __name__ == "__main__":
    setup_database()
