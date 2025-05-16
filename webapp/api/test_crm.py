from tinydb.table import Document
from crm import User
import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage


@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)

@pytest.fixture
def user(setup_db):
    u = User(
        first_name="Patrick",
        last_name="Martin",
        phone_number="0123456789",
        address="1 rue du Chemin, 75000 Paris"

    )
    u.save()
    return u


def test_first_name(user):
    assert user.first_name == "Patrick"

def test_full_name(user):
    assert user.full_name == "Patrick Martin"

def test_check_phone_number_invalid(setup_db):
    user_bad = User("Jean",
                    "Dupont",
                    phone_number="ABCD",
                    address="Paris")

    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()
    assert "invalide" in str(err.value)

def test_check_phone_number_valid(setup_db):
    assert False

def test_check_names_empty(setup_db):
    user_bad = User("", "", phone_number="0123456789", address="Paris")
    with pytest.raises(ValueError) as err:
        user_bad._check_names()
    assert "ne peuvent pas être vides" in str(err.value)

def test_check_names_invalid_characters(setup_db):
    user_bad = User("Jean$", "Dup@nt", phone_number="0123456789", address="Paris")
    with pytest.raises(ValueError) as err:
        user_bad._check_names()
    assert "Nom invalide" in str(err.value)



def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance["first_name"] == "Patrick"
    assert user.db_instance["last_name"] == "Martin"
    assert user.db_instance["address"] == "1 rue du Chemin, 75000 Paris"
    assert user.db_instance["phone_number"] == "0123456789"

def test_db_instance_not_found(setup_db):
    user = User("Alice", "Durand", "0612345678", "Paris")
    assert user.db_instance is None

def test_exists():
    assert False

def test_not_exists(setup_db):
    u = User("Jean", "Dupont", "0123456789", "Paris")
    assert u.exists() is False

def test_delete(setup_db):
    user = User("Alice", "Dupont", phone_number="0123456789", address="Lyon")
    user.save()

    first = user.delete()
    second = user.delete()

    assert isinstance(first, list)
    assert isinstance(second, list)
    assert len(first) > 0
    assert len(second) == 0


def test_save(setup_db):
    user1 = User("John", "Smith", phone_number="0123456789", address="Paris")
    user2 = User("John", "Smith", phone_number="0123456789", address="Paris")

    first = user1.save()
    second = user2.save()

    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1
