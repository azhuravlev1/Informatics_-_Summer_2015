"""
The Predictive
Version 1.3.1 Dr Who
Settings launcher for working with libraries
"""

class SETTINGS:
	name = "Default"
	library = None
	autodidact = True

class LIBRARY:
	name = "Default"
	filename = "default.txt"
	statistics = {}
	version = "1.3.1"
	reliability = 0.0
	maxwords = 1
	lock = False

def file_restore(lib):
	global libraries
	global version
	lib.filename = lib.name + ".libt"
	l = open(lib.filename , 'w')
	lock = ""
	if lib.lock == True:
		lock = "LOCKED"
	l.write("<info" + "\n" + lib.name + "\n" + lib.version + "\n" + str(lib.reliability) + "\n" + str(lib.maxwords) + "\n" + lock + "\ninfo>")
	l.write("\n" + str(lib.statistics))
	l.close()

version = "1.2.3"
all_vers = ["1.0.2" , "1.0.3" , "1.1.1" , "1.1.3" , "1.1.4" , "1.1.5" , "1.1.6" , "1.2.0" , "1.2.2" , "1.2.4" , "1.3.0" , "1.3.1"]
lib_def = LIBRARY()
libraries = [lib_def]
file_restore(lib_def)
set_def = SETTINGS()
set_def.library = lib_def
settings = set_def

commands_info = {"'help'" : "list of commands" , "'info'" : "current settings information" , "'new_lib'" : "create a new statistics library"}
commands_info.update({"'libraries'" : "list of existing statistics libraries" , "'change_lib'" : "change current statistics library"})
commands_info.update({"'quit'" : "stop this console" , "'stop_console'" : "stop this console" , "'close_dialogue'" : "stop this console"})
commands_info.update({"'new_adid'" : "create a new empty *.adid training file"})
commands_info.update({"'run_text'" : "run machine learning on a certain text" , "'restore_lib'" : "restore a library from a statistics file"})

def new_lib_dialog():
	print("Type the name of the new statistics library")
	print("new_lib >>>\n")
	comnd = input()
	global settings
	global libraries
	global LIBRARY
	global version
	exists = False
	for lib in libraries:
		if lib.name == comnd:
			exists = True
	if exists:
		print("There already exists a library with this name.")
		return(new_lib_dialog())
	else:
		new_lib = LIBRARY()
		new_lib.name = comnd
		print("Would you like to apply special changes to the new library?")
		print("new_lib >>>\n")
		if yes_no(input()):
			print("You may change the version by typing 'version', maximum words with 'maxwords' and lock with 'lock'. Type 'quit' to leave this mode.")
			print("new_lib >>>\n")
			comnd = input()
			while not comnd == "quit":
				if comnd == "version":
					print("You may choose one of the following versions:")
					print(all_vers)
					print("Current version is " + version)
					print("Customizing versions of the libraries is not recommended.")
					print("new_lib >>>\n")
					comnd = input()
					if comnd in all_vers:
						new_lib.version = comnd
						print("The library version is successfully changed.")
					else:
						print("Such version is inavailable.")
				elif comnd == "maxwords":
					print("Input the maximum ammount of words to be analysed.")
					print("new_lib >>>\n")
					new_lib.maxwords = max(1 , min(7 , int(input())))
					print("The maximum ammount of words is successfully changed.")
				elif comnd == "lock":
					print("Would you like to lock the library so that its statistics didn't change?")
					print("yes_no >>>\n")
					if yes_no(input()):
						new_lib.lock = True
						print("The library is now locked.")
					else:
						new_lib.lock = False
						print("The library is now unlocked.")
				else:
					print("There is no similar command. It may appear in the following versions.")
				print("new_lib >>>\n")
				comnd = input()
		file_restore(new_lib)
		print("A new library called '" + new_lib.name + "' is successfuly saved.")
		return(new_lib)

