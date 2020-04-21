from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse,redirect
from django.db.models import Sum
from django.contrib.auth.models import User
from .form import RegisterForm, QuestionForm
from .models import Mark, Question
from marks import settings
import random
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

FLAG = 'TeacherCTF{y0u_4r3_h0n0ur5_pup1l_4nd_x55_m4573r}'
SUBJECTS = ['Математика', 'Литература', 'Биология', 'Физкультура', 'Minecraft', 'ctf']

@login_required(login_url='/login')
def index_page(request):
	user = request.user

	ctf_ar_mean = sum(Mark.objects.filter(user=user, subject='ctf').values_list('value', flat=True)) / Mark.objects.filter(user=user, subject='ctf').count()

	context = {
		'user': user,
		'text': 'Повысьте свой средний балл по ctf\'у для того, чтобы получить флаг' if not user.profile.is_teacher else 'Для выставления оценок ученикам перейдите во вкладку "Поставить оценку"',
		'flag': FLAG if ctf_ar_mean >= 4 and not user.profile.is_teacher else ''
	}

	return render(request, 'index.html', context)

def register(request):
	error_context = {}

	if request.user.is_authenticated:
		return redirect('index_page')

	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
				username = form.cleaned_data.get('login')
				password = form.cleaned_data.get('password')
				password1 = form.cleaned_data.get('password1')

				if User.objects.filter(username=username).exists():
					error_context['username_error'] = 'Пользователь с таким именем уже существует.'

				if password != password1:
					error_context['password_missmatch'] = 'Пароли не совпадают.'

				if error_context == {}:
					user = User.objects.create_user(username, password=password)
					user.save()

					marks = Mark.objects.bulk_create(
						3*[Mark(user=user, subject=sub, value=random.randint(4,5)) for sub in SUBJECTS[:-1]]
					)

					two = Mark(user=user, subject='ctf', value=3)
					two.save()

					login(request, user)
					return redirect('index_page')

	else:
		form = RegisterForm()

	context = {
		'form': form,
		'error_context': error_context
	}

	return render(request,'registration/register_form.html', context)


@login_required(login_url='/login')
def marks(request):
	user = request.user

	if user.profile.is_teacher == True:
		return HttpResponse('вы не похожи на ученика!')

	subjects = [		
		{					#да, костыль, признаю!
			'title': sub, 
			'marks': Mark.objects.filter(user=user, subject=sub).values_list('value', flat=True),  
			'ar_mean': sum(Mark.objects.filter(user=user, subject=sub).values_list('value', flat=True)) / Mark.objects.filter(user=user, subject=sub).count()
		} 
		for sub in SUBJECTS
	]

	context = {
		'subjects': subjects,
		'user': request.user	
	}
	return render(request, 'marks.html', context)


@login_required(login_url='/login')
def question(request):
	user = request.user

	if request.method == 'POST':
		form = QuestionForm(request.POST)

		if form.is_valid():
			title = form.cleaned_data.get('title')
			text = form.cleaned_data.get('text')

			new_question = Question(title=title, text=text, author=user)
			new_question.save()

			redis_instance.set(str(new_question.id), 'check_question/'+str(new_question.id))
	
	else:
		form = QuestionForm()

	questions = Question.objects.filter(author=user) if user.profile.is_teacher == False else Question.objects.all()

	context = {
		'form': form, 
		'questions': questions,
		'user': user
	}

	return render(request, 'question.html', context)


@login_required(login_url='/login')
def inspect_question(request, question_id):
	user = request.user
	
	if not Question.objects.filter(author=user, id=question_id).exists() and not user.profile.is_teacher:
		return redirect('index_page')

	question = Question.objects.get(id=question_id)

	context = {
		'question': question,
		'user': user
	}

	return render(request, 'inspect_question.html', context)


@login_required(login_url='/login')
def diary(request):
	user = request.user

	context = {
		'no_homework': 'Карантин! Никакого домашнего задания.',
		'user': user
	}

	return render(request, 'diary.html', context)