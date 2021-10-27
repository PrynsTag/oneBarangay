"""Generate fake user and rbi."""
import csv
import getopt
import json
import os
import sys
from datetime import date, datetime
from random import SystemRandom

import pytz
import requests
from dotenv import load_dotenv
from faker import Faker
from firebase_admin import auth, firestore
from firebase_admin._auth_utils import EmailAlreadyExistsError

from one_barangay.local_settings import logger
from one_barangay.settings import firebase_app

load_dotenv()


def main():
    """Run script."""
    argv = sys.argv[1:]

    try:
        # Define the getopt parameters
        opts, args = getopt.getopt(argv, "n:", ["num_email"])
        # Check if the options' length is 1 (can be enhanced)
        if len(opts) == 0 and len(opts) > 1:
            logger("usage: generate_emails.py -n <first_operand>")
        else:
            _, num_emails = opts[0]

            for _ in range(int(num_emails)):
                family_data = create_dummy_rbi()
                logger(json.dumps(family_data, indent=4, sort_keys=True, default=str))
                save_rbi(family_data, family_data["house_num"])

    except getopt.GetoptError:
        # Print something useful
        logger("usage: generate_emails.py -n <first_operand>")
        sys.exit(2)


def delete_all_account():
    """Delete all accounts in firestore auth."""
    for user in auth.list_users(app=firebase_app).iterate_all():
        logger("Deleting user " + user.uid)
        auth.delete_user(user.uid, app=firebase_app)


def create_dummy_rbi():
    """Create dummy rbi."""
    fake = Faker(["fil_PH"])
    crypto_gen = SystemRandom()

    house_num = str(crypto_gen.randrange(100000, 999999))
    address = fake.address()
    street = crypto_gen.choice(STREET_CHOICES)
    date_accomplished = datetime.combine(fake.date_between(start_date="-2y"), datetime.min.time())
    last_name = fake.last_name()
    created_at = datetime.now(tz=pytz.timezone("Asia/Manila"))

    db = firestore.client(app=firebase_app)
    family_dictionary = {}
    user_list = []
    for idx in range(0, crypto_gen.randint(1, 5)):
        first_name = fake.first_name()
        middle_name = fake.last_name()
        ext = fake.suffix()
        birth_place = fake.city()
        birth_date = fake.date_of_birth(minimum_age=15, maximum_age=60).strftime("%B %d, %Y")
        today = date.today()
        birth_date_dt = datetime.strptime(birth_date, "%B %d, %Y")
        age = (
            today.year
            - birth_date_dt.year
            - ((today.month, today.day) < (birth_date_dt.month, birth_date_dt.day))
        )
        civil_status = crypto_gen.choice(
            [
                "Single",
                "Married",
                "Divorced",
                "Widowed",
                "Separated",
            ]
        )
        citizenship = crypto_gen.choice(["Filipino", "Foreigner"])
        if age > 20:
            monthly_income = f"{crypto_gen.randrange(1000, 50000):,}"
        else:
            monthly_income = f"{0:,}"

        if idx == 0:
            remarks = "Father"
            sex = "M"
        elif idx == 1:
            remarks = "Mother"
            sex = "F"
        else:
            sex = crypto_gen.choice(["M", "F"])
            remarks = crypto_gen.choice(["Daughter", "Son"])

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

        auth_data = create_dummy_user(first_name, last_name)
        # Merge family_member data with auth_data.
        family_dictionary[first_name].update(auth_data)
        # Add RBI info to user
        rbi_info = {"house_num": house_num, "address": address, "street": street}
        save_users_collection(family_dictionary[first_name] | rbi_info, auth_data["uid"])
        user_list.append(auth_data["uid"])

    family_chunk = {}
    for family_member, index in zip(
        family_dictionary.items(), range(len(family_dictionary.keys()))
    ):
        chunk = {"uid": user_list[index]}
        key, _ = family_member
        for field, val in family_dictionary[key].items():
            if field in ["first_name", "last_name", "birth_date"]:
                chunk[field] = val

        family_chunk[key] = chunk

    for _, user in enumerate(user_list):
        doc_ref = db.collection("users").document(user).collection("family").document(house_num)
        doc_ref.set(family_chunk, merge=True)

    return {
        "house_num": house_num,
        "created_at": created_at,
        "address": address,
        "date_accomplished": date_accomplished,
        "street": street,
        "family_members": family_dictionary,
    }


