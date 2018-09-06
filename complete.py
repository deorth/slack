#!/usr/bin/env python

import cgi
import requests
import todoslib
import json

# get payload from slack
mylist = vars(cgi.FieldStorage())["list"][0].value
callback = json.loads(mylist)

response_url = callback["response_url"]
todo_id = callback["actions"][0]["value"]
user_id = callback["user"]["id"]
action = callback["actions"][0]["name"]

if (action == "incomplete"):
    complete = 0
else:
    complete = 1

post_msg = todoslib.complete_todo(todo_id, user_id, complete)

r = requests.post(response_url, data=post_msg)

print("Content-type: text/plain\n")