def yes_no(ansr):
	yep = {"Yes" , "YES" , "yes" , "Y" , "y" , "Yep" , "yep" , "YEP" , "Yeah" , "yeah" , "Ye" , "YE" , "ye" , "YEAH" , "Sure" , "SURE" , "sure"}
	nope = {"No" , "NO" , "no" , "N" , "n" , "Nope" , "nope" , "NOPE" , "Noah" , "noah" , "NOAH"}
	if ansr in yep:
		return(1)
	elif ansr in nope:
		return(0)
	else:
		print("You should answer in a way, similar to 'Yes'/'No'.")
		print("yes_no >>>\n")
		return(yes_no(input()))

def didaction(tex , libr):
	stats = libr.statistics
	for i in range(len(tex) - 1):
		if tex[i] in stats:
			if tex[i+1] in stats[tex[i]]:
				stats[tex[i]][tex[i+1]] += 1
			else:
				stats[tex[i]][tex[i+1]] = 1
		else:
			stats[tex[i]] = {tex[i+1] : 1}

def word_output(word , libr):
	stats = libr.statistics
	for vr in stats[word]:
		best = vr
		break
	for vr in stats[word]:
		if stats[word][vr] > stats[word][best]:
			best = vr
	return(best)



"""
STARTS HERE:
"""

def change_lib():
	global settings
	global libraries
	global yes_no
	print("Input the name of the statistics library or 'libraries' to see the list of libraries.")
	print("change_lib >>>\n")
	comnd = input()
	key = 1
	if comnd == "libraries":
		if libraries == None:
			print("No libraries yet, but you can create one now.")
			key = 0
		else:
			print("Here is the list of existing statistics libraries:")
			for lib in libraries:
				print(lib.name)
			print("Which library would you use?")
			print("change_lib >>>\n")
			comnd = input()
			key = 1
	if key:
		exists = False
		for lib in libraries:
			if lib.name == comnd:
				key = 0
				if not version == lib.version:
					print("The library version is " + str(lib.version) + ", which is lower than current " + str(version) + ".")
					key = 1
				if lib.reliability<0.25 and key==0:
					print("The rate of this library is " + str(lib.reliability) + ", which is quite low.")
					key = 1
				elif lib.reliability<0.25:
					print("Also, the rate of this library is " + str(lib.reliability) + ", which is quite low.")
					print("So this statistics library has a low reliability.")
				if key:
					print("Are you sure you would like to proceed?")
					print("yes_no >>>\n")
					if yes_no(input()):
						settings.library = lib
						exists = True
					else:
						print("You may choose another library from the 'libraries' list.")
						return(0)
				else:
					settings.library = lib
					exists = True
		if exists:
			if settings.library.lock:
				settings.autodidact = False
			print("The changes are applied, you may type 'info' to check them.")
		else:
			print("No library with such name found, but you can create one now.")

def new_lib():
	global settings
	global libraries
	global LIBRARY
	global new_lib_dialog
	global yes_no
	libraries.append(new_lib_dialog())
	print("Would you like to use this library now?")
	print("yes_no >>>\n")
	a = yes_no(input())
	if a:
		settings.library = libraries[-1]
		print("The changes are applied, you may type 'info' to check them.")
	else:
		print("You may apply it later by typing 'change_lib'.")

def run_text():
	global settings
	global libraries
	global LIBRARY
	global didaction
	global yes_no
	if settings.autodidact and not settings.library.lock:
		print("Which library would you like to edit? Current library is " + settings.library.name + ". Type 'libraries' for the list of all libraries.")
		print("run_text >>>\n")
		comnd = input()
		key = 1
		if comnd == "libraries":
			if libraries == None:
				print("No libraries yet, but you can create one now.")
				key = 0
			else:
				print("Here is the list of existing statistics libraries:")
				for lib in libraries:
					print(lib.name)
				print("Which library would you use?")
				print("run_text >>>\n")
				comnd = input()
				key = 1
		if key:
			exists = False
			for lib in libraries:
				if lib.name == comnd:
					if not version == lib.version:
						print("The library version is " + str(lib.version) + ", which is lower than current " + str(version) + ".")
						print("Are you sure you would like to proceed?")
						print("yes_no >>>\n")
						if yes_no(input()):
							libr = lib
							exists = True
						else:
							print("You may change the library later. Now you will return home.")
							return(0)
					else:
						libr = lib
						exists = True
			if exists:
				print("Input the name of the *.txt or *.adid file. Example: 'Great_Gatsby.txt' . NB: the file should be in the same directory as the app.")
				print("run_text >>>\n")
				filename = input()
				didact = []
				try:
					t = open(filename , 'rt')
					for line in t:
						didact.extend(line.split())
					t.close()
					didaction(didact , libr)
					file_restore(libr)
					print("The " + libr.name + " library is successfully updated.")
				except IOError or EOFError:
					print("There is no appropriate file with such name in the directory. You now will return home.")
			else:
				print("No library with such name found, but you can create one now. You will return home.")
	else:
		print("Machine learning is currently locked. Try to enable autodidaction or change the library.")

