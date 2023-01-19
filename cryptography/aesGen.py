import os
from Crypto.Random import get_random_bytes

key = get_random_bytes(16) # random key with 16 bytes
iv = get_random_bytes(16) # random iv with 16 bytes

print("Key: ", key.hex()) 
print("IV: ", iv.hex()) 