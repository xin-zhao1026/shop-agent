from langchain_community.llms import tongyi
import os
from langchain_community.chat_models import ChatZhipuAI

from config import setting


class LLMInitializer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.llm = None
        return cls._instance

    def get_llm(self):
        if self.llm is None:
            # 初始化通义千问LLM
            # key = 'sk-258d9eef3c234493b5e1c6e4247ff162'
            # self.llm = tongyi.Tongyi(model="qwen-max", api_key=key)

            os.environ["ZHIPUAI_API_KEY"] = setting.ZHIPU_KEY

            self.llm = ChatZhipuAI(
                model=setting.MODEL_NAME,
                temperature=setting.TEMPERATURE     # 模型温度，　值在0-1之间。 值越小，随机性越低
            )
        return self.llm


if __name__ == '__main__':
    llm = LLMInitializer().get_llm()
    llm2 = LLMInitializer().get_llm()

    # 判断llm和llm2是否是同一个对象
    print(llm is llm2)
