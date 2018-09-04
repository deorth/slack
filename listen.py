#!/home/d3l1r1um/opt/python-3.6.6/bin/python3

import cgi

print("Content-Type: text/plain\n")

payload = cgi.FieldStorage()
myvars = vars(payload)
mylist = myvars["list"]

request_file = open("request-data", "w")

for x in mylist:
    name = x.name
    value = x.value
    request_file.write("{0} : {1}\n".format(name, value))
    
request_file.close()
