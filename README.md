# yfa
Your family app

# db
Setup Postgres

```
CREATE DATABASE yfd;

\c yfd

CREATE TABLE family_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    member_id INT REFERENCES family_members(id),
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME,
    description TEXT
);

CREATE TABLE recurring_events (
    id SERIAL PRIMARY KEY,
    member_id INT REFERENCES family_members(id),
    event_name VARCHAR(255) NOT NULL,
    event_time TIME NOT NULL,
    description TEXT,
    day_of_week VARCHAR(10) NOT NULL -- E.g., 'Monday', 'Tuesday'
);

CREATE USER yfd_user WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE yfd TO yfd_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO yfd_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO yfd_user;

GRANT ALL PRIVILEGES ON TABLE recurring_events TO yfd_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE recurring_events_id_seq TO yfd_user;
```


