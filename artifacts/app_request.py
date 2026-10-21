import json
import urllib.request


base_url = 'http://127.0.0.1:5000'

def test_get_log() -> None:
	url = base_url + '/log'
	request = urllib.request.Request(url, method='GET')
	request.add_header('Content-Type', '')
	with urllib.request.urlopen(request) as response: ...

def test_get_health() -> None:
	url = base_url + '/health'
	request = urllib.request.Request(url, method='GET')
	request.add_header('Content-Type', '')
	with urllib.request.urlopen(request) as response: ...

def test_get_api_v1_todos() -> None:
	url = base_url + '/api/v1/todos'
	request = urllib.request.Request(url, method='GET')
	request.add_header('Content-Type', '')
	with urllib.request.urlopen(request) as response: ...

def test_get_api_v1_todos_todo_id() -> None:
	url = base_url + '/api/v1/todos/todo_id'
	request = urllib.request.Request(url, method='GET')
	request.add_header('Content-Type', '')
	with urllib.request.urlopen(request) as response: ...

def test_post_api_v1_todos() -> None:
	url = base_url + '/api/v1/todos'
	data = json.dumps({'title': 'string', 'description': 'str-obj'}).encode()
	request = urllib.request.Request(url, data=data, method='POST')
	request.add_header('Content-Type', 'application/json')
	with urllib.request.urlopen(request) as response: ...

def test_patch_api_v1_todos_todo_id() -> None:
	url = base_url + '/api/v1/todos/todo_id'
	data = json.dumps({'title': 'str-obj', 'description': 'value', 'completed': True}).encode()
	request = urllib.request.Request(url, data=data, method='PATCH')
	request.add_header('Content-Type', 'application/json')
	with urllib.request.urlopen(request) as response: ...

def test_delete_api_v1_todos_todo_id() -> None:
	url = base_url + '/api/v1/todos/todo_id'
	request = urllib.request.Request(url, method='DELETE')
	request.add_header('Content-Type', '')
	with urllib.request.urlopen(request) as response: ...
