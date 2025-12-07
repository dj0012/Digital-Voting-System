# Setup Guide for Secure Digital Voting Platform

## Prerequisites
This project requires:
1. **MySQL Server** (version 5.7 or higher)
2. **Python 3.7+**
3. **mysql-connector-python** package

## Installation Steps

### 1. Install MySQL Server

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install mysql-server
```

#### On macOS (using Homebrew):
```bash
brew install mysql
```

#### On Windows:
Download and install from: https://dev.mysql.com/downloads/mysql/

### 2. Start MySQL Server

#### On Ubuntu/Debian:
```bash
sudo service mysql start
```

#### On macOS:
```bash
brew services start mysql
```

#### On Windows:
MySQL typically starts automatically after installation.

### 3. Create the Database and Tables

Connect to MySQL and run the SQL files in order:

```bash
mysql -u root -p
```

Then in the MySQL prompt, execute:
```sql
SOURCE /path/to/Voting\ tables.sql
SOURCE /path/to/vote\ tables.sql
SOURCE /path/to/Insert\ Statements.sql
```

Or from terminal:
```bash
mysql -u root -p voting_system < "Voting tables.sql"
mysql -u root -p voting_system < "vote tables.sql"
mysql -u root -p voting_system < "Insert Statements.sql"
```

### 4. Configure Database Credentials

Edit `final.py` and update the database connection parameters:

```python
self.db = connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',  # Change to your MySQL username
    password='****',  # Change to your MySQL password
    database='voting_system'
)
```

### 5. Install Python Dependencies

```bash
pip install mysql-connector-python
```

### 6. Run the Application

```bash
python final.py
```

## Database Schema

The application uses the following tables:
- **voter_table**: Stores voter information
- **user_table**: Stores login credentials
- **party_table**: Stores party information
- **candidate_table**: Stores candidate details
- **vote_table**: Stores voting records
- **address**: Stores address information
- **Result**: View for vote aggregation

## Features

- **Sign Up**: Register as a voter
- **Login**: Authenticate with Voter ID and credentials
- **Vote**: Cast a vote for a candidate
- **Party Registration**: Register a new political party
- **Candidate Management**: Add/remove candidates (for party leaders)
- **View Results**: See current voting rankings
- **Update Profile**: Modify personal details

## Important Notes

1. **Security Warning**: The current implementation uses SQL string formatting which is vulnerable to SQL injection. For production use, always use parameterized queries.

2. **Password Storage**: Passwords are stored in plain text. For production, use proper hashing (bcrypt, argon2, etc.)

3. **Database Credentials**: The hardcoded password in the code should be externalized to environment variables or a config file.

## Troubleshooting

### "Can't connect to MySQL server" Error
- Ensure MySQL server is running
- Check host, port, username, and password are correct
- Verify the `voting_system` database exists

### "Access denied for user 'root'" Error
- Check your MySQL username and password
- Update credentials in `final.py`

### "Table 'voting_system.xyz' doesn't exist" Error
- Ensure all SQL files have been executed
- Check that you're connected to the `voting_system` database
