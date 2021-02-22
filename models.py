from peewee import *
import base64
import hashlib
import imp
import os

db = SqliteDatabase('Modules.db')

class Module(Model):
	name = CharField(unique=True)
	author = CharField(default='')
	version = CharField(default='0.1')
	code = TextField()
	icon = CharField(default="")
	description = TextField(default="")
	hash_signature =  CharField()
	requirements = CharField(default='')
	app_type = CharField(default='app')

	@property
	def file(self):
		raise AttributeError('file is not a readable attribute')

	@file.setter
	def file(self, file):
		file = os.path.join(file, 'main.py')
		with open(file) as f:
			data = f.read()
			self.code = data.encode('hex')
			sha = hashlib.sha256()
			sha.update(data)
			self.hash_signature = sha.hexdigest()
	@property
	def get_code(self):
		return self.code.decode('hex')

	def load(self):
		module = imp.new_module(self.name)
		exec self.get_code() in module.__dict__
		return module

		#except Exception as e:
		#	print str(e)
		#	return None


	class Meta:
		database = db


class Library(Model):
	name = CharField()
	code = TextField()
	description = TextField(default='')
	hash_signature =  CharField()
	requirements = CharField(default='')

	@staticmethod
	def load(name):
		try:
			lib = Library.get(name=name)
			module = imp.new_module(name)
			exec lib.get_code in module.__dict__
			return module

		except Exception as e:
			print str(e)
			return None


	@property
	def get_code(self):
		return self.code.encode('hex')


	@property
	def file(self):
		raise AttributeError('file is not a readable attribute')

	@file.setter
	def file(self, file):
		with open(file) as f:
			data = f.read()
			self.code = data.encode('hex')
			sha = hashlib.sha256()
			sha.update(data)
			self.hash_signature = sha.hexdigest()

	class Meta:
		database = db


db.create_tables([Module, Library], safe=True)
