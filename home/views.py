from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from .models import Question
import random
from .forms import QuestionForm



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
            print('list_ans', list_ans)
            print('qs.ans', qs.ans)
            
            qs.save() 

            category = items['category']
        ques_list = Question.objects.all()
        print('ques_list in instr', ques_list)

    return render(request, 'home/instr.html', {'category': category})
   
        


def genknow(request):

    ques_list = Question.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(ques_list, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'home/genknow.html', {'users':users})


def check(request):


    if request.method == "POST":
        u_answer = request.POST.get('userans')
        print('u_answer', u_answer)

        try:
            user_question = Question.objects.get(corr_ans=u_answer)
            
        except Question.DoesNotExist:
            user_question = None
            user_correct_answer = Question.objects.filter(ans__contains=[u_answer]).values('corr_ans')
        
        if user_question == None:
            flag_status = 'fail'
        else:
            flag_status = 'pass'

        
    return render(request, 'home/check.html', {
        'flag_status': flag_status,
        'user_correct_answer':user_correct_answer
        })
