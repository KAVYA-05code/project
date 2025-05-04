CREATE DATABASE animalshelter;

USE animalshelter;

CREATE TABLE animals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE adoptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT NOT NULL,
    adopter_name VARCHAR(150) NOT NULL,
    adopter_contact VARCHAR(150) NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES animals(id)
);