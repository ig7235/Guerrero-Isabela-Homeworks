import unittest
from read_animals import num_legs_two_animals

class TestReadAnimals(unittest.TestCase):
  
   def test_num_legs_two_animals(self):
      self.assertEqual(num_legs_two_animals(10,5), 21)
      self.assertEqual(num_legs_two_animals(-1,21), 'animal does not exist')
      self.assertRaises(TypeError, num_legs_two_animals, [1,2])
      self.assertRaises(TypeError, num_legs_two_animals, True)
      self.assertRaises(TypeError, num_legs_two_animals, 'a')



if __name__ == '__main__':
   unittest.main()
