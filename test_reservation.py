import unittest

from api_client import parse_reservation


class ReservationTests(unittest.TestCase):
    def test_no_reservation(self):
        response = {
            "data": {
                "userAuth": {
                    "reserve": {
                        "reserve": None,
                    }
                }
            }
        }

        self.assertIsNone(parse_reservation(response))

    def test_existing_reservation(self):
        record = {
            "lib_id": 101,
            "lib_name": "测试阅览室",
            "seat_key": "7,3",
            "seat_name": "389",
            "exp_date": 0,
        }

        response = {
            "data": {
                "userAuth": {
                    "reserve": {
                        "reserve": record,
                    }
                }
            }
        }

        result = parse_reservation(response)

        self.assertEqual(result["lib_id"], 101)
        self.assertEqual(result["seat_name"], "389")
        self.assertEqual(result["seat_key"], "7,3")

    def test_graphql_error(self):
        response = {
            "errors": [{"message": "测试错误"}]
        }

        with self.assertRaises(ValueError):
            parse_reservation(response)

    def test_missing_data_is_not_no_reservation(self):
        with self.assertRaises(ValueError):
            parse_reservation({})


if __name__ == "__main__":
    unittest.main()