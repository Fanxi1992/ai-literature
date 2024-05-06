import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
import re
import dotenv
import cohere
import os
from pinecone import Pinecone
import os
from langchain_openai import OpenAIEmbeddings

from streamlit_extras.colored_header import colored_header
from streamlit_extras.customize_running import center_running
from streamlit_extras.mention import mention
import streamlit as st
from streamlit_extras.stateful_chat import chat
from streamlit_extras.stodo import to_do
import random
from streamlit_extras.switch_page_button import switch_page


import re
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import pandas as pd

import dotenv
dotenv.load_dotenv()

# os.environ["http_proxy"] = "127.0.0.1:9788"
# os.environ["https_proxy"] = "127.0.0.1:9788"

# app config
st.set_page_config(page_title="文献投稿系统", page_icon="🤖", layout="wide")

pc = Pinecone()


embed_model = "text-embedding-3-large"
embeddings = OpenAIEmbeddings(model=embed_model)


def is_valid_string(s):
    if s is not None and s.strip():
        # 删除所有空格和无意义的字符，例如制表符
        cleaned_string = re.sub(r'[ \t]+', '', s)
        # 检查清洗后的字符串长度是否至少为8
        if len(cleaned_string) >= 5:
            return s
        else:
            return ''
    return ''




df = pd.read_csv('complete_test.csv',encoding='GBK')
print(df)
df = df.rename(columns={'Cites': '引用数'})
df = df.rename(columns={'Authors': '作者'})
df = df.rename(columns={'Title': '标题'})
df = df.rename(columns={'Year': '年份'})
df = df.rename(columns={'Source': '期刊'})
df = df.rename(columns={'ArticleURL': '文章链接'})
df = df.rename(columns={'CitesURL': '引用链接'})
df = df.rename(columns={'Abstract': '缩略摘要'})
# 嵌入并存入向量数据库生成检索器
# db = Chroma.from_documents(chunks, OpenAIEmbeddings(disallowed_special=()), persist_directory=CHROMA_PATH,
#                            collection_name='paper_scan')

def filter_by_score(d,threshold):
    return d["score"] > threshold


