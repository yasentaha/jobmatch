import unittest
from unittest.mock import Mock
from server.data.models import User, Professional, Company, LoginData, CompanyRegisterData, ProfessionalRegisterData
from server.routers import users as users_router
from server.common.responses import NotFound, Success

mock_user_service = Mock(spec='server.services.user_service')
mock_professional_service = Mock(spec='server.services.professional_service')
mock_company_service = Mock(spec='server.services.company_service')

def fake_user(id=1, user_name='Test_user', password='Test_password', role='Test_role'):
    mock_user = Mock(spec=User)
    mock_user.id = id
    mock_user.user_name = user_name
    mock_user.password = password
    mock_user.role = role
    return mock_user

def fake_professional(id=1, 
                    user_name='Test_user', 
                    email='test@test.com', 
                    town_name='Sofia', 
                    first_name='Test_first_name', 
                    last_name='Test_last_name', 
                    summary='Test_summary', 
                    busy=False):
    mock_professional = Mock(spec=Professional)
    mock_professional.id = id
    mock_professional.user_name = user_name
    mock_professional.email = email
    mock_professional.town_name = town_name
    mock_professional.first_name = first_name
    mock_professional.last_name = last_name
    mock_professional.summary = summary
    mock_professional.busy = busy

    return mock_professional

# def fake_company(id=1, 
#                 user_name='Test_user_name', 
#                 password='Test_password', 
#                 company_name='Test_company_name', 
#                 description='Test_description', 
#                 email='test@test.com', 
#                 address='Test_address', 
#                 town_id=, 
#                 successful_matches):
#     mock_professional = Mock(spec=Company)
#     mock_professional.id = id
#     mock_professional.user_name = user_name
#     mock_professional.email = email
#     mock_professional.town_name = town_name
#     mock_professional.first_name = first_name
#     mock_professional.last_name = last_name
#     mock_professional.summary = summary
#     mock_professional.busy = busy
    
#     return mock_professional

class UsersRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        mock_company_service.reset_mock()
        mock_professional_service.reset_mock()
        mock_user_service.reset_mock

    def test_registerProfessional_returns_SuccessMessage_when_professionalIsValid(self):
        mock_user_service.create_user = lambda user: fake_user
        mock_professional_service.get_professional_by_id = lambda professional:fake_professional

        expected = Success

        result = users_router.register_professional()
        self.assertEqual(expected, result)