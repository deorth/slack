DROP TABLE slack_todos;
DROP TABLE slack_todos_priorities;

CREATE TABLE slack_todos(
    id INT AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL,
    todo VARCHAR(255) NOT NULL,
    priority INT NOT NULL,
    complete BOOLEAN NOT NULL,
    PRIMARY KEY (id)
) ENGINE InnoDB;

CREATE TABLE slack_todos_priorities(
    id INT AUTO_INCREMENT,
    priority VARCHAR(10) NOT NULL,
    color VARCHAR(7) NOT NULL,
    PRIMARY KEY (id)
) ENGINE InnoDB;

INSERT INTO slack_todos
    VALUES (1, "UCKDCBLAE", "Write Slack app", 1, false),
           (2, "UCKDCBLAE", "Write tests", 1, false),
           (3, "UCKDCBLAE", "Clean up code", 1, false),
           (4, "UCKDCBLAE", "Eat lunch", 2, false),
           (5, "UCKDCBLAE", "Goof around on Facebook", 3, false);

INSERT INTO slack_todos_priorities
    VALUES (1, "high", "#ff0000"),
           (2, "med", "#0000ff"),
           (3, "low", "#00ff00");
