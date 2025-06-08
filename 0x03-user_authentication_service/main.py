#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@me.com'
password = 'mySuperPwd'
auth = Auth()

auth.register_user(email, password)

session_id = auth.create_session(email)
print(session_id)
user = auth.get_user_from_session_id(session_id="sakfdjkajflkdsjalkdjflksdfj")
print(user)
