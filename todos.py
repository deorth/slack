#!/home/d3l1r1um/opt/python-3.6.6/bin/python3

import cgi
import requests

print("Content-Type: text/plain\n")

# get payload from slack
mylist = vars(cgi.FieldStorage())["list"]

# expected vars
user_id = ""
response_url = ""
command = ""
text = ""

for x in mylist:
    name = x.name
    value = x.value

    if (name == "user_id"):
        user_id = value

    if (name == "response_url"):
        response_url = value

    if (name == "command"):
        command = value

    if (name == "text"):
        text = value

# escape special characters

text = cgi.escape(text)
        
# could theoretically check if any of the other expected vars are
# missing from the payload, but that would mean there's a problem
# bigger than the scope of my app and it didn't seem too important to
# handle in this exercise

if (text == ""):
    post_msg = "Thank you for your message. Your command {0} was received without parameters.\n".format(command)
else:
    post_msg = "Thank you for your message. Your command {0} with parameters \"{1}\" was received.\n".format(command, text)

data = {}
data["text"] = post_msg
post_data = str(data).encode("utf-8")

r = requests.post(response_url, data=post_data)
