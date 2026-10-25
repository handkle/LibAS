import unittest

from api_client import parse_libraries

class LibraryParsingTests(unittest.TestCase):
    def test_filters_zero_floor(self):
        response = {
            'data':{
                'userAuth':{
                    'reserve':{
                        'libs':[
                            {
                                "lib_id": 101,
                                "lib_name": "示例阅览室",
                                "lib_floor": "2",
                                "is_open": True,
                            },
                            {
                                "lib_id": 102,
                                "lib_name": "过滤示例",
                                "lib_floor": "0",
                                "is_open": True,
                            }
                        ]
                    }
                }
            }
        }

        libraries = parse_libraries(response)

        self.assertEqual(len(libraries), 1)
        self.assertEqual(libraries[0]['lib_id'], 101)

    def test_rejects_graphql_error(self):
        response = {
            'errors': [{'message':'示例错误'}]
        }

        with self.assertRaises(ValueError):
            parse_libraries(response)

    def test_rejects_missingdata(self):
        with self.assertRaises(ValueError):
            parse_libraries({})

if __name__ == '__main__':
    unittest.main()