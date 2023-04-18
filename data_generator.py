from utils import Person, timer
import pandas as pd
import random
import hashlib
from typing import Dict

person_dict = {}

def generate_random_dataframe(num_rows: int) -> pd.DataFrame:
    global person_dict
    data = []

    # Generate a random person object to get an idea of the attributes
    
    disposable_person = Person.generate_random_person()
    hash_object = hashlib.sha256(f"{disposable_person.first_name}{disposable_person.last_name}{disposable_person.date_of_birth}".encode())
    hash_key = hash_object.hexdigest()
    person_dict[hash_key] = disposable_person

    # Columns to include in the dataframe
    attributes = [attr for attr in dir(disposable_person) if not callable(getattr(disposable_person, attr)) and not attr.startswith("_")]
    num_attributes = random.randint(1, len(attributes))
    selected_attributes = random.sample(attributes, num_attributes)
    
    # Rows to include in the dataframe
    for i in range(num_rows):
        if random.random() < 0.05:
          empty_data = {attr: [] for attr in selected_attributes}
          return pd.DataFrame(empty_data, columns=selected_attributes)
        elif random.random() < 0.5 and len(person_dict) > 0:
            # Retrieve a person object from the dict
            hash_key = random.choice(list(person_dict.keys()))
            person = person_dict[hash_key]
        else:
            # Generate a new person object
            person = Person.generate_random_person()
            # Store the new person object in the dict
            hash_object = hashlib.sha256(f"{person.first_name}{person.last_name}{person.date_of_birth}".encode())
            hash_key = hash_object.hexdigest()
            person_dict[hash_key] = person
        
        row_data = {'first_name': person.first_name, 'last_name': person.last_name}
        for attribute in selected_attributes:
            row_data[attribute] = getattr(person, attribute)
        data.append(row_data)

        df = pd.DataFrame(data)
        if random.random() < 0.3:
            df = add_blank_rows(df)
        
    return df

@timer
def generate_nested_dict(num_collections: int) -> Dict[str, Dict[str, pd.DataFrame]]:
    nested_dict = {}
    for i in range(num_collections):
        collection_id = f"{random.getrandbits(128):032x}"
        num_documents = random.randint(1, 20)
        document_dict = {}
        for j in range(num_documents):
            document_id = f"{random.getrandbits(128):032x}"
            document_dict[document_id] = generate_random_dataframe(random.randint(1, 100))
        nested_dict[collection_id] = document_dict
    return nested_dict

def add_blank_rows(df):
    # Add col names as top row
    col_names = df.columns
    new_data = [col_names.tolist()] + df.values.tolist()
    df = pd.DataFrame(new_data, columns=col_names)
    # Blank out the column names
    df.columns = ['' for col in df.columns]

    num_blanks = random.randint(1,5)
    # Create a DataFrame with random number of blank rows
    blank_rows = pd.DataFrame(index=range(num_blanks), columns=df.columns)
    
    # Concatenate the blank rows DataFrame with the input DataFrame
    df = pd.concat([blank_rows, df]).reset_index(drop=True)
    return df