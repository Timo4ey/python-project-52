from django.test import TransactionTestCase

from task_manager.users.forms import SignUpForm


class TestSignUpForm(TransactionTestCase):
    def test_sign_up_form_validate(self):
        form_valid = SignUpForm(
            data={
                "first_name": "Garry",
                "last_name": "Galler",
                "username": "garry_galler",
                "password1": "secretpassword",
                "password2": "secretpassword",
            }
        )
        self.assertTrue(form_valid.is_valid())

        form_invalid_name_too_long = SignUpForm(
            data={
                "first_name": "Garry" * 31,
                "last_name": "Galler",
                "username": "garry_galler",
                "password1": "secretpassword",
                "password2": "secretpassword",
            }
        )
        self.assertFalse(form_invalid_name_too_long.is_valid())

        form_invalid_name_is_empty = SignUpForm(
            data={
                "first_name": "",
                "last_name": "Galler",
                "username": "garry_galler",
                "password1": "secretpassword",
                "password2": "secretpassword",
            }
        )
        self.assertFalse(form_invalid_name_is_empty.is_valid())

        form_invalid_last_name_too_long = SignUpForm(
            data={
                "first_name": "Garry",
                "last_name": "Galler" * 31,
                "username": "garry_galler",
                "password1": "secretpassword",
                "password2": "secretpassword",
            }
        )
        self.assertFalse(form_invalid_last_name_too_long.is_valid())

        form_invalid_last_name_is_empty = SignUpForm(
            data={
                "first_name": "Garry",
                "last_name": "",
                "username": "garry_galler",
                "password1": "secretpassword",
                "password2": "secretpassword",
            }
        )
        self.assertFalse(form_invalid_last_name_is_empty.is_valid())

        form_invalid_username_too_long = SignUpForm(
            data={
                "first_name": "Garry",
                "last_name": "Galler",
                "username": "garry_galler" * 15,
                "password1": "secretpassword",
                "password2": "secretpassword",
            }
        )
        self.assertFalse(form_invalid_username_too_long.is_valid())

        form_invalid_username_is_empty = SignUpForm(
            data={
                "first_name": "Garry",
                "last_name": "Galler",
                "username": "",
                "password1": "secretpassword",
                "password2": "secretpassword",
            }
        )
        self.assertFalse(form_invalid_username_is_empty.is_valid())
