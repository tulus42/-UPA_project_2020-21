DROP DATABASE IF EXISTS corona;
CREATE DATABASE corona;
USE corona;

DROP TABLE IF EXISTS ill;
DROP TABLE IF EXISTS country_codes;
DROP TABLE IF EXISTS region_codes;
DROP TABLE IF EXISTS district_codes;
DROP TABLE IF EXISTS infectivity;



CREATE TABLE ill(
	id INTEGER,
    date_of_infection DATE NOT NULL,
    age SMALLINT NOT NULL,
    gender CHAR(1) NOT NULL,
    region_code VARCHAR(10) NOT NULL,
    district_code VARCHAR(10) NOT NULL,
    imported BOOL NOT NULL,
    country_code VARCHAR(2) NULL ### can be null if not imported
);

### kraj
CREATE TABLE region_codes(
	region_code VARCHAR(10) NOT NULL,
    region_name VARCHAR(50) NOT NULL
);

### okres (spadá pod kraj)
CREATE TABLE district_codes(
	district_code VARCHAR(10) NOT NULL,
    district_name VARCHAR(50) NOT NULL,
    region_code VARCHAR(10) NOT NULL
);

CREATE TABLE country_codes(
	country_code VARCHAR(2) NOT NULL,
    country_name VARCHAR(100) NOT NULL
);

CREATE TABLE infectivity(
	id INTEGER NOT NULL AUTO_INCREMENT,
    region_code VARCHAR(10) NOT NULL,
    district_code VARCHAR(10) NOT NULL,
    num_of_ill INTEGER NOT NULL
);

CREATE TABLE country_rates(
	id INTEGER NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    new_cases INTEGER NOT NULL,
    tests_done INTEGER NOT NULL,
    population INTEGER NOT NULL,
    testing_rate FLOAT NOT NULL,
    positivity_rate FLOAT NOT NULL
);

### primary keys ###
ALTER TABLE ill ADD constraint PK_ill PRIMARY KEY (id);
ALTER TABLE region_codes ADD constraint PK_region_code PRIMARY KEY (region_code);
ALTER TABLE district_codes ADD constraint PK_district_code PRIMARY KEY (district_code);
ALTER TABLE country_codes ADD constraint PK_country_code PRIMARY KEY (country_code);
ALTER TABLE infectivity ADD constraint PK_infectivity PRIMARY KEY (id);
ALTER TABLE country_rates ADD constraint PK_country_rates PRIMARY KEY (id);
####################

### foreign keys ###
# ill foreign keys
ALTER TABLE ill ADD CONSTRAINT FK_ill_in_region FOREIGN KEY (region_code) REFERENCES region_codes(region_code);
ALTER TABLE ill ADD CONSTRAINT FK_ill_in_district FOREIGN KEY (district_code) REFERENCES district_codes(district_code);
ALTER TABLE ill ADD CONSTRAINT FK_import_country FOREIGN KEY (country_code) REFERENCES country_codes(country_code);

# country rates foreign keys
ALTER TABLE country_rates ADD CONSTRAINT FK_country_name FOREIGN KEY (country_code) REFERENCES country_codes(country_code);

# district foreign keys
ALTER TABLE district_codes ADD CONSTRAINT FK_district_belongs_to_region FOREIGN KEY (region_code) REFERENCES region_codes(region_code);

# infectivity foreign keys
ALTER TABLE infectivity ADD CONSTRAINT FK_infectivity_in_region FOREIGN KEY (region_code) REFERENCES region_codes(region_code);
ALTER TABLE infectivity ADD CONSTRAINT FK_infectivity_in_district FOREIGN KEY (district_code) REFERENCES district_codes(district_code);
####################