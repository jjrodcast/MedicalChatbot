#!/usr/bin/env python
# -*- coding: utf-8 -*-
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