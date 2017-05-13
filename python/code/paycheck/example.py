import unittest
from paycheck import with_checker

class TestTypes(unittest.TestCase):

    @with_checker(int)
    def test_int(self, i):
        self.assertTrue(isinstance(i, int))

    @with_checker([int])
    def test_get_list(self, list_of_ints):
        self.assertTrue(isinstance(list_of_ints, list))
        for i in list_of_ints:
            self.assertTrue(isinstance(i, int))

    @with_checker([{str: int}])
    def test_list_of_dict_of_int_string(self, list_of_dict_of_int_string):
        self.assertTrue(isinstance(list_of_dict_of_int_string, list))

        for dict_of_int_string in list_of_dict_of_int_string:
            self.assertTrue(isinstance(dict_of_int_string, dict))

            for key, value in dict_of_int_string.items():
                self.assertTrue(isinstance(key, str))
                self.assertTrue(isinstance(value, int))

if __name__ == '__main__':
    unittest.main()
