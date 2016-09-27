CREATE DATABASE IF NOT EXISTS inventaire;

USE inventaire;

CREATE TABLE IF NOT EXISTS upc (
        number VARCHAR(50) NOT NULL PRIMARY KEY,
        description VARCHAR(500) NOT NULL,
        size_weight VARCHAR(50) NOT NULL,
        source ENUM('upc_db','generated','real') NOT NULL
        );
INSERT IGNORE INTO upc (number, description, size_weight, source) VALUES ('0060410074978','32i0 grams Tostitos Tortilla Chip - Bite Size Rounds - Premium White Corn','320g','upc_db');
INSERT IGNORE INTO upc (number, description, size_weight, source) VALUES ('0069000014257','355ml/12fl.oz. Canadian Diet Pepsi','355ml','upc_db');

CREATE TABLE IF NOT EXISTS stock (
        upc VARCHAR(50) NOT NULL PRIMARY KEY,
        description VARCHAR(500) NOT NULL,
        expiration DATE NOT NULL,
        date_achat DATE NOT NULL,
        CONSTRAINT `fk_new_table_1`
        FOREIGN KEY (`upc`)
        REFERENCES `inventaire`.`upc` (`number`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
        );

