from django.shortcuts import render
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question
import random



def home(request):
    return render(request, 'home/home.html')



def instr(request):
    
    Question.objects.all().delete()
    if request.path == '/home/instr/genknow':
        response = requests.get('https://opentdb.com/api.php?amount=5&category=9&type=multiple')
        data = response.json()
        result_list = data['results']
        for items in result_list:
            qs = Question()
            list_ans = []
            qs.category = items['category']
            qs.type_qs = items['type']
            qs.difficulty = items['difficulty']
            qs.ques = items['question']
            qs.corr_ans = items['correct_answer']
            items['incorrect_answers'].append(items['correct_answer'])
            random.shuffle(items['incorrect_answers'])

            for item in items['incorrect_answers']:
                list_ans.append(item.replace(',', ''))
            qs.ans = list_ans
            
            qs.save()    
        


def genknow(request):


    page = request.GET.get('page')
    paginator = Paginator(qs, 1)
    try:
        page_count = paginator.page(page)
        counter += 1
    except PageNotAnInteger:
        page_count = paginator.page(1)
    except EmptyPage:
        page_count = paginator.page(paginator.num_pages)
    
    print('page_count', page_count)
    print('type(page_count)', type(page_count))

    return render(request, 'home/genknow.html', {'datas':page_count})
