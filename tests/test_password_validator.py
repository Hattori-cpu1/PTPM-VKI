import unittest
from src.password_validator import validate_password


class TestPasswordValidator(unittest.TestCase):

    def test_valid_latin_password(self):
        self.assertTrue(validate_password("SecurePass1!"))

    def test_valid_cyrillic_password(self):
        self.assertTrue(validate_password("ПарольТест9#"))

    def test_boundary_length_7(self):
        self.assertFalse(validate_password("Aa1!aaa"))

    def test_boundary_length_8(self):
        self.assertTrue(validate_password("Aa1!aaaa"))

    def test_boundary_length_20(self):

        self.assertTrue(validate_password("Aa1!aaaaaaaaaaaaaaaa"))

    def test_boundary_length_21(self):

        self.assertFalse(validate_password("Aa1!aaaaaaaaaaaaaaaaa"))

    def test_missing_uppercase(self):
        self.assertFalse(validate_password("securepass1!"))

    def test_missing_lowercase(self):
        self.assertFalse(validate_password("SECUREPASS1!"))

    def test_missing_digit(self):
        self.assertFalse(validate_password("SecurePassword!"))

    def test_missing_special_char(self):
        self.assertFalse(validate_password("SecurePassword1"))

    def test_invalid_special_char(self):

        self.assertFalse(validate_password("SecurePass1_"))

    def test_empty_string(self):
        self.assertFalse(validate_password(""))

    def test_value_error_space_inside(self):
        with self.assertRaises(ValueError):
            validate_password("Pass 1234!")

    def test_value_error_space_start(self):
        with self.assertRaises(ValueError):
            validate_password(" Pass1234!")

    def test_value_error_space_end(self):
        with self.assertRaises(ValueError):
            validate_password("Pass1234! ")

    def test_type_error_int(self):
        with self.assertRaises(TypeError):
            validate_password(12345678)

    def test_type_error_none(self):
        with self.assertRaises(TypeError):
            validate_password(None)

    def test_type_error_list(self):
        with self.assertRaises(TypeError):
            validate_password(["P", "a", "s", "s", "1", "!"])


if __name__ == "__main__":
    unittest.main()