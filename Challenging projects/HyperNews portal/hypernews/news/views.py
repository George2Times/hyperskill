from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View

from django.conf import settings

import itertools
import json
from datetime import datetime
import random


def read_news_from_json() -> []:
    with open(settings.NEWS_JSON_PATH, 'r') as f:
        return json.load(f)


def append_news_to_json(data: [{}, ]):
    with open(settings.NEWS_JSON_PATH, 'w') as f:
        f.write(json.dumps(data, indent=4))


def coming_soon(request):
    # return HttpResponse('Coming soon!')
    return redirect('/news/')


news_data = read_news_from_json()


class Index(View):
    def get(self, request):
        q = request.GET.get('q')
        if q is None:
            sorted_news = sorted(news_data, key=lambda i: i['created'], reverse=True)
        else:
            found_news = []
            for news in news_data:
                if q in news['title']:
                    found_news.append(news)
            sorted_news = sorted(found_news, key=lambda i: i['created'], reverse=True)
        grouped_news = {}
        for key, value in itertools.groupby(sorted_news, lambda i: i['created'][:10]):
            grouped_news[key] = list(value)
        return render(request, 'home.html', context={'grouped_news': grouped_news})


class NewsView(View):
    def get(self, request, link, *args, **kwargs):
        for news in news_data:
            if link == news['link']:
                return render(request, 'news.html', context=news)
        return redirect('/news/')


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create.html')

    def post(self, request, *args, **kwargs):
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        link = random.randint(1, 10000)
        while link in [i['link'] for i in news_data]:
            link = random.randint(1, 10000)
        title = request.POST.get('title')
        text = request.POST.get('text')
        news_data.append({'created': created,
                          'link': link,
                          'title': title,
                          'text': text})
        append_news_to_json(news_data)
        return redirect('/news/')
