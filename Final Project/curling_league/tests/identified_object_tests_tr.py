from identified_object import IdentifiedObject
import unittest


class IdentifiedObjectTest(unittest.TestCase):
    def test_identified_object_created(self):
        """identified object is created with specified oid"""
        i_object = IdentifiedObject(123)

        self.assertIsInstance(i_object, IdentifiedObject, "Is not an Identified Object")
        self.assertEqual(123, i_object.oid)

    def test_identified_objects_are_equal(self):
        """Tests whether identified objects have the same oid and are of the same type"""
        test_object1 = IdentifiedObject(123)
        test_object2 = IdentifiedObject(123)
        test_object3 = IdentifiedObject(456)
        test_string = "123"

        self.assertTrue(test_object1 == test_object2)
        self.assertFalse(test_object1 == test_object3)
        self.assertFalse(test_object1 == test_string)

    def test_identified_objects_are_hashable(self):
        """Tests whether identified objects are correctly hashable"""
        test_object1 = IdentifiedObject(123)
        test_object2 = IdentifiedObject(123)
        test_object3 = IdentifiedObject(456)

        self.assertTrue(hash(test_object1) == hash(test_object2))
        self.assertFalse(hash(test_object1) == hash(test_object3))


if __name__ == '__main__':
    unittest.main()
