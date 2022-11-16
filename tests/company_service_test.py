import unittest
from unittest.mock import Mock, create_autospec, patch
from server.data.models import Company
from server.services import company_service

class CompanyService_Should(unittest.TestCase):
    def test_getCompanyById_returnsCorrect_WhenCompanyPresent(self):
        get_data_func = lambda q, id: [(1,'Test','Test_company',
                                       'testtest','test@gmail.com',
                                       '0878787878','Test','Sofia',1)]
        result = company_service.get_company_by_id(1,get_data_func)
        expected = Company(id= 1,
                            user_name= 'Test',
                            company_name= 'Test_company',
                            description= 'testtest',
                            email= 'test@gmail.com',
                            phone= '0878787878',
                            address= 'Test',
                            town_name= 'Sofia',
                            successful_matches= 1)
        self.assertEqual(expected, result)
    
    def test_getCompanyById_returnsNone_WhenNoCompany(self):
        get_data_func = lambda q, id: []
        result = company_service.get_company_by_id(1,get_data_func)
        expected = None
        self.assertEqual(expected, result)
