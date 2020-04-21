from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from student.models import Profile, Question, Mark
from django.contrib.auth.decorators import login_required
from .form import NewMarkForm
from marks import settings
import json

TEACHER_KEY = '5765e7913925628c3a42fa4f219f6b5a'
TEACHER_PASSWORD = 'keklolteacherspasswordissosecret213'

SUBJECTS = ['Математика', 'Литература', 'Биология', 'Физкультура', 'Minecraft', 'ctf']


def activate_teacher(request):
	t_key = request.GET.get('t_key')

	if t_key == TEACHER_KEY:
		teacher_login = 'teacher_'+str(User.objects.filter(profile__is_teacher=True).count()+1)
		teacher = User.objects.create_user(teacher_login, 
										password=TEACHER_PASSWORD)

		teacher.profile.is_teacher = True
		teacher.profile.save()
		teacher.save()

		mark = Mark(user=teacher, value=5, subject='ctf')
		mark.save()

		return HttpResponse(
			json.dumps(
				{'status': 'success', 'credentials':{'login':teacher_login, 'password':TEACHER_PASSWORD}}
			)
		)
	
	else:
		return HttpResponse(
			json.dumps(
				{'status': 'error'}
			)
		)

@login_required(login_url='/login')
def check_question(request, question_id):
	user = request.user

	if user.profile.is_teacher == False:
		return HttpResponse('вы не похожи на учителя!')


	question = Question.objects.get(id=question_id)
	question.seen = True
	question.save()

	context = {
		'question': question
	}

	return render(request, 'check_question.html', context)

@login_required(login_url='/login')
def new_mark(request):
	user = request.user
	error_context = {}

	if user.profile.is_teacher == False:
		return HttpResponse('вы не похожи на учителя!')

	if request.method == 'POST':
		form = NewMarkForm(request.POST)

		if form.is_valid():
			subject = form.cleaned_data.get('subject')
			mark = form.cleaned_data.get('mark')
			student = form.cleaned_data.get('student')

			if subject not in SUBJECTS:
				error_context['subject_error'] = 'Такого предмета не существует.'
			try:
				mark = int(mark)
				if mark < 0 or mark > 5:
					error_context['mark_error'] = 'Выберите оценку от 1 до 5.'
			except:
				error_context['mark_error'] = 'Неверный формат оценки.'

			if not User.objects.filter(username=student).exists():
				error_context['student_error'] = 'Неверный login студента.'

			if error_context == {}:
				new_mark = Mark(user=User.objects.get(username=student), value=int(mark), subject=subject)
				new_mark.save()

				return redirect('new_mark')

	else:
		form = NewMarkForm()

	context = {
		'error_context': error_context,
		'user': user,
		'form': form
	}

	return render(request, 'new_mark.html', context)