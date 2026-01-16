from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor, create_tool_calling_agent

from models.llm import LLMInitializer
from tools.order_tools import get_order_status, return_order, complain_order
from tools.knowledge_tools import query_knowledge
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory


class ServiceAgent:
    def __init__(self):
        # 初始化LLM
        self.llm = LLMInitializer().get_llm()
        # 初始化工具类
        self.tools = [
            get_order_status,
            return_order,
            complain_order,
            query_knowledge
        ]
        # 创建记忆系统
        self.memory = ConversationBufferWindowMemory(
            k=5, return_messages=True, memory_key="chat_history")
        # 初始化代理对象
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self):
        '''
        返回代理对象
        '''
        # 获取提示词
        # prompt = hub.pull("hwchase17/react")
        template = '''
        Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}
        '''
        # prompt = PromptTemplate.from_template(template)
        # 创建智能体
        # agent = create_react_agent(
        #     llm=self.llm, tools=self.tools, prompt=prompt)

        agent_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional e-commerce customer service assistant who can check order status, apply for returns, submit complaints, and access the knowledge base.

        IMPORTANT INSTRUCTIONS:
        1. Use tools when you need specific information (order status, knowledge queries, etc.)
        2. When using the knowledge tool, extract keywords from the user's input as the input content
        3. Once you have the information needed to answer the user's question, provide your final answer directly
        4. Do NOT call the same tool multiple times unless you need different information
        5. Always provide your final answer in Chinese language

        WHEN TO STOP:
        - After getting tool results that answer the user's question, provide your final answer immediately
        - Do not call tools again if you already have the information needed"""),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])

        agent = create_tool_calling_agent(
            llm=self.llm, tools=self.tools, prompt=agent_prompt)
        # 创建AgentExecutor,运行智能体
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,  # verbose代表输出日志
            handle_parsing_errors=True    # 默认False,帮处理异常错误,让程序更健壮
        )
        return agent_executor

    def chat(self, user_input: str):
        resp = self.agent_executor.invoke({'input': user_input})
        return resp['output']


customer_service_agent = ServiceAgent()
