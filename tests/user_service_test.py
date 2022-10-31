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


    #Create User
    def test_createUser_returnsUserWithGeneratedID(self):
        #Arrange:
        generated_id = 3
        insert_data_func = lambda q, user: generated_id

        expected = User(id=generated_id, 
                        user_name='yasen_taha', 
                        password='',
                        role='professional',
                        email='yasen@gmail.com',
                        town_id=28)

        #Act:
        result = user_service.create_user(user_name='yasen_taha', 
                                            password='fhgjfghkfhdfhdskjhfsdhf',
                                            role='professional',
                                            email='yasen@gmail.com',
                                            town_id=28, insert_data_func=insert_data_func)

        #Assert:
        self.assertEqual(expected, result) 


    #Return Town Id By Name
    def test_returnTownIdByName_returnsIdWhenTownPresent(self):
        #Arrange:
        read_single_data_func = lambda q, town_id: (28,)
        expected = 28

        #Act:
        result = user_service.get_town_id_by_name('Sofia', read_data_func=read_single_data_func)

        #Assert:
        self.assertEqual(expected, result) 


    def test_returnTownIdByName_returnsIdWhenTownPresent(self):
        #Arrange:
        read_single_data_func = lambda q, town_id: (28,)
        expected = 28

        #Act:
        result = user_service.get_town_id_by_name('Sofia', read_data_func=read_single_data_func)

        #Assert:
        self.assertEqual(expected, result) 

    def test_returnTownIdByName_returnsNoneWhenTownNotPresent(self):
        #Arrange:
        read_single_data_func = lambda q, town_id: None
        expected = None

        #Act:
        result = user_service.get_town_id_by_name('London', read_data_func=read_single_data_func)

        #Assert:
        self.assertEqual(expected, result) 


    #Valid Email
    def test_validEmail_returns_Email_when_valid(self):
        #Arrange:
        email = 'yasen@gmail.com'
        expected = email

        #Act:
        result = user_service.valid_email(email)

        #Assert:
        self.assertEqual(expected, result)

    def test_validEmail_returns_None_when_invalidEmailExtension(self):
        #Arrange:
        email = 'yasen@gmail'
        expected = None

        #Act:
        result = user_service.valid_email(email)

        #Assert:
        self.assertEqual(expected, result)

    def test_validEmail_returns_None_when_invalidEmail_NoAtMail(self):
        #Arrange:
        email = 'yasengmail.com'
        expected = None

        #Act:
        result = user_service.valid_email(email)

        #Assert:
        self.assertEqual(expected, result)


    #Valid Username
    def test_validUsername_returns_userName_when_valid(self):
        #Arrange:
        user_name = 'yasen_taha'
        expected = user_name

        #Act:
        result = user_service.valid_username(user_name)

        #Assert:
        self.assertEqual(expected, result)

    def test_validUsername_returns_None_when_lessThanTwoChars(self):
        #Arrange:
        user_name = 'y'
        expected = None

        #Act:
        result = user_service.valid_username(user_name)

        #Assert:
        self.assertEqual(expected, result)

    def test_validUsername_returns_None_when_moreThanThirtyChars(self):
        #Arrange:
        user_name = 'yasenyasenyasenyasenyasenyaseny'
        expected = None

        #Act:
        result = user_service.valid_username(user_name)

        #Assert:
        self.assertEqual(expected, result)

    #Password Confirmation
    def test_passwordConfirmation_returns_True_when_bothPasswordsAreSame(self):
        #Arrange:
        password = 'adminateyak'
        confirmation = 'adminateyak'
        expected = True

        #Act:
        result = user_service.password_confirmation(password, confirmation)

        #Assert:
        self.assertEqual(expected, result)

    def test_passwordConfirmation_returns_False_when_bothPasswordsAreNotSame(self):
        #Arrange:
        password = 'adminateyak'
        confirmation = 'adminategotin'
        expected = False

        #Act:
        result = user_service.password_confirmation(password, confirmation)

        #Assert:
        self.assertEqual(expected, result)
