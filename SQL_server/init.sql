CREATE DATABASE connections

GRANT ALL PRIVILEGES ON DATABASE connections to "postgres";
CREATE TABLE Controllers(
                id serial PRIMARY KEY,
                ip varchar(20) NOT NULL UNIQUE,
                connection boolean);

CREATE TABLE Smartphones(
                id serial PRIMARY KEY,
                ip varchar(20) NOT NULL,
                connection boolean);

CREATE TABLE Pairs(
                id serial PRIMARY KEY,
                id_controller int REFERENCES Controllers(id),
                id_smartphone int REFERENCES Smartphones(id));

