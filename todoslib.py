#!/home/d3l1r1um/opt/python-3.6.6/bin/python3

import MySQLdb

# an earlier version of this file had credentials exposed. rather than
# tinker with git history, i changed my db password :)
host = "xxx"
user = "xxx"
passwd = "xxx"
dbase = "xxx"

def get_todos(user_id):

    db = MySQLdb.connect(host, user, passwd, dbase)

    cur = db.cursor()

    todo_list = {}

    cur.execute("SELECT a.id, a.todo, b.color FROM slack_todos a INNER JOIN slack_todos_priorities b on a.priority = b.id WHERE a.user_id=%s AND a.complete=0 order by a.priority, a.id;", [user_id])

    for row in cur.fetchall():
        todo_id = row[0]
        text = row[1]
        priority_color = row[2]

        todo_list[todo_id] = (priority_color, text)

    db.close()
    return todo_list

def get_all_todos(user_id):

    db = MySQLdb.connect(host, user, passwd, dbase)

    cur = db.cursor()

    todo_list = {}

    cur.execute("SELECT a.id, a.todo, a.complete, b.color FROM slack_todos a INNER JOIN slack_todos_priorities b on a.priority = b.id WHERE a.user_id=%s order by a.complete, a.priority, a.id;", [user_id])

    for row in cur.fetchall():
        todo_id = row[0]
        text = row[1]
        complete = row[2]
        priority_color = row[3]

        todo_list[todo_id] = (priority_color, text, complete)

    db.close()

    return todo_list

def complete_todo(todo_id, user_id, complete):

    db = MySQLdb.connect(host, user, passwd, dbase)

    result = ""
    cur = db.cursor()

    if (complete == 1):    

        cur.execute("UPDATE slack_todos SET complete = 1 where id=%s and user_id=%s", (todo_id, user_id))

        if (cur.rowcount == 0):
            result = "{\"text\": \":shit: Something went wrong! No matching task found.\", \"replace_original\": false}"
        else:
            result = "{\"text\": \":boom: Task complete!\", \"replace_original\": false}"

    else:
    
        cur.execute("UPDATE slack_todos SET complete = 0 where id=%s and user_id=%s", (todo_id, user_id))

        if (cur.rowcount == 0):
            result = "{\"text\": \":shit: Something went wrong! No matching task found.\", \"replace_original\": false}"
        else:
            result = "{\"text\": \":confounded: Task marked incomplete...\", \"replace_original\": false}"
            
    db.commit()
    db.close()

    return result

def add_todo(user_id, text, priority):

    db = MySQLdb.connect(host, user, passwd, dbase)

    text = text.strip()
    result = ""

    cur = db.cursor()

    dupe_id = 0

    # confirm that passed priority value is valid

    cur.execute("SELECT id FROM slack_todos_priorities where priority = %s", [priority])
    if (cur.rowcount == 0):
        result = "{{\"text\": \"ERROR: Priority #{0} is not a valid priority value. Valid priorities are `#high`, `#med`, and `#low`.\"}}".format(priority)
    else:
        priority_id = cur.fetchone()[0]

        cur.execute("SELECT count(*), id from slack_todos where lower(todo)=%s and user_id=%s and complete=0", (text.lower(), user_id))
        existing_todo = cur.fetchone()
        if (existing_todo[0] != 0):
            # this task is a duplicate (it might have a different priority)
            # duplicate tasks are allowed if all existing ones are completed
            dupe_id = existing_todo[1] # not using for now, but keeping around just in case
            result = "{\"text\": \"ERROR: The same task is already on your to-do list!\"}"
        else:
            # this task is not a duplicate
            cur.execute("INSERT INTO slack_todos (user_id, todo, priority, complete) VALUES (%s, %s,%s,%s)",(user_id, text, priority_id, 0))
            db.commit()
            result = "{\"text\": \"Task added!\"}"

    db.close()

    return result
