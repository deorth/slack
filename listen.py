#!/home/d3l1r1um/opt/python-3.6.6/bin/python3

import cgi
import requests

print("Content-Type: text/plain\n")

mylist = vars(cgi.FieldStorage())["list"]

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

# could theoretically check if any of the expected vars are missing from the payload,
# but that would mean there's a problem bigger than the scope of my app and it didn't
# seem too important to handle in this exercise
        
post_msg = "Thank you for your message. Your command {0} with parameters \"{1}\" was received.\n".format(command, text)

data = {}
data["text"] = post_msg
post_data = str(data).encode("utf-8")

r = requests.post(response_url, data=post_data)
