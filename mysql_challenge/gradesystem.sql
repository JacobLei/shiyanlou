DROP DATABASE gradesystem;

CREATE DATABASE gradesystem;

use gradesystem;

CREATE TABLE student
(
sid    INT(10)  PRIMARY KEY,
sname  CHAR(20) NOT NULL,
gender CHAR(10)  NOT NULL
);

CREATE TABLE course
(
cid   INT(10)  PRIMARY KEY,
cname CHAR(20) NOT NULL
);

CREATE TABLE mark
(
mid   INT(10) PRIMARY KEY,
sid   INT(10) NOT NULL,
cid   INT(10) NOT NULL,
score INT(10) NOT NULL,
CONSTRAINT mark_pk FOREIGN KEY (sid) REFERENCES student(sid),
CONSTRAINT mark_pk1 FOREIGN KEY (cid) REFERENCES course(cid)
);

INSERT INTO student VALUES(1, 'Tom', 'male');
INSERT INTO student VALUES(2, 'Jack', 'male');
INSERT INTO student VALUES(3, 'Rose', 'female');
INSERT INTO course VALUES(1, 'math');	
INSERT INTO course VALUES(2, 'physics');	
INSERT INTO course VALUES(3, 'chemistry');	
INSERT INTO mark VALUES(1, 1, 1, 80);
INSERT INTO mark VALUES(2, 2, 1, 85);
INSERT INTO mark VALUES(3, 3, 1, 90);
INSERT INTO mark VALUES(4, 1, 2, 60);
INSERT INTO mark VALUES(5, 2, 2, 90);
INSERT INTO mark VALUES(6, 3, 2, 75);
INSERT INTO mark VALUES(7, 1, 3, 95);
INSERT INTO mark VALUES(8, 2, 3, 75);
INSERT INTO mark VALUES(9, 3, 3, 85);

