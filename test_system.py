import unittest
import auth

class TestSecurityModule(unittest.TestCase):
    """
    Test suite for the Global Insurance system's security and authentication logic.
    """

    def test_password_hashing_and_verification(self):
        """
        Tests that passwords are securely hashed and cannot be read as plain text,
        and verifies that the validation logic correctly accepts/rejects passwords.
        """
        plain_text_password = "SuperSecretPassword123!"
        
        # 1. Test Hashing
        hashed_pw = auth.hash_password(plain_text_password)
        
        # Ensure the hash does NOT equal the plain text
        self.assertNotEqual(plain_text_password.encode('utf-8'), hashed_pw, "Hash should not match plain text!")
        self.assertTrue(len(hashed_pw) > 0, "Hashed password should not be empty.")

        # 2. Test Successful Verification
        is_valid = auth.verify_password(plain_text_password, hashed_pw)
        self.assertTrue(is_valid, "System failed to verify the correct password.")

        # 3. Test Failed Verification
        is_invalid = auth.verify_password("WrongPassword456", hashed_pw)
        self.assertFalse(is_invalid, "System incorrectly verified a wrong password.")

if __name__ == '__main__':
    # This runs the tests when the script is executed
    unittest.main(verbosity=2)