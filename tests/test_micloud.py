import unittest
import logging
import os, json

from micloud import MiCloud
from micloud.micloudexception import MiCloudAccessDenied
from tests.configuration import setup_testing_environment

setup_testing_environment()

class TestMiCloud(unittest.TestCase):

    # Will fail of network errors makes the login fail.
    def test_login_access_denied(self):
        mc = MiCloud('DEFFNOTAUSER', 'DEFFWRONGPW')
        self.assertRaises(MiCloudAccessDenied, mc.login)

    def test_get_devices(self):
        mc = MiCloud(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        self.assertTrue(mc.login())

        self.assertIsNotNone(mc.get_token())

        res = mc.get_devices(save=True)
        self.assertIsNotNone(res)
        self.assertTrue(type(res)==list)

    
        

if __name__ == '__main__':  
    unittest.main()
    
