import unittest
from unittest.mock import Mock

from server.common.responses import BadRequest
from server.data.models import (Company, CompanyRegisterData, LoginData,
                                Professional, ProfessionalRegisterData, User)
from server.routers import users
from server.routers import users as users_router

mock_user_service = Mock(spec='server.services.user_service')
mock_professional_service = Mock(spec='server.services.professional_service')
mock_company_service = Mock(spec='server.services.company_service')
mock_auth = Mock(spec='server.common.auth')
users.user_service = mock_user_service

def fake_user(id=1, user_name='Test_user', password='Test_password', role='Test_role'):
    mock_user = Mock(spec=User)
    mock_user.id = id
    mock_user.user_name = user_name
    mock_user.password = password
    mock_user.role = role
    return mock_user

def fake_login_data(user_name='Test_user', password='Test_password'):
    mock_login_data = Mock(spec=LoginData)
    mock_login_data.user_name = user_name
    mock_login_data.password = password
    return mock_login_data

def fake_token_and_role(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJUZXN0X3VzZXIifQ.YprWHS5M6v8Wlju60gpUTmmYwQDbrsYiAFVqYWXQlQ8', role='Test_role'):
    fake_token_role = {'token': token,
                    'role': role}

    return fake_token_role

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

def fake_professional_register_data(user_name='Test_user',
                    password='Test_password',
                    confirm_password='Test_password',
                    first_name='Test_first_name', 
                    last_name='Test_last_name', 
                    summary='Test_summary',
                    email='test@test.com', 
                    town_name='Sofia'):
    mock_professional_register_data = Mock(spec=ProfessionalRegisterData)
    mock_professional_register_data.user_name = user_name
    mock_professional_register_data.password = password
    mock_professional_register_data.confirm_password = confirm_password
    mock_professional_register_data.first_name = first_name
    mock_professional_register_data.last_name = last_name
    mock_professional_register_data.summary = summary
    mock_professional_register_data.email = email
    mock_professional_register_data.town_name = town_name

def fake_company_register_data(user_name='Test_user',
                    password='Test_password',
                    confirm_password='Test_password',
                    company_name='Test_first_name', 
                    description='Test_summary',
                    email='test@test.com',
                    address='Test_address', 
                    town_name='Sofia'):
    mock_company_register_data = Mock(spec=CompanyRegisterData)
    mock_company_register_data.user_name = user_name
    mock_company_register_data.password = password
    mock_company_register_data.confirm_password = confirm_password
    mock_company_register_data.company_name = company_name
    mock_company_register_data.description = description
    mock_company_register_data.email = email
    mock_company_register_data.address = address
    mock_company_register_data.town_name = town_name

class UsersRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        mock_company_service.reset_mock()
        mock_professional_service.reset_mock()
        mock_user_service.reset_mock()
        mock_auth.reset_mock()

    def test_logIn_returns_tokenAndRole_when_validData(self):
        user = fake_user()
        login_data = fake_login_data()

        mock_user_service.try_login = lambda user_name, password: user
        token = fake_token_and_role()

        result = users.login(login_data)
        expected = token

        self.assertEqual(expected, result)


    def test_logIn_returns_badRequest_when_invalidData(self):
        login_data = fake_login_data()

        mock_user_service.try_login = lambda user_name, password: None

        result = type(users.login(login_data))
        expected = BadRequest

        self.assertEqual(expected, result)