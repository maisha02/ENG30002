import pickle
from pathlib import Path  # Importing Path from pathlib
import streamlit_authenticator as stauth

houses = ["HouseA","HouseB","HouseC","HouseD"]
usernames = ["Dev","jhilam","Jordan","Ryan"]
passwords = ["dev123","jhilam123","jordan123","ryan123"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pk1"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)


