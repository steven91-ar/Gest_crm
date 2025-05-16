from pathlib import Path
import re
import string
from tinydb import TinyDB, where, table
from typing import List




class User:
    DB = TinyDB (Path(__file__).resolve().parent / "db.json", indent=4)

    def __init__(self, first_name: str, last_name: str, phone_number: str = "", address: str = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self) -> str:
        return f"User({self.first_name}, {self.last_name})"

    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"


    def _check_phone_number(self):
        phone_number = re.sub(r"[+\s()]", "", self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f"Numéro de téléphone invalide : {self.phone_number}")

    def _check_names(self):
        if not self.first_name or not self.last_name:
            raise ValueError("Le prénom et le nom ne peuvent pas être vides.")
        special_chars = string.punctuation + string.digits
        for char in self.first_name + self.last_name:
            if char in special_chars:
                raise ValueError(f"Nom invalide : {self.full_name}")

    def checks(self):
        self._check_phone_number()
        self._check_names()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def db_instance(self) -> table.Document:
        return User.DB.get(
            (where("first_name") == self.first_name) &
            (where("last_name") == self.last_name)
        )
        
    def exists(self):
        return bool(self.db_instance)
    def delete(self) -> List[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []
    
    def save (self, validate_data: bool = False) -> int:
        if validate_data:
            self.checks()
        if self.exists():
            return -1
        else:
            return User.DB.insert(self.__dict__)
    
def get_all_users():
     return [User(**user) for user in User.DB.all()]

# Exécution principale
if __name__ == "__main__":
   camille = User("Camille", "Pereira")
   for i in camille.delete():
       print(i)