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

            items['correct_answer'].replace(',','')
            qs.corr_ans = items['correct_answer']

            items['incorrect_answers'].append(items['correct_answer'])
            random.shuffle(items['incorrect_answers'])

            for item in items['incorrect_answers']:
                list_ans.append(item.replace(',', ''))
            qs.ans = list_ans
            
            qs.save() 

            category = items['category']
        ques_list = Question.objects.all()
        print('ques_list in instr', ques_list)

    return render(request, 'home/instr.html', {'category': category})
   
        


def genknow(request):

    ques_list = Question.objects.all().order_by('id')
    print('ques_list in genknow', ques_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(ques_list, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'home/genknow.html', {'users':users})
