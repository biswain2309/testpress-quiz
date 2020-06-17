from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from .models import Question
import random
from .forms import QuestionForm

page_number_prev = 0

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
            # print('list_ans', list_ans)
            # print('qs.ans', qs.ans)
            
            qs.save() 

            category = items['category']
        ques_list = Question.objects.all()
        # print('ques_list in instr', ques_list)


    return render(request, 'home/instr.html', {'category': category})
   
        


def genknow(request):

    global page_number_prev

    print('type(page_number_prev)', type(page_number_prev))
    # show_next = False
    print('request.method', request.method)
    ques_list = Question.objects.all().order_by('id')
    # page = Question.objects.values('question_id')
    # print('*********1', page_number)
    # print('*********1', page_number_prev)
    if page_number_prev > 1 and page_number_prev < 6 or request.method=='POST':
        page_number_prev += 1
        page_number = page_number_prev
        print('*********1', page_number)
        print('*********1', page_number_prev)
    else:
        page_number = request.GET.get('page', 1)
        page_number_prev = int(page_number)
        print('*********2', page_number)
        print('*********2', page_number_prev)
    # if request.method == 'GET':
    #     print('*****inside GET', page)
    # elif request.method == 'POST':
    #     page+=1
    
    # print('******', page)
    # print('******', type(page))

    # if page > 1:
    #     page = int(page)

    # if page < 2:
    #     pass
    # else:
    #     page+=1

    # page = 0

    # if request.method == 'GET':
    #     print('*****inside if', page_number)
    #     page_number+=1

    # else:
    #     page = page


    paginator = Paginator(ques_list, 1)
    page_obj = paginator.get_page(page_number)
    # try:
    #     users = paginator.page(page)
    # except PageNotAnInteger:
    #     print('Not an integer', page)
    #     users = paginator.page(1)
    # except EmptyPage:
    #     users = paginator.page(paginator.num_pages)

    print('----------->redirect')

    if request.method == "POST":
        print('*****inside POST', page_number)
        print('page_obj', page_obj)
        u_answer = request.POST.get('userans')
        # print('u_answer', u_answer)
        print('----------->post')
        try:
            user_question = Question.objects.get(corr_ans=u_answer)
            
        except Question.DoesNotExist:
            user_question = None
            user_correct_answer = Question.objects.filter(ans__contains=[u_answer]).values('corr_ans')
        
        if user_question == None:
            flag_status = 'fail'
        else:
            flag_status = 'pass'
            user_correct_answer = u_answer
        
        return render(request, 'home/genknow.html', {
        'page_obj':page_obj,
        'flag_status': flag_status,
        'user_correct_answer':user_correct_answer,
        'show_next': True
        })


    return render(request, 'home/genknow.html', {'page_obj':page_obj, 'show_next': False})


def check(request):

    show_next = True

    if request.method == "POST":


        u_answer = request.POST.get('userans')
        # print('u_answer', u_answer)

        try:
            user_question = Question.objects.get(corr_ans=u_answer)
            
        except Question.DoesNotExist:
            user_question = None
            user_correct_answer = Question.objects.filter(ans__contains=[u_answer]).values('corr_ans')
        
        if user_question == None:
            flag_status = 'fail'
        else:
            flag_status = 'pass'
            user_correct_answer = u_answer
        
    # return redirect(request, 'home/genknow/check.html', {
    #     'flag_status': flag_status,
    #     'user_correct_answer':user_correct_answer,
    #     'show_next': show_next
    #     })
    return redirect('/home/genknow')
