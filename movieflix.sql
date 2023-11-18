DROP DATABASE db_movieflix;
CREATE DATABASE db_movieflix;
USE db_movieflix;



CREATE USER 'sean'@'localhost' IDENTIFIED BY 'jj001109';
GRANT ALL PRIVILEGES ON *.* TO 'sean'@'localhost';
FLUSH PRIVILEGES;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(80) NOT NULL
);

