from elasticsearch import Elasticsearch
es = Elasticsearch(['es'])
es.indices.refresh(index="user_index")
print(es.search(index='user_index', body={'query': {'query_string': {'query': 'qwer'}}, 'size': 10}))