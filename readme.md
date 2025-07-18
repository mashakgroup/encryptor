##Key Features:

-Generates random encryption codes between 20-30 digits
-Uses multiple layers of randomization (system entropy, timestamps, SHA256 hashing)
-Military-grade AES encryption via Fernet
-Stores all data in encrypted_data.json
-Clean, simple interface

##Randomization Sources:

-secrets module for cryptographically secure randomness
-System entropy via os.urandom()
-Microsecond timestamps
-SHA256 hashing with random positioning
-Character scrambling with 50% probability per character

##Installation:
bash pip install cryptography
##Usage:
Just run python main.py and you'll get a clean menu to encrypt/decrypt data. Each encryption generates a unique 20-30 character code that's practically impossible to guess.
The test function will show you how randomized the codes are - each time you encrypt the same data, you'll get completely different codes!
