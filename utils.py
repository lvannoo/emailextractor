import functools
import random
import time


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Function {func.__name__} took {end_time - start_time:.2f} seconds to run")
        return result
    return wrapper


class Person:
    __FIRST_NAMES = {
        'male': ['William', 'Liam', 'James', 'Oliver', 'Benjamin', 'Elijah', 'Lucas', 'Mason', 'Logan', 'Alexander',
                 'Ethan', 'Michael', 'Daniel', 'Henry', 'Jackson', 'Sebastian', 'Aiden', 'Matthew', 'Samuel', 'David',
                 'Joseph', 'Carter', 'Owen', 'Wyatt', 'John', 'Luke', 'Gabriel', 'Nicholas', 'Nathan', 'Ryan',
                 'Anthony', 'Christian', 'Jaxon', 'Ezra', 'Isaac', 'Jesse', 'Elliott', 'Levi', 'Josiah', 'Maxwell',
                 'Caleb', 'Aaron', 'Adam', 'Isaiah', 'Julian', 'Andrew', 'Asher', 'Leo', 'Dominic', 'Ian'],
        'female': ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Charlotte', 'Mia', 'Amelia', 'Harper', 'Evelyn',
                   'Abigail', 'Emily', 'Elizabeth', 'Mila', 'Ella', 'Avery', 'Sofia', 'Camila', 'Aria', 'Scarlett',
                   'Victoria', 'Madison', 'Luna', 'Grace', 'Chloe', 'Penelope', 'Layla', 'Riley', 'Zoey', 'Nora',
                   'Lily', 'Eleanor', 'Hannah', 'Lillian', 'Addison', 'Aubrey', 'Ellie', 'Stella', 'Natalie',
                   'Zoe', 'Leah', 'Savannah', 'Audrey', 'Brooklyn', 'Maya', 'Claire', 'Lucy', 'Skylar']
    }
    __LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Perez', 'Gomez', 'Martin', 'Lee', 'Allen', 'Young', 'Wright', 'Walker', 'White', 'Hall', 'Lewis', 'Scott', 'Green', 'Adams', 'Baker', 'Nelson', 'Carter', 'Mitchell', 'Parker', 'King', 'Collins', 'Cooper', 'Reed', 'Bailey', 'Bell', 'Murphy', 'Rivera', 'Cook', 'Rogers', 'Phillips', 'Turner', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Stewart', 'Flores']
    __COMPANY_NAMES = ['Apple', 'Microsoft', 'Amazon', 'Google', 'Facebook', 'Tesla', 'Netflix', 'Uber', 'Airbnb', 'IBM']

    def __init__(self, first_name=None, last_name=None, date_of_birth=None, gender=None, email = None, email2 = None, mobile_phone = None, passport = None):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email_address = email
        self.email_address2 = email2
        self.phone_number = mobile_phone
        self.passport = passport


    @classmethod
    def generate_random_person(cls):
        gender = random.choice(['male', 'female'])
        first_name = random.choice(cls.__FIRST_NAMES[gender])
        last_name = random.choice(cls.__LAST_NAMES)
        date_of_birth = f"{random.randint(1, 12)}/{random.randint(1, 28)}/{random.randint(1950, 2005)}"
        email_address = f"{first_name.lower()}.{last_name.lower()}@test.com"
        email_address2 = f"{first_name.lower()}.{last_name.lower()[0]}@{random.choice(cls.__COMPANY_NAMES)}.com"
        mobile_phone = f"+44{random.randint(1000, 9999)}{random.randint(100, 999)}{random.randint(100, 999)}"
        passport = f"{random.choice(['A','B','C','D'])}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
        return cls(first_name, last_name, date_of_birth, gender, email_address, email_address2, mobile_phone, passport)
    