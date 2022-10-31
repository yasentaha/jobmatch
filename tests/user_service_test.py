import unittest
from unittest.mock import Mock, create_autospec, patch
from server.data.models import User
from server.services import user_service

class UserService_Should(unittest.TestCase):
    
    #Find By Username
    def test_findByUsername_returns_singleUser_when_dataIsPresent(self):
        #Arrange:
        get_data_func = lambda q, user_name: [(1, 'yasen_taha', 'fhgjfghkfhdfhdskjhfsdhf', 'professional')]
        expected = User(id=1, user_name='yasen_taha', password='fhgjfghkfhdfhdskjhfsdhf', role='professional')
        
        #Act:
        result = user_service.find_by_username(1, get_data_func)

        #Assert:
        self.assertEqual(expected, result)

    def test_findByUsername_returns_None_when_noDataIsPresent(self):
        #Arrange:
        get_data_func = lambda q, user_name: []
        expected = None
        
        #Act:
        result = user_service.find_by_username(1, get_data_func)

        #Assert:
        self.assertEqual(expected, result)



