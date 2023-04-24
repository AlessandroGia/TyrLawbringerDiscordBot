DROP DATABASE IF EXISTS statsXP;
CREATE DATABASE statsXP;

\c statsXP;

CREATE SCHEMA statsXP;

CREATE TABLE user (
    id_user INT NOT NULL,
    id_guild INT NOT NULL,
    id_role INT NOT NULL,
    points INT NOT NULL,
    "index" INT NOT NULL,
    FOREIGN KEY (id_guild) REFERENCES guild(id),
    FOREIGN KEY (id_role) REFERENCES role(id)
);

CREATE TABLE guild (
    id SERIAL PRIMARY KEY,
    id_guild INT NOT NULL,
);

CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    id_role INT NOT NULL
);

