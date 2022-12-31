from http import HTTPStatus
from copy import deepcopy

from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib import auth

from netflix.models import Category, Movie


TEST_DATA = {
    "firstname": "John",
    "lastname": "Joe",
    "email": "johnjoe@gmail.com",
    "password": "NetflixClone2022",
    "password_conf": "NetflixClone2022"
}


class IndexTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Action")
        self.spider_man_movie = Movie.objects.create(
            name="Spider man",
            category=self.category
        )
        self.avatar_movie = Movie.objects.create(
            name="Avatar",
            category=self.category
        )

    def test_index_render_all_movies(self):
        response = self.client.get("/")
        # make sure index displays the two movies
        self.assertContains(response, self.spider_man_movie.name)
        self.assertContains(response, self.avatar_movie.name)

    def test_index_filter_movies(self):
        # make sure only `Avatar` movie is rendered when the search term is `ava`
        # This also asserts that the search is case insensitive as the real name
        # is `Avatar` with upper `A` and we search `ava`.
        response = self.client.post(
            "/",
            data={"search_text": "avat"}
        )
        # make sure index displays `Avatar` movie
        self.assertContains(response, self.avatar_movie.name)
        # Make sure index doesn't display `Spider man` movie
        self.assertNotContains(response, self.spider_man_movie.name)


# Create your tests here.
class RegisterTests(TestCase):

    def test_get_registration_page(self):
        # We call the `register` route using `GET`
        response = self.client.get("/register")
        # We make an assertion that no error is returned
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # We assert that the returned page contains the button for registration
        # form
        self.assertContains(
            response,
            '<button type="submit">Register</button>',
            html=True
        )

    def test_registration_with_valid_data(self):
        # We make sure that there no user exists in the database before the registration
        self.assertEqual(User.objects.count(), 0)

        # We call the `register` route using `POST` to simulate form submission
        # with the good data in the setup
        self.client.post("/register", data=TEST_DATA)

        # We make sure that there is 1 user created in the database after the registration
        self.assertEqual(User.objects.count(), 1)

        # We make sure that new created user data are the same we used during registration
        new_user = User.objects.first()
        self.assertEqual(new_user.first_name, TEST_DATA['firstname'])
        self.assertEqual(new_user.last_name, TEST_DATA['lastname'])
        self.assertEqual(new_user.email, TEST_DATA['email'])

    def test_registration_with_empty_fields(self):
        # We make sure that there no user exists in the database before the registration
        self.assertEqual(User.objects.count(), 0)

        # We call the `register` route using `POST` to simulate form submission
        # with empty fields data
        response = self.client.post(
            "/register",
            data={
                "firstname": "",
                "lastname": "",
                "email": "",
                "password": "",
                "password_conf": ""
            }
        )

        # We make sure that there no user exists in the database after the registration
        # failure. That means no user has been created
        self.assertEqual(User.objects.count(), 0)
        # Make sure the required message is displayed
        self.assertContains(response, 'This field is required')

    def test_registration_with_wrong_password_confirmation(self):
        # We make sure that there no user exists in the database before the registration
        self.assertEqual(User.objects.count(), 0)

        # We call the `register` route using `POST` to simulate form submission
        # with wrong password confirmation good data in the setup
        # This time, to create the invalid dict, we create a copy of the good
        # data of the setup first.
        bad_data = deepcopy(TEST_DATA)
        bad_data['password_conf'] = "Wrong Password Confirmation"
        response = self.client.post(
            "/register",
            data=bad_data
        )

        # We make sure that there no user exists in the database after the registration
        # failure. That means no user has been created
        self.assertEqual(User.objects.count(), 0)

        # Make sure the wrong confirmation is displayed
        self.assertContains(response, 'wrong confirmation')


class LoginTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="johnjoe@gmail.com")
        self.user_password = "NetflixPassword2022"
        self.user.set_password(self.user_password)
        self.user.save()

    def test_login_with_invalid_credentials(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        response = self.client.post(
            "/login",
            data={"email": self.user.username, "password": "Wrong password"}
        )
        self.assertContains(response, 'Invalid credentials.')
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_login_with_good_credentials(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.client.post(
            "/login",
            data={"email": self.user.username, "password": self.user_password}
        )
        self.assertTrue(auth.get_user(self.client).is_authenticated)
