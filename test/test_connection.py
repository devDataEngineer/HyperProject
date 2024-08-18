import pytest

from src.extractlambda.connection import db_connection

def test_connection_to_DB_is_established():
    conn1=db_connection()
    result = conn1.run("Select * FROM design;")
    assert result 