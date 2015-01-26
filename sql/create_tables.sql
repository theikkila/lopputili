CREATE TABLE accounts (name varchar(40), pk integer primary key, description varchar(400), aid integer, side varchar(13))
CREATE TABLE users (password varchar(40), pk integer primary key, last_name varchar(40), first_name varchar(40), username varchar(40))
CREATE TABLE visits (pk integer primary key, useragent varchar(400), time datetime)
