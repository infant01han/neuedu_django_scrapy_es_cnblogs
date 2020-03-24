from django.shortcuts import render
from elasticsearch import Elasticsearch
# Create your views here.
client = Elasticsearch(hosts='127.0.0.1')

def home(request):
    return render(request,'index.html')

def dosearch(request):
    keyword = request.GET.get('q','')

    body = {
        'query':{
            'multi_match':{
                'query':keyword,
                'fields':['title','description']
            }
        },
        'highlight':{
            'pre_tags':['<span class="keyWord">'],
            'post_tags':['</span>'],
            'fields':{
                'title':{},
                'description':{}
            }
        }
    }
    response = client.search(index='cnblogs_new',doc_type='doc',body=body)
    print(response)
    hit_list=[]
    for hit in response['hits']['hits']:
        hit_dic = {}
        if 'title' in hit['highlight']:
            hit_dic['title']=''.join(hit['highlight']['title'])
        else:
            hit_dic['tltle']=hit['_source']['title']

        hit_dic['url'] = hit['_source']['url']

        if 'description' in hit['highlight']:
            hit_dic['description']=''.join(hit['highlight']['description'])
        else:
            hit_dic['description']=hit['_source']['description']
        hit_list.append(hit_dic)
    return render(request,'results.html',{'all_hits':hit_list})