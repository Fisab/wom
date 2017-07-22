import time

def get_time():
	return int(time.time())

def to_unix_time(date):
	return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

def to_normal_time(date):
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(date)))

def sleep(sec):
	time.sleep(sec)