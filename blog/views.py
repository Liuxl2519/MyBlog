from django.shortcuts import render

from django.http import HttpResponse

from blog.models import Article
from django.core.paginator import Paginator

# Create your views here.

def hello_world(request):
    return HttpResponse("hello_world")


def article_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_abstrace = article.brief_abstract
    content = article.content
    article_id = article.article_id
    publish_date = article.publish_date
    return_str = 'title:%s, brief_abstrace:%s,' \
                 'content:%s,article_id:%s,publish_date:%s,' % (
                 title, brief_abstrace, content, article_id, publish_date)
    return HttpResponse(return_str)


def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param:', page)
    all_article = Article.objects.all()
    # 按照发布时间倒序（事件最新）排列文章，取前五篇
    top5_article_list=Article.objects.order_by('-publish_date')[:5]
    # 实例化Django分页组件
    paginator=Paginator(all_article,1)
    # 一共多少页
    page_num=paginator.num_pages
    # 第几页
    page_article_list=paginator.page(page)
    if page_article_list.has_next():
        next_page=page+1
    else:
        next_page=page
    if page_article_list.has_previous():
        previous_page=page-1
    else:
        previous_page=page

    return render(request, 'blog/index.html',
                  {
                      'article_list': page_article_list,
                      'page_num':range(1,page_num+1),
                      'currt_page':page,
                      'previous_page':previous_page,
                      'next_page':next_page,
                      'top5_article_list':top5_article_list
                  }
                  )


def get_detail_page(request, article_id):
    all_article = Article.objects.all()

    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None
    currt_content = None
    for index, article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index == index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        if article.article_id == article_id:
            currt_content = article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break

    section_list = currt_content.content.split('\n')
    return render(request, 'blog/detail.html',
                  {
                      'currt_content': currt_content,
                      'section_list': section_list,
                      'previous_article': previous_article,
                      'next_article': next_article
                  }
                  )
