from datetime import datetime

from django.shortcuts import render
from elasticsearch import Elasticsearch
# Create your views here.
client = Elasticsearch(hosts='127.0.0.1')

def home(request):
    return render(request,'index.html')

def dosearch(request):
    keyword = request.GET.get('q','')
    pageIndex = request.GET.get('page','1')
    try:
        pageIndex = int(pageIndex)
    except:
        pageIndex = 1

    body = {
        'query':{
            'multi_match':{
                'query':keyword,
                'fields':['title','description']
            }
        },
        'from':(pageIndex-1)*10,
        'size':10,
        'highlight':{
            'pre_tags':['<span class="keyWord">'],
            'post_tags':['</span>'],
            'fields':{
                'title':{},
                'description':{}
            }
        }
    }
    start_time = datetime.now()
    response = client.search(index='cnblogs_new',doc_type='doc',body=body)
    # print(response)
    total_nums = response["hits"]["total"]
    if total_nums%10==0:
        page_nums=int(total_nums/10)
    else:
        page_nums=int(total_nums/10)+1
    hit_list=[]
    for hit in response['hits']['hits']:
        hit_dic = {}
        if 'title' in hit['highlight']:
            hit_dic['title']=''.join(hit['highlight']['title'])
        else:
            hit_dic['tltle']=hit['_source']['title']

        hit_dic['url'] = hit['_source']['url']
        hit_dic['article_date'] = hit['_source']['article_date']
        hit_dic['score'] = hit['_score']
        hit_dic["source_site"] = "博客园"


        if 'description' in hit['highlight']:
            hit_dic['description']=''.join(hit['highlight']['description'])
        else:
            hit_dic['description']=hit['_source']['description']
        hit_list.append(hit_dic)
    end_time = datetime.now()
    last_time = (end_time-start_time).total_seconds()
    return render(request,'results.html',{'all_hits':hit_list,
                                          'pageIndex':pageIndex,
                                          'keyword':keyword,
                                          'page_nums':page_nums,
                                          'total_nums':total_nums,
                                          'last_time':last_time})