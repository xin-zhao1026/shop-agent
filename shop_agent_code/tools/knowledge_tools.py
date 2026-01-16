from models.rag import RAGSystem
from langchain.tools import tool
rag = RAGSystem()


@tool(description='查询知识库，当用户问退货政策与优惠规则时，可以调用此工具')
def query_knowledge(question: str) -> str:
    """
    查询知识库，回答用户问题
    当用户问退货政策与优惠规则时，可以调用此工具
    :param question: 用户问题
    :return: 回答
    """
    if not question:
        return "请提供一个问题。"

    # 使用RAG系统回答问题
    answer = rag.qa_chain({"query": question})
    rs = answer.get("result", "")
    return rs if rs else "这个问题暂时我还不会。您可以联系人工客服"
