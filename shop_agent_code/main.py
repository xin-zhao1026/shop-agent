from agent.service_agent import customer_service_agent
from tools.knowledge_tools import query_knowledge


def main():
    print('==============电商智能客服系统启动成功 =====================')
    print('您可以询问:')
    print('- 订单状态: 我的订单OD1001状态如何?')
    print('- 退货: 订单OD1001退货')
    print('- 投诉: 订单OD1001投诉商品质量')
    print('- 查询知识库: 请问退货政策是什么？')
    print('- 输入:exit 退出系统')

    while True:
        user_input = input('请输入您的问题: ')
        if user_input.lower() == 'exit':
            print('系统已退出！')
            break
        if user_input:
            rs = customer_service_agent.chat(user_input)
            print(f'客服:{rs}')


'''
1. 修改提示词
2. 修改工具的描述
3. 更换LLM
'''
if __name__ == '__main__':
    main()

    # 测试查询知识库
    # test_question = "请问退货政策是什么？"
    # response = query_knowledge(test_question)
    # print(f"回答: {response}")
