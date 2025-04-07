# yfc
Your family calendar

This is a simple app to track events and recurring events for multiple individuals. It runs just fine on a Raspberry Pi.  Stop wasting your compute trying to figure out how to give your data to GOOG/AAPL (aka, the headache of setting up shared calendars)! 

## Installation

Database operations are manually performed.

First, set up the schemas:
```
CREATE DATABASE yfd;
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
CREATE USER yfd_user WITH ENCRYPTED PASSWORD 'badpassword';
GRANT USAGE, SELECT, UPDATE ON SEQUENCE events_id_seq TO yfd_user;
GRANT ALL PRIVILEGES ON TABLE recurring_events TO yfd_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE recurring_events_id_seq TO yfd_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO yfd_user;
# Rinse/repeat for everyone else in the Doe family
INSERT INTO family_members (name, email) VALUES ('John Doe', 'john.doe@example.com');
```

Clone the Git repo and install the requirements:
```
git clone git@github.com:reptation/yfc.git
cd yfc
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Create a .env file in the `src` folder with appropriate local values (note: don't do this in production)
```
export DB_HOST='localhost'
export DB_NAME='wfd'
export DB_USER='wfd_user'
export DB_PASS='badpassword'
```

Finally, start the app in HA (/s)
```
source ./venv/bin/activate
nohup python src/main.py &
```
