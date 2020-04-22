from django import forms

class RegisterForm(forms.Form):
    login = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Имя пользователя'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'form-control form-control mx-sm-3','placeholder':'Пароль', 'style':'margin-bottom:0px;'}))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'form-control form-control mx-sm-3','Placeholder':'Ваш пароль еще раз'}))


class QuestionForm(forms.Form):
	title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class':'form-control rounded-0'}))
	text = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class':'form-control rounded-0', 'rows':'5'}))
