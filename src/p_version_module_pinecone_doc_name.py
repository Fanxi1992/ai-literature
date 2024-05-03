'''计算每一个人数据库已存向量所属的文件名列表，用于展示选择框'''
from pinecone import Pinecone
import os
import numpy as np
import time
import dotenv
dotenv.load_dotenv()

# os.environ["http_proxy"] = "127.0.0.1:9788"
# os.environ["https_proxy"] = "127.0.0.1:9788"


def batch_deletes_by_metadata(index_name, filter_metadata, namespace=None, dimensions=3072, batch=100):
      # Next, we'll create a random vector to use as a query.
     pc = Pinecone()
     index = pc.Index(index_name)
     query_vector = np.random.uniform(-1, 1, size=dimensions).tolist()
     # Now, cycle through the index, and add a slight sleep time in between batches to make sure we don't overwhelm the index.
     deletes = []
     deleted = 0
     results = index.query(vector=query_vector, filter={"source": {"$in":filter_metadata}}, namespace=namespace, top_k=batch)
     while len(results['matches']) > 0:
         ids = [i['id'] for i in results['matches']]
         index.delete(ids=ids,namespace=namespace)
         deleted += len(ids)
         time.sleep(0.01)
         results = index.query(vector=query_vector, filter={"source": {"$in":filter_metadata}}, namespace=namespace, top_k=batch)
     # return deleted


def get_doc_names(index_name):
    pc = Pinecone()
    index1 = pc.Index(index_name)

    # 定义一个集合来存储独立的doc_name
    unique_doc_names = set()

    # 获取索引统计信息
    index_stats = index1.describe_index_stats()
    print(index_stats)
    # 获取向量总数
    try:
        total_vectors = index_stats['namespaces']['']['vector_count']
    except KeyError:
        return unique_doc_names


    # 查询所有向量
    query_response = index1.query(
        top_k=total_vectors,
        include_metadata=True,
        vector=list(range(index1.describe_index_stats()['dimension'])),
    )

    print(len(query_response['matches']))
    # 遍历查询结果并提取metadata中的doc_name
    for result in query_response['matches']:
        doc_name = result['metadata'].get('source', None)
        if doc_name:
            unique_doc_names.add(doc_name)

    # 输出所有独立的doc_name
    return unique_doc_names




