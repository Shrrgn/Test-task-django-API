#utils.py

def checking_password(data):
		return any(i.isupper() for i in data) and any(i.isdigit() for i in data) and \
					any(i in '@.+-_' for i in data) and (len(data) >= 8 or len(data) <= 30)
