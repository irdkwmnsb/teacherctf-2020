from flask import Flask, Response, request, render_template, redirect, session
app = Flask(__name__)
app.secret_key = '123454321'

def check_user(username, password):
	db = open('db_users','r').read().split('\n')
	users = {u.split(':')[0]:u.split(':')[1] for u in db}

	if username in users.keys():
		if password == users[username]:
			return True

	return False


@app.route('/', methods=['POST', 'GET'])
def index():
	error = ''
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		if check_user(username, password):
			recipe = open('recipe.txt').read()

			return Response(recipe, mimetype='text/plain', content_type='text/plain; charset=UTF-8')
		else:
			error = 'incorrect'

	return render_template('login.html', error=error), {'Script-File': 'sourcefile.py'}


@app.route('/static')
def style():
	f = request.args.get('file')

	if 'recipe' in f:
		return 'not so easy'

	if 'jpeg' in f:
		file = open('static/'+f, 'r').read()
		return Response(file, mimetype='image/jpeg')

	file = open('static/'+f, 'r').read()

	return Response(file, mimetype='text/css')
