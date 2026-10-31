"""
sessions
"""

from yoyo import step

__depends__ = {'dwarf_qm_20261008_01_Sw988-users'}

steps = [
    step(
        """
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    token VARCHAR(255) NOT NULL,
    user_agent VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
        """,
        "DROP TABLE sessions;"
    ),

    step(
        "CREATE INDEX idx_sessions_token ON sessions (token);",
        "DROP INDEX idx_sessions_token;"
    )
]
