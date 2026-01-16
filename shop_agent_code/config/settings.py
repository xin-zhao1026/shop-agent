import os


class Settings:
    # API KEY
    QWEN_KEY = 'sk-258d9eef3c234493b5e1c6e424'
    ZHIPU_KEY = '506b011ee51c4a828124883fa3CerJRyD5md33'

    # 模型配置
    MODEL_NAME = 'glm-4'  # 使用的模型名称
    TEMPERATURE = 0.2  # 模型温度，值在0-1之间。值越小，随机性越低

    # 文件路径配置
    ORDER_FILE = os.path.join(os.path.dirname(
        __file__), '../data/orders.json')  # 订单数据文件路径
    DB_PATH = os.path.join(os.path.dirname(
        __file__), '../data/orders.db')  # 订单数据库路径
    # RAG文档
    DOC_FILE = os.path.join(os.path.dirname(
        __file__), '../docs/policy_docs.md')  # 知识库文档路径

    # RAG配置
    EMBEDDING_MODEL = 'bge-small-zh-v1.5'  # 嵌入模型名称

    # Chroma数据库路径
    CHROMA_DB_PATH = 'chroma_db5'

    # 拆分文档的块大小
    CHUNK_SIZE = 50  # 适合中文段落，段落大小
    CHUNK_OVERLAP = 10  # 避免上下缺失


setting = Settings()
