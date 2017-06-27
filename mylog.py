# -*- coding: utf-8 -*-

import time
import sys

INFO = 1
WARNING = 2
ERROR = 3
FATAL = 4

level_prefix_map = {
	INFO : "I",
	WARNING : "W",
	ERROR : "E",
	FATAL : "F"
}

def Log(level, log_str):
	level_prefix = level_prefix_map[level]
	print("[" + level_prefix + str(int(time.time())) + "] " + log_str)

if __name__ == "__main__":
	Log(INFO, "hello")