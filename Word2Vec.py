from gensim.models import KeyedVectors
import jieba
import numpy as np

# 加载预训练的Word2Vec模型
model = KeyedVectors.load_word2vec_format('sgns.baidubaike.bigram-char', binary=False)

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

def get_sentence_vector(sentence):
    """将句子转换为向量"""
    words = jieba.lcut(sentence)
    vectors = [model[word] for word in words if word in model]
    if not vectors:
        return np.zeros(model.vector_size)
    return np.mean(vectors, axis=0)

def calculate_similarity(vec1, vec2):
    """计算两个向量的余弦相似度"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def process_string(input_string):
    max_score = 0
    best_match = -1

    input_vector = get_sentence_vector(input_string)
    for intent, value in intents.items():
        intent_vector = get_sentence_vector(intent)
        score = calculate_similarity(input_vector, intent_vector)
        if score > max_score:
            max_score = score
            best_match = value

    # 设置相似度阈值
    threshold = 0.5
    if max_score >= threshold:
        return best_match
    else:
        return -1

# 使用示例
while True:
    input_string = input("请输入一个句子: ")
    if input_string == "exit":
        break
    output = process_string(input_string)
    print(f"输入: '{input_string}' 的输出结果: {output}")