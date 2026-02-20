**Query**
sqlite3 intership.db

.open internship.db

.database

**SQL Data Definition (DDL)**

create table interns(id INTEGER PRIMARY KEY, name TEXT NOT NULL, track TEXT NOT NULL, stipend INTEGER);

**SQL Data Manipulation (DML)**

INSERT into interns VALUES(01,'Karthik','Data Science',5000);
INSERT into interns VALUES(02,'Bhavish','Web Developer',6000);
INSERT into interns VALUES(03,'Adithya','Data Analyst',4000);
INSERT into interns VALUES(04,'Dilan','Full Stack Dev',3000);
INSERT into interns VALUES(05,'Dhanush','Frontend Dev',10000);

**SQL Data Query (DQL)**
select name,track from interns;
select \* from interns;
