from aip import AipNlp

# 百度AI服务的API凭证
APP_ID = '103835469'
API_KEY = 'okFsYNtZ7aKicru6mWpJMW3T'
SECRET_KEY = 'OZxunjYvXg2eTymrnqDrSJNog1TYn004'

# 初始化AipNlp对象
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# 定义意图和对应的输出值
"""
展示的内容：
1. 图书馆相关信息
2. 智能搜索
3. 根据自习室号来预定座位
4. 借特定书籍
"""
intents = {
    # 跳转功能/查询功能
    '看图书库的所有图书': 1, # 打开图书库列表，展示图书馆的所有图书
    '我要看自习室': 2, # 打开座位预约单据
    '打开读书笔记': 3, # 打开读书笔记动态表单
    '打开我的书架看,看我借阅过哪些图书': 4, # 打开我的书架列表
    '查看我的信誉分数': 5, # 查看我的信誉分数表单
    '我想查看图书论坛': 6,  # 打开图书论坛
    '我要用智慧阅读功能': 7, # 打开智慧阅读功能
    # GPT 适配功能
    '了解图书馆的概况': 0, # 呼出图书馆咨询助手，并向读者介绍图书馆的基本情况
    '我要用GPT功能来推荐图书': 8, # 呼出gpt来推荐图书
    '帮我预定座位，需要某号自习室的座位': 9, # 呼出gpt来订座位
    # 交付给kimi的功能
    '我要借一本XXX的图书': -1, # 借一本特定的书
    '我想看一本讲述XXX的书籍': -1, # 智能搜索
}

def process_string(input_string):
    """
    处理输入字符串并返回对应的值。

    :param input_string: 需要处理的字符串
    :return: 对应意图的值，如果没有匹配的意图则返回 -1
    """
    max_score = 0
    best_match = -1
    
    # 使用百度AI的短文本相似度API来分析输入字符串的意图
    for intent, value in intents.items():
        similarity_result = client.simnet(input_string, intent)
        
        # 检查相似度结果是否包含'score'字段
        if 'score' in similarity_result:
            score = similarity_result['score']
            if score > max_score:
                max_score = score
                best_match = value
        else:
            print(f"Error in API response: {similarity_result}")
    
    # 设置相似度阈值
    threshold = 0.5
    if max_score >= threshold:
        return best_match
    else:
        return -1

# 使用
# input_string = "我想借呐喊"
# output = process_string(input_string)
# print(f"输入: '{input_string}' 的输出结果: {output}")