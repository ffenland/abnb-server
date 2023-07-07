from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestFacilities(APITestCase):
    NAME = "Test Facility"
    DES = "Test Description"
    URL = "/api/v1/cafes/facilities/"

    def setUp(self) -> None:
        models.Facility.objects.create(
            name=self.NAME,
            description=self.DES,
        )

    def test_all_facilities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )

        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DES,
        )

    def test_create_facility(self):
        new_facility_name = "NEW TEST FACILITY"
        new_facility_description = "NEW FACILITY DESCRIPTION"
        response = self.client.post(
            self.URL,
            data={
                "name": new_facility_name,
                "description": new_facility_description,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 code",
        )
        self.assertEqual(data["name"], new_facility_name)
        self.assertEqual(data["description"], new_facility_description)

        response = self.client.post(self.URL)

        self.assertEqual(
            response.status_code,
            400,
        )
        data = response.json()

        self.assertIn("name", data)


class TestFacility(APITestCase):
    NAME = "Test Facility"
    DES = "Test Description"

    def setUp(self) -> None:
        models.Facility.objects.create(
            name=self.NAME,
            description=self.DES,
        )

    def test_facility_not_found(self):
        response = self.client.get("/api/v1/cafes/facilities/2")
        self.assertEqual(response.status_code, 404)

    def test_get_facility(self):
        response = self.client.get("/api/v1/cafes/facilities/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DES)

    def test_put_facility(self):
        pass

    def test_delete_facility(self):
        response = self.client.delete("/api/v1/cafes/facilities/1")
        self.assertEqual(response.status_code, 204)


class TestCafe(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="tester")
        user.set_password("1234")
        user.save()
        self.user = user

    def test_create_cafe(self):
        response = self.client.post("/api/v1/cafes/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username="tester", password="1234")

        response = self.client.post("/api/v1/cafes/")
        print(response.json())