def save_rbi(family_data, house_num):
    """Save rbi to firestore rbi collection.

    Args:
      family_data: The family to save in rbi.
      house_num: The house number of family.

    Returns:
      None.
    """
    db = firestore.client(app=firebase_app)
    doc_ref = db.collection("rbi").document(house_num)
    family_data["house_num"] = house_num
    doc_ref.set(family_data)


def save_users_collection(user_data, uid):
    """Save user in firestore users collection.

    Args:
      user_data: The user data to save.
      uid: The unique I.D. of user.

    Returns:
      The unique I.D. of the user.
    """
    db = firestore.client(app=firebase_app)
    doc_ref = db.collection("users").document(uid)
    user_data["uid"] = uid
    doc_ref.set(user_data)

    return doc_ref.id


def create_dummy_user(first_name, last_name):
    """Create dummy user.

    Args:
      first_name: The name of the user to create.
      last_name: The last name of the user to create.

    Returns:
      The dictionary containing the user information.
    """
    fake = Faker(["fil_PH"])
    crypto_gen = SystemRandom()

    # Auth
    name_lower = first_name.lower()
    email = f"c5zzk.{name_lower}@inbox.testmail.app"
    password = f"{name_lower}123"
    display_name = f"{first_name} {last_name}"
    role = crypto_gen.choice(["resident", "admin", "secretary", "worker"])
    photo_url = f"https://i.pravatar.cc/150?img={crypto_gen.randint(1, 70)}"
    phone_number = fake.mobile_number().replace("-", "")
    formatted_phone_number = (
        phone_number.replace("0", "+63", 1) if phone_number.startswith("0") else phone_number
    )

    auth_data = {
        "email": email,
        "display_name": display_name,
        "photo_url": photo_url,
        "password": password,
        "disabled": False,
        "email_verified": True,
        "phone_number": formatted_phone_number,
        "app": firebase_app,
    }

    try:
        user_record = auth.create_user(**auth_data)
    except EmailAlreadyExistsError:
        # Generate new email with number appended.
        name = first_name + str(crypto_gen.randint(0, 99))
        email = f"c5zzk.{name.lower()}@inbox.testmail.app"
        auth_data["email"] = email

        user_record = auth.create_user(**auth_data)

    auth.set_custom_user_claims(user_record.uid, {role: True}, app=firebase_app)

    with open("emails.csv", mode="a", encoding="UTF-8") as email_file:
        email_writer = csv.writer(email_file, delimiter=",")
        email_writer.writerow([f"{email}", f"{password}", f"{role}"])

    return {
        "uid": user_record.uid,
        "display_name": user_record.display_name,
        "email": user_record.email,
        "role": role,
        "provider": user_record.provider_id,
        "creation_date": user_record.user_metadata.creation_timestamp,
        "last_sign_in": user_record.user_metadata.last_sign_in_timestamp,
        "email_verified": user_record.email_verified,
        "disabled": user_record.disabled,
        "phone_number": user_record.phone_number,
        "photo_url": user_record.photo_url,
    }


def firebase_register(email, password):
    """Register user using Firebase Auth REST API.

    Args:
      email: The email to register.
      password: The email to register.

    Returns:
      None.
    """
    headers = {"Content-type": "content_type_value"}
    dict_data = json.dumps({"email": email, "password": password, "returnSecureToken": False})
    json_data = json.loads(dict_data)
    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:signUp?key={os.getenv('FIREBASE_WEB_API_KEY')}"
    )
    status = requests.post(url, json=json_data, headers=headers)

    if status.status_code == 200:
        logger(status.text)
    else:
        logger("error", status.text)


STREET_CHOICES = [
    "A. Duque",
    "Aca Road",
    "Bangcal Extension",
    "Bartolome Street",
    "C. Molina Street",
    "Central Road",
    "Cherry Blossom Street",
    "Dr. Bartolome",
    "East Road",
    "F. San Diego Street",
    "I. Fernando",
    "I. Lozada Street",
    "Jollibee Drive-Through",
    "M.H. del Pilar Footbridge (footway)",
    "Main Road",
    "North Road",
    "Orange Street",
    "P. Adriano",
    "Peach Street",
    "Road 1",
    "Roseville Street",
    "South RoadSt. Elsewhere Street",
    "T. Santiago Street",
    "West Road",
]


if __name__ == "__main__":
    main()