def process_input(query: str, top_k: int, parameter_value=0.65):
    index = pc.Index('tougaoabs')
    # # raw_paths = [r"{path}".format(path=p) for p in filter_metadata]
    # # print(raw_paths)
    # # 对list2中的字符串进行转换
    # unescaped_list2 = [unescape_string(s) for s in filter_metadata]

    # 对查询进行编码
    xq = embeddings.embed_query(query)
    # 在 Pinecone 索引中搜索
    q = index.query(vector=xq, top_k=top_k,
                    include_metadata=True
                    )
    # print('q:',len(q['matches']))
    # print('q score:', q['matches'][0]['score'])
    # 使用 lambda 函数来传递额外的 threshold 参数
    docs = list(filter(lambda d: filter_by_score(d, parameter_value), q['matches']))

    print('遴选得到最后的文档数',len(docs))
    # print(docs)
    num_docs = len(docs)
    # print(list(docs[1].metadata.values())[0])

    row_index = []

    for i in range(len(docs)):
        row_index.append(list(docs[i].metadata.values())[0])
    print(row_index)
    result = df.loc[row_index]
    # print(result)
    # print(result.iloc[3])
    second_para = ''
    for i in range(len(row_index)):
        test = result.iloc[i].to_json()
        print(test)
        json_str_trimmed = test[1:-1]
        # 将逗号替换为逗号加换行符
        json_str_with_newlines = json_str_trimmed.replace(",", ",\n")
        # print(json_str_with_newlines)
        print(json_str_with_newlines)
        # 找到 "作者" 字段的起始和结束位置
        start = json_str_with_newlines.find("\\u4f5c")
        end = json_str_with_newlines.find("\\u6807", start)
        print(start,end)

        # 检查 "作者" 字段中是否包含换行符，并进行相应的处理
        if start != -1 and end != -1 and '\n' in json_str_with_newlines[start:end]:
            # 保留最后一个换行符，其他的换行符替换为逗号
            authors_part = json_str_with_newlines[start:end].rsplit('\n', 1)
            authors_part[0] = authors_part[0].replace('\n', ', ')
            json_str_with_newlines = str(i+1) + '.' + ' ' + json_str_with_newlines[:start] + ''.join(authors_part) + '\n' + json_str_with_newlines[end:] + '\n\n'   # str(i+1) + '、' +
    # print(json_str_with_newlines)
            chinese_str = json_str_with_newlines.encode().decode('unicode_escape')
            second_para += chinese_str

    print('论文内容：', second_para)
    result_json = result.to_json()
    # print(result_json)
    # 第2步：在result中处理 "Source" 字段
    source_counts_result = result['期刊'].value_counts()
    # 第3步：在原始DataFrame中统计每个 "Source" 元素的行数
    source_counts_original = df['期刊'].value_counts()

    # 第4步：计算比例
    ratios = source_counts_result / source_counts_original

    # 对比例进行排序并移除0或NaN值
    ratios_sorted = ratios.sort_values(ascending=False).dropna()
    ratios_sorted = ratios_sorted[ratios_sorted > 0]

    # # 第5步：打印结果
    # print("按相关比例排序的期刊次序为：")
    # print(ratios_sorted)
    # print("按绝对值排序的期刊次序为：")
    # print(source_counts_result)

    print(ratios_sorted.to_json())
    # 然后替换逗号（,）为逗号加换行符（,\n）
    json_str = ratios_sorted.to_json()
    # 去掉首尾的 {} 符号
    json_str_trimmed = json_str[1:-1]
    # 将逗号替换为逗号加换行符
    json_str_with_newlines = json_str_trimmed.replace(",", ",\n")
    # 将双引号替换为书名号
    rate_journal_sort = re.sub(r'"([^"]+)"', r'《\1》', json_str_with_newlines)
    cleaned_str1 = rate_journal_sort.replace('\\u2026', '')
    print(cleaned_str1)

    # 然后替换逗号（,）为逗号加换行符（,\n）
    json_str2 = source_counts_result.to_json()
    # 去掉首尾的 {} 符号
    json_str_trimmed2 = json_str2[1:-1]
    # 将逗号替换为逗号加换行符
    json_str_with_newlines2 = json_str_trimmed2.replace(",", ",\n")
    # 将双引号替换为书名号
    jueduizhi_sort_journal = re.sub(r'"([^"]+)"', r'《\1》', json_str_with_newlines2)
    cleaned_str = jueduizhi_sort_journal.replace('\\u2026', '')
    print(cleaned_str)

    first_para = f'根据您的论文内容与设定的相关性阈值({parameter_value})，已在ABS期刊范围内为您找到{num_docs}篇相关论文如下：\n'
    third_para = f'\n下面是相关论文在各期刊中的分布计算，首先从数量分布上来看，结果如下：\n\n'
    fourth_para = cleaned_str
    fifth_para = f'\n\n然后从比例分布上来看，结果如下：\n\n'
    sixth_para = cleaned_str1

    return [first_para,second_para,third_para,fourth_para,fifth_para,sixth_para]




print('程序启动完成')




coltougao_1, coltougao_2 = st.columns([2.5, 1])

with coltougao_2:

    colored_header(
        label="参数配置",
        description="",
        color_name="blue-70",
    )


    # 大模型的温度选择，返回重排序之后的chunks
    similarity_value = st.slider("相似度阈值设置（过滤低于该值的论文）", min_value=0.2, max_value=0.7, value=0.4, step=0.05,
                           key="slider2_tougao")


    chunks_limit = st.slider("最多返回的论文数（按相似度降序）", min_value=5, max_value=50, value=20, step=1,
                           key="slider3_tougao")

with coltougao_1:
    colored_header(
        label="论文投稿推荐系统（暂只包括ABS期刊中数十种与流动性研究有关的期刊）",
        description="",
        color_name="violet-70",
    )
    # session state
    if "tougao_history" not in st.session_state:
        st.session_state.tougao_history = [
            AIMessage(content="你好，我是您的投稿推荐助手，请将您需要投稿论文的标题或者摘要等内容直接告诉我，我将为你推荐相关论文和期刊~"),
        ]

    # 设置一个按钮，用于清空除了第一条消息之外的所有消息
    if st.button(label="清空对话记录",type="primary"):
        st.session_state.tougao_history = st.session_state.tougao_history[:1]



    # conversation
    for message in st.session_state.tougao_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    # 创建用户输入的占位符
    # # 创建一个容器来持续更新内容
    # content = st.container()
    #
    # # 在脚本的末尾创建一个输入框占位符
    # input_placeholder = st.empty()
    # user input
user_query = st.chat_input("Type your message here...")

with coltougao_1:
    if user_query is not None and user_query != "":
        st.session_state.tougao_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            response = process_input(query=user_query, parameter_value=similarity_value, top_k=chunks_limit)
            response_str = "\n".join(response)  # 将列表连接成一个单独的字符串
            print(response_str)
            st.text(response_str)

        st.session_state.tougao_history.append(AIMessage(content=response_str))







