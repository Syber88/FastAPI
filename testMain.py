import unittest
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.test_user = {
            "firstName": "Siya",
            "lastName": "Syber",
            "email": "Siya.syber@testing.com",
            "phone_number": "1234567890"
        }
        client.post("/users/", json=self.test_user)

    def test_create_user_duplicate(self):
        response = client.post("/users/", json=self.test_user)
        self.assertEqual(response.status_code, 400)
        self.assertIn("user already exitsts", response.text)

    def test_get_user_by_email(self):
        response = client.get(f"/users/by-email/{self.test_user['email']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], self.test_user["email"])

    def test_update_user_by_email(self):
        update_data = {"firstName": "Johnny"}
        response = client.post(
            f"/users/by-email/{self.test_user['email']}",
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user updated successfully, user "]["firstName"], "Johnny")

    def test_get_all_users(self):
        response = client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))
        self.assertGreater(len(response.json()), 0)

    def test_delete_user_by_email(self):
        response = client.delete(f"/users/by-email/{self.test_user['email']}")
        self.assertEqual(response.status_code, 200)

        # Confirm user no longer exists
        response_check = client.get(f"/users/{self.test_user['email']}")
        self.assertEqual(response_check.status_code, 404)

if __name__ == '__main__':
    unittest.main()
