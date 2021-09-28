"""Dummy class to generate dummy data."""
from random import SystemRandom

import pytz
from faker import Faker


class RBIDummy:
    """Create dummy RBI data."""

    def __init__(self):
        """Initialize class variables."""
        self.crypto_gen = SystemRandom()
        self.fake = Faker(["en_PH"])

    def create_rbi(self):
        """Create RBI dummy data."""
        house_num = self.crypto_gen.randrange(100000, 999999)
        address = self.fake.address()
        date = self.fake.date()
        last_name = self.fake.last_name()
        created_at = self.fake.iso8601(tzinfo=pytz.timezone("Asia/Manila"))

        family_dictionary = {}
        for idx in range(0, self.crypto_gen.randint(1, 10)):
            first_name = self.fake.first_name()
            middle_name = self.fake.last_name()
            ext = self.fake.suffix()
            birth_place = self.fake.city()
            birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=60).strftime(
                "%B %d, %Y"
            )
            sex = self.crypto_gen.choice(["M", "F"])
            civil_status = self.crypto_gen.choice(
                [
                    "Single",
                    "Married",
                    "Divorced",
                    "Widowed",
                    "Separated",
                ]
            )
            citizenship = self.crypto_gen.choice(["Filipino", "Foreigner"])
            monthly_income = f"{self.crypto_gen.randrange(10000, 1000000):,}"

            if idx == 0:
                remarks = "Father"
            elif idx == 1:
                remarks = "Mother"
            else:
                remarks = self.crypto_gen.choice(["Daughter", "Son"])

            family_dictionary[first_name] = {
                "last_name": last_name,
                "first_name": first_name,
                "middle_name": middle_name,
                "ext": ext,
                "birth_place": birth_place,
                "birth_date": birth_date,
                "sex": sex,
                "civil_status": civil_status,
                "citizenship": citizenship,
                "monthly_income": monthly_income,
                "remarks": remarks,
            }

        return {
            "house_num": house_num,
            "created_at": created_at,
            "address": address,
            "date_accomplished": date,
            "family_members": family_dictionary,
        }
