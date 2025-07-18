import os
import json
import hashlib
import secrets
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SuperEncryptor:
    def __init__(self):
        self.storage_file = "encrypted_data.json"
        self.load_storage()
    
    def load_storage(self):
        """Load existing encrypted data or create new storage"""
        try:
            with open(self.storage_file, 'r') as f:
                self.storage = json.load(f)
        except FileNotFoundError:
            self.storage = {}
    
    def save_storage(self):
        """Save encrypted data to file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.storage, f, indent=2)
    
    def generate_random_code(self):
        """Generate ultra-random encryption code (20-30 digits)"""
        length = secrets.randbelow(11) + 20  # Random length between 20-30
        
        # Mix multiple randomization sources
        chars = string.digits + string.ascii_letters + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Generate base random string
        code = ''.join(secrets.choice(chars) for _ in range(length))
        
        # Add timestamp and system entropy for extra randomness
        import time
        timestamp = str(int(time.time() * 1000000))  # Microsecond timestamp
        system_random = os.urandom(8).hex()
        
        # Combine and hash for maximum randomization
        combined = code + timestamp + system_random
        final_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        # Take random portion of hash and add more randomness
        start_pos = secrets.randbelow(len(final_hash) - 25)
        random_code = final_hash[start_pos:start_pos + length]
        
        # Final scramble with more entropy
        scrambled = list(random_code)
        for i in range(len(scrambled)):
            if secrets.randbelow(2):  # 50% chance to modify each char
                scrambled[i] = secrets.choice(string.ascii_letters + string.digits)
        
        return ''.join(scrambled)
    
    def create_encryption_key(self, password, salt):
        """Create encryption key from password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_data(self, data, password=None):
        """Encrypt data and return encryption code"""
        if password is None:
            password = secrets.token_urlsafe(32)  # Generate random password
        
        # Generate random salt
        salt = os.urandom(16)
        
        # Create encryption key
        key = self.create_encryption_key(password, salt)
        fernet = Fernet(key)
        
        # Encrypt the data
        encrypted_data = fernet.encrypt(data.encode())
        
        # Generate random encryption code
        encryption_code = self.generate_random_code()
        
        # Store encrypted data with metadata
        self.storage[encryption_code] = {
            'encrypted_data': base64.b64encode(encrypted_data).decode(),
            'salt': base64.b64encode(salt).decode(),
            'password': password,
            'timestamp': str(int(time.time()))
        }
        
        self.save_storage()
        return encryption_code
    
    def decrypt_data(self, encryption_code):
        """Decrypt data using encryption code"""
        if encryption_code not in self.storage:
            return None
        
        try:
            stored_data = self.storage[encryption_code]
            
            # Reconstruct encryption key
            salt = base64.b64decode(stored_data['salt'])
            password = stored_data['password']
            key = self.create_encryption_key(password, salt)
            fernet = Fernet(key)
            
            # Decrypt data
            encrypted_data = base64.b64decode(stored_data['encrypted_data'])
            decrypted_data = fernet.decrypt(encrypted_data)
            
            return decrypted_data.decode()
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None
    
    def list_codes(self):
        """List all encryption codes"""
        return list(self.storage.keys())
    
    def delete_code(self, encryption_code):
        """Delete an encryption code and its data"""
        if encryption_code in self.storage:
            del self.storage[encryption_code]
            self.save_storage()
            return True
        return False

def main():
    encryptor = SuperEncryptor()
    
    print("🔐 SUPER POWERFUL ENCRYPTOR/DECRYPTOR 🔐")
    print("=" * 50)
    
    while True:
        print("\n1. Encrypt Data")
        print("2. Decrypt Data")
        print("3. List All Codes")
        print("4. Delete Code")
        print("5. Test with Sample Data")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            data = input("Enter data to encrypt: ")
            if data:
                code = encryptor.encrypt_data(data)
                print(f"\n✅ Data encrypted successfully!")
                print(f"🔑 Encryption Code: {code}")
                print(f"📏 Code Length: {len(code)} characters")
        
        elif choice == '2':
            code = input("Enter encryption code: ")
            if code:
                decrypted = encryptor.decrypt_data(code)
                if decrypted:
                    print(f"\n✅ Decrypted Data: {decrypted}")
                else:
                    print("\n❌ Invalid code or decryption failed!")
        
        elif choice == '3':
            codes = encryptor.list_codes()
            if codes:
                print(f"\n📋 Found {len(codes)} encryption codes:")
                for i, code in enumerate(codes, 1):
                    print(f"{i}. {code} ({len(code)} chars)")
            else:
                print("\n📋 No encryption codes found!")
        
        elif choice == '4':
            code = input("Enter code to delete: ")
            if encryptor.delete_code(code):
                print("\n✅ Code deleted successfully!")
            else:
                print("\n❌ Code not found!")
        
        elif choice == '5':
            print("\n🧪 Testing with sample data...")
            test_data = ["password123", "secret_message", "my_bank_account", "confidential_info"]
            
            for data in test_data:
                code = encryptor.encrypt_data(data)
                print(f"Data: '{data}' → Code: {code} ({len(code)} chars)")
                
                # Verify decryption
                decrypted = encryptor.decrypt_data(code)
                status = "✅" if decrypted == data else "❌"
                print(f"  Decryption test: {status}")
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    import time
    main()
