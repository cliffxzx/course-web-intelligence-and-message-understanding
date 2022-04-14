import elasticsearch

elk = elasticsearch.Elasticsearch(hosts='http://localhost:9200', http_auth=('elastic', '123456'))