#!/bin/python

import os

from urllib.parse import urlparse
from pathlib import Path
from string import Template
from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET

file_path = 'climatetrace.sources.v2.list'

group_id = 'org.coypu.data.climatetrace'
version = '0.2.0'
project_prefix = "climatetrace-"

parent_str = "<parent><groupId>org.aksw.data.config</groupId><artifactId>aksw-data-deployment</artifactId><version>0.0.3</version><relativePath></relativePath></parent>"

def capitalize_words(s):
  return ' '.join(word.capitalize() for word in s.split())

def prettify_xml(s):
  return s
  #xml = ET.fromstring(s)
  #ET.indent(xml)
  #result = ET.tostring(xml, encoding='unicode')
  #return result


build_path = 'build'
consumer_path = 'consumer'
os.makedirs(build_path, exist_ok=True)
os.makedirs(consumer_path, exist_ok=True)

env = Environment(loader=FileSystemLoader('resources'))
artifact_template = env.get_template('artifact.template.pom.xml')
parent_template = env.get_template('parent.template.pom.xml')
consumer_template = env.get_template('consumer.template.pom.xml')

# Open the file and process each line
with open(file_path, 'r') as file:
  modules = []
  for line in file:
    line = line.strip()
    if line and not line.startswith('#'):
      parsed_url = urlparse(line)
      # Extracting the local name (last part of the path)
      input_file_fullname = parsed_url.path.split('/')[-1]
      input_file_parts = input_file_fullname.partition('.') # os.path.splitext(input_file_fullname)
      input_file_basename = input_file_parts[0]
      input_file_ext = input_file_parts[2]
      base_name = input_file_basename.replace('_', '-')
      artifact_id = f'{project_prefix}{base_name}'
      output_file_fullname_alt = f'{artifact_id}.{input_file_ext}'
      output_file_fullname = input_file_fullname
      module_name = artifact_id
      tmp_name = base_name.replace('-', ' ')
      sector_name = capitalize_words(tmp_name)
      # print(f'{line} -> {module_name}')
      module = {
        "moduleName": module_name,
        "parentStr": parent_str,
        "groupId": group_id,
        "artifactId": artifact_id,
        "version": version,
        "description": f'Climate TRACE archive for the sector "{sector_name}".',
        "name": f'Climate TRACE - {sector_name}',
        "url": "https://climatetrace.org",
        "licenses": [{
          "name": "Creative Commons Attribution 4.0",
          "url": "https://creativecommons.org/licenses/by/4.0/"
        }],
        "input": {
          "url": line
        },
        "output": {
          "filename": output_file_fullname,
          "filetype": input_file_ext
        }
      }
      rendered = artifact_template.render(this=module)
      rendered = prettify_xml(rendered)
      modules.append(module)
      module_folder=f'{build_path}/{module_name}'
      os.makedirs(module_folder, exist_ok=True)
      with open(f'{module_folder}/pom.xml', "w") as file:
        file.write(rendered)
  parent = {
    "parentStr": parent_str,
    "groupId": group_id,
    "artifactId": f'{project_prefix}parent',
    "version": version,
    "modules": modules
  }
  rendered = parent_template.render(this=parent)
  rendered = prettify_xml(rendered)
  with open(f'{build_path}/pom.xml', "w") as file:
    file.write(rendered)
  consumer = {
    "parentStr": parent_str,
    "groupId": group_id,
    "artifactId": f'{project_prefix}consumer',
    "version": version,
    "modules": modules
  }
  rendered = consumer_template.render(this=consumer)
  rendered = prettify_xml(rendered)
  with open(f'{consumer_path}/pom.xml', "w") as file:
    file.write(rendered)

      
