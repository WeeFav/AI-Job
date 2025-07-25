CREATE TABLE jobs (
	hash VARCHAR(300) PRIMARY KEY,
	title VARCHAR(255),
	company VARCHAR(255),
	url TEXT,
	description TEXT,
	description_extracted TEXT,
    timestamp TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE skills (
    job_hash VARCHAR(300),
    skills JSONB,
    educations TEXT[],
    majors TEXT[],
    embedding vector(384),
    FOREIGN KEY (job_hash) REFERENCES jobs(hash)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

