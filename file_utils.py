#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

def save_state(new_state):
	file = open('estado.txt', 'w')
	file.write(new_state)
	file.close()

def read_state():
	file = open('estado.txt', 'r')
	state = file.read()
	file.close()
	return state

def load_info():
	file = open('information.txt', 'r')
	info = file.read()
	file.close()
	return info

def save_info(info):
	file = open('information.txt', 'w')
	file.write(info)
	file.close()

def reload_info():
	file = open('informatiion.txt', 'w')
	file.write('')
	file.close()

def read_file(file_name):
	"""Leemos el archivo y mapeamos los datos a un diccionario"""
	content = {}
	file_content = open(file_name, "r")
	for line in file_content:
		if line.startswith('##'):
			name = line[2:].strip()
			if name not in content:
				content[name] = []
		elif line.startswith('-'):
			content[name].append(line[1:])
	file_content.close()
	return content