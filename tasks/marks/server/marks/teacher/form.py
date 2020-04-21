from django import forms


class NewMarkForm(forms.Form):
	subject = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Название предмета'}))
	mark = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Оценка(от 1 до 5)'}))
	student = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Имя пользователя студента'}))
