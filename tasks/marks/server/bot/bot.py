from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import redis
import json
import time


HOST = 'marks'
PORT = 8000

REDIS_HOST = 'redis'
REDIS_PORT = 6379

redis_instance = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

TEACHER_KEY = '5765e7913925628c3a42fa4f219f6b5a'
		
def bot_init():
	try:
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		
		driver = webdriver.Chrome('/bot/chromedriver', options=chrome_options)
		
		print('[+] webdriver created')
		return driver
	except:
		print('[-] webdriver creation failed')
		return False
	

def activate_teacher():
	r = requests.get('http://{}:{}/api/activate_teacher?t_key={}'.format(HOST, PORT, TEACHER_KEY))

	if json.loads(r.text)['status'] == 'success':
		print('[+] teacher\'s account created')
	else:
		print('[-] teacher\'s account creation failed')
		return False, False

	login = json.loads(r.text)['credentials']['login']
	password = json.loads(r.text)['credentials']['password']

	return login, password


def log_in(driver, t_login, t_password):
	try:
		driver.get('http://{}:{}/login'.format(HOST, PORT))

		username = driver.find_element_by_name('username')
		username.send_keys(t_login)

		password = driver.find_element_by_name('password')
		password.send_keys(t_password)

		username.send_keys(Keys.RETURN)

		assert 'Marks' in driver.title

		print('[+] teacher logged in successfully')

		return driver
	except:
		print('[-] teacher\'s logging in failed')

		return False


def check_questions(questions, driver):
	try:
		for q in questions:
			link = redis_instance.get(q).decode()
			driver.get('http://{}:{}/{}'.format(HOST, PORT, link))
			
			redis_instance.delete(q)

			print('[+] question n{} has been checked'.format(q.decode()))
	except:
		print('[-] checking questions failed')


def main():
	driver = bot_init()

	t_login, t_password = activate_teacher()

	if not t_login or not t_password or not driver:
		print('[-] exiting')
		return 0

	if not log_in(driver, t_login, t_password):
		print('[-] exiting')
		return 0

	print('[+] starting checking questions')

	while True:
		questions = redis_instance.keys()
		if not questions:
			print('[-] have no questions to check')
			time.sleep(10)
		else:
			print('[+] got new questions')
			check_questions(questions, driver)


if __name__ == '__main__':
	main()
