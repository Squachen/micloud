import unittest
import logging
import os, json

from micloud import MiCloud
from tests.configuration import setup_testing_environment

setup_testing_environment()

class TestMiCloud(unittest.TestCase):

    """def test_login_success(self):
        mc = MiCloud(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        f = open("tests.txt", "w")
        f.write("Now the file has more content!")
        f.close()
        self.assertTrue(mc.login())"""

    def test_get_devices(self):
        mc = MiCloud(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        self.assertTrue(mc.login())

        self.assertIsNotNone(mc.get_token())

        res = mc.get_devices(save=True)
        self.assertIsNotNone(res)
        self.assertTrue(type(res)==list)

        
        

if __name__ == '__main__':  
    unittest.main()
    
