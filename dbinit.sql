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

INSERT INTO slack_todos_priorities
    VALUES (1, "high", "#ff0000"),
           (2, "med", "#0000ff"),
           (3, "low", "#00ff00");
