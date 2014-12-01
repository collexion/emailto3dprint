import config
import json
conf = config.read_config()
class User(object):
	@staticmethod
	def copy(self, user):
		return User(user.to_row())
		
	def __init__(self, ls):
		self.construct(ls)
		
	def construct(self, ls):
		self.email = ls[0]
		self.jobs_submitted = int(ls[1])
		
	def __eq__(self, other):
		if isinstance(other, User):
			return self.email == other.email
		else:
			return False
			
	def __str__(self):
		return self.to_string()
		
	def to_row(self):
		return [self.email, self.prints_submitted]
		
	def to_string(self):
		return ' '.join(self.to_row())
		
class UserDB(object):
	def __init__(self):
		self.userdb_flname = conf['Users']['filename']
	def read_all_users(self):
		users = []
		with open(self.userdb_flname) as fl:
			for line in fl:
				user = User(line.split())
				users.append(user)
		return users
	def write_all_users(self, users):
		lines = [user.to_string() for user in users]
		text = '\n'.join(lines)
		with open(self.userdb_flname, 'w') as fl:
			fl.write(text)
	def find_user(self, email):
		with open(self.userdb_flname) as fl:
			for line in fl:
				user = User(line.split())
				if user.email == email:
					return user
		return None
	def add_user(self, new_user):
		users = self.read_all_users()
		found = False
		for user in users:
			if user == new_user:
				user.construct(new_user)
				found = True
		if not found:
			users.append(User.copy(new_user))
		self.write_all_users(users)
if __name__ == '__main__':
	udb = UserDB()
	udb.find_user('person@email.com')