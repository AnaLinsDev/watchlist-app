import pytest
from unittest.mock import MagicMock

# This is a special pytest file
# Everything here becomes globally available to all tests
# (no imports needed)


@pytest.fixture
def db_mock():
    db = MagicMock()

    # Simulates: db.query(...).filter(...).first()
    db.query.return_value.filter.return_value.first.return_value = None

    return db
