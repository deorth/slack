# Slack ToDoS App

Application requirements (tested with):
* Python 3.6.6 (add'l module required: requests)
* MySQL Server 5.6.34
* Apache with FastCGI (whatever my shared host happened to be running)

The application consists of 3 required files:

* [`todos.py`](todos.py)
* [`todoslib.py`](todoslib.py)
* [`complete.py`](complete.py)

Two SQL files are also provided.

* [`dbinit.sql`](dbinit.sql) initializes and populates the required MySQL tables. **It will drop the `slack_todos` table, removing all existing tasks!**
* [`test-data.sql`](test-data.sql) adds some test tasks to the database (replace `SLACK_USER_ID` with your Slack user ID before running!)

To set up the environment:

* Edit the python path in each `*.py` file if necessary (points to whatever python is found first in the runtime environment by default)
* Edit the database configuration at the beginning of `todoslib.py`
* Initialize the database configuration by sourcing `dbinit.sql`

Supported commands:

* `/todos` shows your incomplete tasks
* `/todos all` shows your complete and incomplete tasks
* `/todos add _task description_ #priority` adds a new task
  * `#priority` is optional and defaults to `#med`
  * valid priority values are `#high`, `#med`, and `#low` (don't forget the #!)

The application should always reply privately, even if the slash command is issued in a public channel.

Dev notes:

* The biggest issue that would keep this app from being actually usable is its lack of constraints on the number of tasks (and therefore, number of message attachments) it displays. Ideally, it would limit the number of displayed tasks to 10 (though Slack's advised limit is 20) and then offer some sort of pagination ability to view 10 more, etc.