def restore_lib():
	global settings
	global libraries
	global LIBRARY
	global yes_no
	print("Input the name of the *.libt file. Example: 'Queru.libt' . NB: the file should be in the same directory as the app.")
	print("restore_lib >>>\n")
	filename = input()
	info = []
	inf = True
	try:
		t = open(filename , 'rt')
		new_lib = LIBRARY()
		new_lib.filename = filename
		new_lib.statistics = {}
		for line in t:
			if inf:
				info.extend(line.split())
				if info[-1] == "info>":
					inf = False
			else:
				new_lib.statistics.update(eval(line))
		print(info)
		t.close()
		new_lib.name = info[1]
		new_lib.version = info[2]
		new_lib.reliability = float(info[3])
		new_lib.maxwords = int(info[4])
		if info[5] == "LOCKED":
			new_lib.lock = True
		libraries.append(new_lib)
		print("A new library called '" + new_lib.name + "' is successfuly saved.")
		print("Would you like to use this library now?")
		print("yes_no >>>\n")
		a = yes_no(input())
		if a:
			settings.library = libraries[-1]
			print("The changes are applied, you may type 'info' to check them.")
		else:
			print("You may apply it later by typing 'change_lib'.")
	except IOError or EOFError:
		print("There is no appropriate *.libt file in the directory. You now will return home.")


def start(command): 
	global settings
	global commands_info
	global libraries
	global LIBRARY
	global new_lib_dialog
	global yes_no
	global didaction
	global change_lib
	global new_lib
	global restore_lib
	global file_restore
	global run_text

	if command == "help" or command == "Help":
		print("Here is the list of available commands:")
		for c in commands_info:
			print(c , "-" , commands_info[c])

	elif command == "info" or command == "Info":
		print("Here is the information about current settings:")
		print(settings.name)
		print("Statistics library:" , settings.library.name)
		print("Statistics reliability:" , str(settings.library.reliability * 100) + "%")
		print("Machine learning mode:" , settings.autodidact)

	elif command == "libraries":
		if len(libraries):
			print("Here is the list of existing statistics libraries:")
			for lib in libraries:
				print(lib.name)
		else:
			print("No libraries yet, but you can create one now")

	elif command == "new_adid":
		print("Type in the name of the new machine learning file. Example: Great_Gatsby.")
		print("new_adid >>>\n")
		filename = input() + ".adid"
		l = open(filename , 'w')
		l.close()
		print(filename , "is successfully saved to the  app directory.")

	elif command == "change_lib":
		change_lib()

	elif command == "new_lib":
		new_lib()

	elif command == "run_text":
		run_text()

	elif command == "restore_lib":
		restore_lib()
	elif command in {"stop_console" , "close_dialogue" , "quit"}:
		return(1)

	elif (command[0] == "'" or command[0] == '"') and (command[-1] == "'" or command[-1] == '"'):
		word = command[1 : -1]
		if word in settings.library.statistics:
			print(word_output(word , settings.library))
		else:
			print("No such word in current library.")

	else:
		print("There is no similar command. It may appear in the following versions.")
		print("You may type 'help' to see possible commands.")
		print("home >>>\n")
		return(start(input()))

	return(0)

print("Input command or library word in 'quotes'.")
print("Type 'help' to see possible commands or 'info' to see current settings.")
end = 0
while not end:
	print("home >>>\n")
	end = start(input())
