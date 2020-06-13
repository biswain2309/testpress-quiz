from django.shortcuts import render
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'home/home.html')


def genknow(request):
    response = requests.get('https://opentdb.com/api.php?amount=5&category=9&difficulty=medium&type=multiple')
    data = response.json()

# Extracting only the results part of the API and converting the data to a list
    list_qs = []
    questions = data['results']
    for items in questions:
        list_qs.append(list(items.values()))

    page = request.GET.get('page')
    paginator = Paginator(list_qs, 1)
    try:
        page_count = paginator.page(page)
    except PageNotAnInteger:
        page_count = paginator.page(1)
    except EmptyPage:
        page_count = paginator.page(paginator.num_pages)

    return render(request, 'home/genknow.html', {'datas':page_count})
