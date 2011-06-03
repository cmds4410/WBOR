#!/usr/bin/env python
# Author: Harrison Chapman

from hashlib import sha256
from hmac import HMAC
import random

# Gleefully stolen from a StackOverflow post
# http://stackoverflow.com/questions/287517/encrypting-hashing-plain-text-passwords-in-database
def random_bytes(num_bytes):
  return "".join(chr(random.randrange(256)) for i in xrange(num_bytes))

def pbkdf_sha256(password, salt, iterations):
  result = password
  for i in xrange(iterations):
    result = HMAC(result, salt, sha256).digest() # use HMAC to apply the salt
  return result

NUM_ITERATIONS = 1732
def hash_password(plain_password):
  salt = random_bytes(8) # 64 bits

  hashed_password = pbkdf_sha256(plain_password, salt, NUM_ITERATIONS)

  # return the salt and hashed password, encoded in base64 and split with ","
  return salt.encode("base64").strip() + "," + hashed_password.encode("base64").strip()

def check_password(saved_password_entry, plain_password):
  salt, hashed_password = saved_password_entry.split(",")
  salt = salt.decode("base64")
  hashed_password = hashed_password.decode("base64")

  return hashed_password == pbkdf_sha256(plain_password, salt, NUM_ITERATIONS)
