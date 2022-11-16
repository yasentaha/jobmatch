import unittest
from server.data.models import Professional
from server.services import professional_service



class ProfessionalService_Should(unittest.TestCase):

    def test_get_professional_by_id(self):
        get_data_func = lambda q, id: [(1,'kiril_nik','kiril_123@abv.bg',
                                       '0878777444','bul. Cherni Vruh 1',
                                       'Sofia','Kiril','Nikolov','Number one',1)]
        result = professional_service.get_professional_by_id(1,get_data_func)
        expected = Professional(id=1,
                                user_name='kiril_nik',
                                email='kiril_123@abv.bg',
                                phone='0878777444',
                                address='bul. Cherni Vruh 1',
                                town_name='Sofia',
                                first_name='Kiril',
                                last_name='Nikolov',
                                summary='Number one',
                                busy=1)
        self.assertEqual(expected, result)


    def test_edit_professional(self):
        self.fail()


    def test_make_professional_busy(self):
        self.fail()
