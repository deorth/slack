#!/home/d3l1r1um/opt/python-3.6.6/bin/python3

import cgi
import requests

print("Content-Type: text/plain\n")

payload = cgi.FieldStorage()
myvars = vars(payload)
mylist = myvars["list"]

request_file = open("request-data", "w")

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

request_file.write("Command {0} with params {1} was issued by Slack user {2}\n".format(command, text, user_id))
request_file.write("Respond to url {0}\n".format(response_url))

post_msg = "Thank you for your message. Your command {0} with parameters \"{1}\" was received.\n".format(command, text
)

data = {}
data["text"] = post_msg

request_file.write(post_msg)
request_file.write(str(data))

post_data = str(data)

r = requests.post(response_url, data=post_data)

request_file.write("\n{0}\n".format(r.text))

request_file.close()
