#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

def read_json(file_name):
	exists = os.path.exists(file_name)
	file = {}
	if exists:
		with open(file_name) as f:
			file = json.load(f)
	else:
		file['sender_id'] = '-'
		file['last_step'] = '-'
		with open(file_name, 'w') as f:
			json.dump(file, f)
	return file

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