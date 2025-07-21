CREATE TABLE jobs (
	hash VARCHAR(300) PRIMARY KEY,
	title VARCHAR(255),
	company VARCHAR(255),
	url TEXT,
	description TEXT,
	description_extracted TEXT,
    timestamp TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE resumes (
    id INT PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    last_updated TIMESTAMP,
);

CREATE TABLE scores (
    resume_id INT,
    job_hash VARCHAR(300),
    score double precision,
    FOREIGN KEY (resume_id) REFERENCES resumes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (job_hash) REFERENCES jobs(hash)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

