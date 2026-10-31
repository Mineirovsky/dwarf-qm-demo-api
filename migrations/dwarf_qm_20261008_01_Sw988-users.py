"""
users
"""

from yoyo import step
import bcrypt

DEFAULT_USERNAME = "super.user"
DEFAULT_PASSWORD = bcrypt.hashpw("admin".encode(), bcrypt.gensalt()).decode()

__depends__ = {}

steps = [
    step(
        """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
        """,
        "DROP TABLE users;"
    ),

    step(
        """
CREATE OR REPLACE FUNCTION update_users_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_users_updated_at_column();
        """,
        """
DROP TRIGGER IF EXISTS trigger_users_updated_at ON users;
DROP FUNCTION IF EXISTS update_users_updated_at_column;
        """
    ),

    step(
        f"INSERT INTO users (username, name, email, password) VALUES ('{DEFAULT_USERNAME}', 'Super User', 'super.user@example.com', '{DEFAULT_PASSWORD}');",
        "DELETE FROM users WHERE username = '{DEFAULT_USERNAME}';"
    )
]
