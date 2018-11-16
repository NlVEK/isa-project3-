from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import time
import json
es = Elasticsearch(['es'])
time.sleep(10)
while True:
    consumer = KafkaConsumer('new_user', group_id='user-indexer', bootstrap_servers=['kafka:9092'])
    for message in consumer:
        msg = json.loads((message.value).decode('utf-8'))
        es.index(index='user_index', doc_type='user', id=msg['id'], body=msg)
        es.indices.refresh(index="user_index")