#!/usr/bin/python3

import datetime as dt
from sys import argv
from os import path, system
import os

#### TODO App
class ToDo:
	"""docstring for ToDo"""
	def __init__(self):
		
		self.usage = '''Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics'''

	def __repr__(self):
		return self.usage

	def __str__(self):
		return self.usage


	def write_in_file(self, file, content):
		if not path.exists(file):
			system('touch '+file)
		
		with open(file, 'a+') as f:
			if type(content) == list:
				for i in content:
					f.write(i)
			else:
				f.write(content)


	def add(self, task):
		with open('todo.txt', 'a+') as f:
				f.write(task+'\n')
		print(f'Added todo: "{task}"')


	def ls(self):
		## print in reversed order
		len_ = len(self.read('todo.txt'))

		if not len_:
			print("There are no pending todos!")
			return 

		contents = self.read('todo.txt')
		count = len(contents)
		for line in reversed(contents):
			print("[{}] {}".format(count, line.strip()))
			count -= 1


	def done(self, num):
		todo_len = len(self.read('todo.txt'))
		if todo_len and todo_len >= num and num != 0:
			cntnt = self.read('todo.txt', num-1)

			self.write_in_file('done.txt', cntnt)

			# delete from todo
			contents = self.read('todo.txt')
			os.unlink('todo.txt')

			for ind, content in enumerate(contents):
				if ind != num-1:
					# print('writing', content)
					self.write_in_file('todo.txt', content)

			if num == 1:
				os.system('touch todo.txt')

			print(f"Marked todo #{num} as done.")

		else:
			print(f"Error: todo #{num} does not exist.")



	def del_(self, num):
		# delete from todo
		todo_len = len(self.read('todo.txt'))

		if todo_len >= num and num != 0:
		
			contents = self.read('todo.txt')
			os.unlink('todo.txt')

			for ind, content in enumerate(contents):
				if ind != num-1:
					# print('writing', content)
					self.write_in_file('todo.txt', content)

			if todo_len == 1:
				os.system('touch todo.txt')

			print(f"Deleted todo #{num}")

		else:
			print(f"Error: todo #{num} does not exist. Nothing deleted.")



	def read(self, file, num=None):
		with open(file, 'r+') as f:
			lines = f.readlines()
			# print(lines)
			if num is not None:
				line = lines[num]
				# print(num, line , lines)
				return line
			else:
				# print('lines')
				return lines


	def trunc_file(self, file):
		os.unlink(file)
		os.system('touch ' + file)


	def help(self):
		print(self.usage)


	def report(self):
		date = dt.date.today()
		print("{} Pending : {} Completed : {}".format(date.strftime("%Y-%m-%d"), \
			len(self.read('todo.txt')), len(self.read('done.txt'))))


if __name__ == '__main__':
	todo = ToDo()

	# todo.trunc_file('todo.txt')
	# todo.trunc_file('done.txt')
	
	args = argv[1:]
	len_ = len(args)

	if len_ == 1:
		if args[0] == 'ls':
			todo.ls()
		elif args[0] == 'report':
			todo.report()
		elif args[0] == 'help':
			todo.help()
		elif args[0] == 'add':
			print("Error: Missing todo string. Nothing added!")
		elif args[0] == 'del':
			print("Error: Missing NUMBER for deleting todo.")
		elif args[0] == 'done':
			print("Error: Missing NUMBER for marking todo as done.")
		
		else:
			todo.help()

	elif len_ == 2:
		if args[0] == 'add':
			todo.add(args[1])
		elif args[0] == 'del':
			todo.del_(int(args[1]))
		elif args[0] == 'done':
			todo.done(int(args[1]))
		
	else:
		todo.help()
