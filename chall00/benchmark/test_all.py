# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_all.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: niragne <niragne@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/04/10 16:04:46 by niragne           #+#    #+#              #
#    Updated: 2020/04/12 14:34:58 by niragne          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import atexit
import os
import signal
import subprocess
import resource
from termcolor import colored

_BENCHMARK_SRC	= "benchmark.c"
_BENCHMARK_OBJ	= "benchmark.o"
_MEMTEST_SRC	= "memtest.c"
_MEMTEST_OBJ	= "memtest.o"
_LOGIN_SRC		= ""
_EXECNAME		= "./__temp"
_TESTS_PATH		= "../"
_RESULT_PATH	= "./results"
_TIMEOUT		= 40
_BLACKLIST		= ["benchmark.c"]

class Answer:
	def __init__(self, filename, fd):
		self.filename = filename
		self.fd = fd
		self.state = 0
		self.ok = 1

class Benchmark:
	def __init__(self):
		self.total = 0
		self.passed = 0
		self.failed = 0
		self.timedout = 0
		self.crashed = 0
		self.compile_error = 0
		self.failed_memtest = 0
		self.total_failed = 0
	
	def display_results(self):
		self.total_failed = self.total - self.passed
		print("Total : " + str(self.total) + " files tested, " + str(self.passed) + " files passed and " + str(self.total_failed) + " files failed")
		print("PASSED: " + str(self.passed) + "\tKO: " + str(self.failed) + "\tCRASH: " + str(self.crashed) + "\tTIMEOUT: " + str(self.timedout) + "\tCOMPILE ERROR: " + str(self.compile_error)+ "\tMEMTEST KO: " + str(self.failed_memtest))


def	exec_command(cmd):
	p = subprocess.check_output(args=cmd, stderr=subprocess.STDOUT, universal_newlines=True, timeout=_TIMEOUT)
	return p

def cleanup():
	exec_command(["/bin/rm", "-rf", _BENCHMARK_OBJ, _EXECNAME, _MEMTEST_OBJ])

def process_benchmark(benchmark, current_test):
	try:
		exec_command(["gcc", "-O3", _TESTS_PATH + current_test.filename, _BENCHMARK_OBJ, "-o", _EXECNAME])
	except subprocess.CalledProcessError as truc:
		benchmark.compile_error += 1
		current_test.ok = 0
		current_test.fd.write(truc.output)
		return (colored("ERROR", "red"))
	try:
		ret = exec_command([_EXECNAME])
	except subprocess.CalledProcessError as truc:
		current_test.fd.write(truc.output)
		current_test.ok = 0
		if truc.returncode < 0:
			benchmark.crashed += 1
			return(colored("CRASH", "red"))
		else: 
			benchmark.failed += 1
			return(colored("KO (" + str(truc.returncode) + " test(s) failed)", "red")) 
	except subprocess.TimeoutExpired:
		current_test.ok = 0
		benchmark.timedout += 1
		current_test.fd.write("Timed out after %d seconds" % _TIMEOUT)
		return(colored("TIMEOUT", "red"))
	current_test.fd.write(ret)
	return (colored("OK", "green"))

def process_memtest(benchmark, current_test):
	try:
		exec_command(["gcc", "-g3", _TESTS_PATH + current_test.filename, _MEMTEST_OBJ, "-o", _EXECNAME, "-fsanitize=address"])
	except subprocess.CalledProcessError as truc:
		current_test.ok = 0
		current_test.fd.write(truc.output)
		return (colored("ERROR", "red"))
	try:
		ret = exec_command([_EXECNAME])
	except subprocess.CalledProcessError as truc:
		current_test.ok = 0
		current_test.fd.write(truc.output)
		benchmark.failed_memtest += 1
		if truc.returncode < 0:
			return(colored("CRASH", "red"))
		else: 
			return(colored("KO", "red")) 
	except subprocess.TimeoutExpired:
		current_test.ok = 0
		benchmark.failed_memtest += 1
		current_test.fd.write("Timed out after %d seconds" % _TIMEOUT)
		return(colored("TIMEOUT", "red"))
	current_test.fd.write(ret)
	return (colored("OK", "green"))

def main():
	soft, hard = resource.getrlimit(resource.RLIMIT_DATA)
	benchmark = Benchmark()
	exec_command(["gcc", "-c", _BENCHMARK_SRC])
	exec_command(["gcc", "-c", _MEMTEST_SRC, "-fsanitize=address"])

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
			current_test = Answer(filename, fd)
			benchmark.total += 1
			resource.setrlimit(resource.RLIMIT_DATA, (1e9, hard))
			tests_results = process_benchmark(benchmark, current_test)
			resource.setrlimit(resource.RLIMIT_DATA, (soft, hard))
			memtest_results = process_memtest(benchmark, current_test)

			print(filename + ":\tMEMTEST: " + memtest_results + "\tTESTS: " + tests_results)
			benchmark.passed += current_test.ok
			current_test.fd.close()

	
	benchmark.display_results()

if __name__ == "__main__":
	atexit.register(cleanup)
	main()
