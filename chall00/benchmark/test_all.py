# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_all.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: niragne <niragne@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/04/10 16:04:46 by niragne           #+#    #+#              #
#    Updated: 2020/04/11 13:28:38 by niragne          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import subprocess
from termcolor import colored

_BENCHMARK_SRC	= "benchmark.c"
_BENCHMARK_OBJ	= "benchmark.o"
_LOGIN_SRC		= "emartine.c"
_EXECNAME		= "__temp"
_TESTS_PATH		= "../"
_RESULT_PATH	= "./results"
_TIMEOUT		= 6
_BLACKLIST		= ["benchmark.c"]

def	exec_command(cmd):
	p = subprocess.check_output(args=cmd, stderr=subprocess.STDOUT, universal_newlines=True, timeout=_TIMEOUT)
	return p

def main():
	exec_command(["g++", "-c", _BENCHMARK_SRC])
	total = 0
	passed = 0
	failed = 0
	timedout = 0
	crashed = 0
	compile_error = 0
	total_failed = 0

	if not (os.path.exists(_RESULT_PATH) and os.path.isdir(_RESULT_PATH)):
		try:
			os.mkdir(_RESULT_PATH)
		except:
			print("error: could not create %s directory. aborting" % _RESULT_PATH)
			return

	for filename in os.listdir(_TESTS_PATH):
		if filename.endswith(".c") and filename not in _BLACKLIST:

			try:
				current_file = _RESULT_PATH + "/" + filename[:-2] + ".txt"
				fd = open(current_file, "w+")
			except:
				print("error: could not open %s. aborting" % current_file)
			total += 1
			try:
				exec_command(["gcc", "-O3", _TESTS_PATH + filename, _BENCHMARK_SRC, "-o", "a.out"])
			except subprocess.CalledProcessError as truc:
				print(filename + ":\t " + colored("DOES NOT COMPILE", "red"))
				compile_error += 1
				# print(truc.output, end="")
				fd.write(truc.output)
				fd.close()
				continue
			try:
				ret = exec_command(["./a.out"])
			except subprocess.CalledProcessError as truc:
				if truc.returncode < 0:
					print(filename + ":\t " + colored("CRASH", "red"))
					crashed += 1
				else: 
					print(filename + ":\t " + colored("KO (" + str(truc.returncode) + " test(s) failed)", "red")) 
					failed += 1
				fd.write(truc.output)
				fd.close()
				continue
			except subprocess.TimeoutExpired as e:
				timedout += 1
				print(filename + ":\t " + colored("TIMEOUT", "red"))
				fd.write("Timed out after %d seconds" % _TIMEOUT)
				fd.close()
				continue
			print(filename + ":\t " + colored("OK", "green"))
			fd.write(ret)
			passed += 1
			fd.close()
	total_failed = timedout + crashed + failed + compile_error
	print("Total : " + str(total) + " files tested, " + str(passed) + " files passed and " + str(total_failed) + " files failed")
	print("PASSED: " + str(passed) + " KO: " + str(failed) + " TIMEOUT: " + str(timedout) + " COMPILE ERROR: " + str(compile_error))

if __name__ == "__main__":
	main()
