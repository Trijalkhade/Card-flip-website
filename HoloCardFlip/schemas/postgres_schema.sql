-- PostgreSQL schema (simplified)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE members (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  bio TEXT,
  profile_picture TEXT
);

CREATE TABLE achievements (
  id SERIAL PRIMARY KEY,
  member_id INTEGER REFERENCES members(id),
  title TEXT,
  description TEXT,
  date_awarded DATE
);

CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  title TEXT,
  description TEXT,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  seats INTEGER DEFAULT 0
);
