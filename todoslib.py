#!/home/d3l1r1um/opt/python-3.6.6/bin/python3

import MySQLdb

def get_todos(user_id):

    db = MySQLdb.connect(host="mysql.vasserman.net",
            user="olgavass",
            passwd="zXqAwG2mquFMshVRRZbAVpaWjJv47H",
            db="olgavass")

    cur = db.cursor()

    todo_list = {}

    cur.execute("SELECT a.id, a.todo, b.color FROM slack_todos a INNER JOIN slack_todos_priorities b on a.priority = b.id WHERE a.user_id=%s AND a.complete=0;", [user_id])

    for row in cur.fetchall():
        todo_id = row[0]
        text = row[1]
        priority_color = row[2]

        todo_list[todo_id] = (priority_color, text)

    db.close()

    return todo_list


'''
def get_all_todos():

def add_todo(text, priority="med"):

    text = text.strip()
    db = MySQLdb.connect(host="mysql.vasserman.net",
                         user="olgavass",
                         passwd="zXqAwG2mquFMshVRRZbAVpaWjJv47H",
                         db="olgavass")

    cur = db.cursor()

    dupe_id = 0
    
    try:
        cur.execute("SELECT id FROM slack_todos_priorities where priority = %s", [priority])
        priority_id = cur.fetchone()[0]
    except:
        print("Could not get priority info from DB")

    try:
        cur.execute("SELECT count(*), id from slack_todos where todo=%s and priority=%s", (text, priority_id))
        existing_todo = cur.fetchone()
        if (existing_todo[0] != 0):
            dupe_id = existing_todo[1]
        else:
            print("This todo item is not a duplicate, adding.")
    except Exception as err:
        print("An exception occurred")
        print(err)

    if (dupe_id != 0):
        print("An identical todo item already exists with ID {0}".format(dupe_id))
    else:
        try:
            cur.execute("INSERT INTO slack_todos (todo, priority, complete) VALUES (%s,%s,%s)",(text, priority_id, 0))
            db.commit()
            db.close()
            return True
        except:
            db.rollback()
            db.close()
            return False
    

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
'''
