CREATE TABLE jobs (
	hash VARCHAR(300) UNIQUE,
	title VARCHAR(255),
	company VARCHAR(255),
	url TEXT,
	description TEXT,
	description_extracted TEXT,
    timestamp TIMESTAMP DEFAULT current_timestamp
);