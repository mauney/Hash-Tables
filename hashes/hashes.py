import hashlib

key = b"str2"

for i in range(2):
    hashed = hashlib.sha256(key).hexdigest()
    print(hashed)

for i in range(2):
    hashed = hash(key)
    print(hashed)
    print(hashed % 8)
