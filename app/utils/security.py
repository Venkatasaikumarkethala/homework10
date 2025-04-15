# app/security.py
import bcrypt
from builtins import Exception, ValueError, bool, int, str
from logging import getLogger

# Set up logging
logger = getLogger(__name__)
 
def hash_password(password: str, rounds: int = 12) -> str:
     """
     Hashes a password using bcrypt with a specified cost factor.
     
     Args:
         password (str): The plain text password to hash.
         rounds (int): The cost factor that determines the computational cost of hashing.
     Returns:
         str: The hashed password.
     Raises:
         ValueError: If hashing the password fails.
     """
     try:
         salt = bcrypt.gensalt(rounds=rounds)
         hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
         return hashed_password.decode('utf-8')
     except Exception as e:
         logger.error("Failed to hash password: %s", e)
         raise ValueError("Failed to hash password") from e
     
def verify_password(plain_password: str, hashed_password: str) -> bool:
     
     try:
         return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
     except Exception as e:
         logger.error("Error verifying password: %s", e)
         raise ValueError("Authentication process encountered an unexpected error") from e
     