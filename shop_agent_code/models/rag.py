import os

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA

from models.llm import LLMInitializer
from config import setting


class RAGSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.qa_chain = None
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        if self.qa_chain is not None:
            return self.qa_chain
        # 加载数据
        DOC_PATH = os.path.join(os.path.dirname(os.path.dirname(
            __file__)), './docs/policy_docs.md')
        print(DOC_PATH)
        # 收集数据
        loader = TextLoader(DOC_PATH, encoding='utf-8')
        documents = loader.load()
        # 分隔数据
        # 中文分块
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=setting.CHUNK_SIZE,  # 适合中文段落，段落大小
            chunk_overlap=setting.CHUNK_OVERLAP,  # 避免上下缺失
            separators=["\n\n", "\n", "。", "!", "?"]  # 段落分隔符
        )
        splits = text_splitter.split_documents(documents)
        # 向量化

        # 加载本地模型
        embeddings = HuggingFaceEmbeddings(
            model_name=setting.EMBEDDING_MODEL,  # 嵌入模型
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}  # 提升相似度计算精度
        )
        # 存放数据库

        db = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=setting.CHROMA_DB_PATH  # 数据库路径
        )
        # 创建提示词模板
        rag_prompt_template = '''
        你是一个专业的电商客服助手，根据以下商品政策信息，用自然友好的对话风格回答用户问题，就像在聊天一样。

        已知信息:
        {context} # 检索出来的原始文档

        用户问题:
        {question} # 用户的问题

        如果已知信息中不包含用户问题的答案，或者已知信息无法回答用户问题，请直接返回"这个问题暂时我还不会。您可以联系人工客服"。
        请不要输出已知信息中不包含的信息或者答案。
        请用中文回答用户问题。
        '''
        rag_prompt = PromptTemplate(
            template=rag_prompt_template,
            input_variables=["context", "question"]
        )

        llm = LLMInitializer().get_llm()
        # 创建qa链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=db.as_retriever(search_kwargs={"k": 1}),
            chain_type_kwargs={"prompt": rag_prompt},
            return_source_documents=False   # 返回源文档
        )
        return self.qa_chain

    def get_chain(self):
        return self.qa_chain
