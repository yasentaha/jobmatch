import unittest
from server.data.models import Skill
from server.common import validations_and_methods

class ValidationService_Should(unittest.TestCase):
    def test_validateWorkSpace_returns_False_when_WrongData(self):
        work = 'sfgw'
        result = validations_and_methods.validate_work_place(work)
        expected = False
        self.assertEqual(expected, result)


    def test_validateWorkSpace_returns_True_when_DataIsCorrect(self):
        work = 'Remote'
        result = validations_and_methods.validate_work_place(work)
        expected = True
        self.assertEqual(expected, result)
    
    def test_validateStatusForJobAd_returns_False_when_DataIsWrong(self):
        status = ''
        for_job_ad = True
        result = validations_and_methods.validate_status(status, for_job_ad)
        expected = False
        self.assertEqual(expected, result)
    
    def test_validateStatusForJobAd_returns_True_when_DataIsCorrect(self):
        status = "Active"
        for_job_ad = True
        result = validations_and_methods.validate_status(status, for_job_ad)
        expected = True
        self.assertEqual(expected, result)
    
    def test_validateStatusForResume_returns_True_when_DataIsCorrect(self):
        status = 'Private'
        for_job_ad = False
        result = validations_and_methods.validate_status(status, for_job_ad)
        expected = True
        self.assertEqual(expected, result)
    
    def test_validateStatusForResume_returns_False_when_DataIsWrong(self):
        status = 'agfag'
        for_job_ad = False
        result = validations_and_methods.validate_status(status, for_job_ad)
        expected = False
        self.assertEqual(expected, result)
    
    def test_validateSalary_returns_True_when_SalaryRangeIsCorrect(self):
        min_salary = 1500
        max_salary = 3244
        result = validations_and_methods.validate_salary(min_salary, max_salary)
        expected = True
        self.assertEqual(expected, result)
    
    def test_validateSalary_returns_False_when_SalaryRangeIsIncorrect(self):
        min_salary = - 100
        max_salary = 1400
        result = validations_and_methods.validate_salary(min_salary, max_salary)
        expected = False
        self.assertEqual(expected, result)
    
    def test_validateSalary_returns_False_when_SalaryRangeIsIncorrect1(self):
        min_salary = 4000
        max_salary = 1400
        result = validations_and_methods.validate_salary(min_salary, max_salary)
        expected = False
        self.assertEqual(expected, result)
    
    def test_validateStars_returns_True_when_DataIsCorrect(self):
        skill = [Skill(name = 'python', stars = 5)]
        result = validations_and_methods.validate_stars(skill)
        expected = True
        self.assertEqual(expected, result)
    
    def test_validateStars_returns_False_when_DataIsIncorrect(self):
        skill = [Skill(name = 'python', stars = 10)]
        result = validations_and_methods.validate_stars(skill)
        expected = False
        self.assertEqual(expected, result)
    
    def test_RemoveUnderFromSkill_return_Correct(self):
        skill = 'new_skill'
        result = validations_and_methods.remove_under_from_skill(skill)
        expected = 'new skill'
        self.assertEqual(expected, result)
    
    def test_RemoveUnderFromSkill_return_Correct1(self):
        skill = 'skill'
        result = validations_and_methods.remove_under_from_skill(skill)
        expected = 'skill'
        self.assertEqual(expected, result)
    
    def test_ParsedSkills_return_Correct(self):
        skills = 'python,sql,azure'
        result = validations_and_methods.parse_skills(skills)
        expected = ('python', 'sql', 'azure')
        self.assertEqual(expected, result)
    
    def test_ParsedSalaryRange_return_CorrectData(self):
        salary_range = '1200-2400'
        result = validations_and_methods.parse_salary_range(salary_range)
        expected = (1200, 2400)
        self.assertEqual(expected, result)
    
    def test_SalaryRangeTreshold_return_CorrectData(self):
        salary_range = (1200, 2400)
        treshold = 400
        result = validations_and_methods.salary_range_threshold(salary_range, treshold)
        expected = (800, 2800)
        self.assertEqual(expected, result)
    
    def test_returnTownIdByName_returnsId_WhenTownPresent(self):
        read_single_data_func = lambda q, town_id: (28,)
        expected = 28
        result = validations_and_methods.get_town_id_by_name('Sofia', read_data_func=read_single_data_func)
        self.assertEqual(expected, result) 
    
    def test_returnTownIdByName_returnsNone_WhenTownNotPresent(self):
        read_single_data_func = lambda q, town_id: None
        expected = None
        result = validations_and_methods.get_town_id_by_name('London', read_data_func=read_single_data_func)
        self.assertEqual(expected, result) 
    
    def test_returnTownNameById_returnsName_WhenTownPresent(self):
        read_data_func = lambda q, town_name: ('Sofia',)
        expected = 'Sofia'
        result = validations_and_methods.get_town_name_by_id(28, read_data_func=read_data_func)
        self.assertEqual(expected, result) 
    
    def test_returnTownNameById_returnsNone_WhenTownNotPresent(self):
        read_data_func = lambda q, town_name: None
        expected = None
        result = validations_and_methods.get_town_name_by_id(58, read_data_func=read_data_func)
        self.assertEqual(expected, result) 
    
    def test_returnSkillIdByName_returnsId_WhenSkillPresent(self):
        read_data_func = lambda q, skill: (1, 'python', 4)
        expected = 1
        result = validations_and_methods.get_skill_id_by_name('python', read_data_func=read_data_func)
        self.assertEqual(expected, result) 
    
    def test_returnSkillIdByName_returnsNone_WhenSkillNotPresent(self):
        read_data_func = lambda q, skill: ()
        expected = None
        result = validations_and_methods.get_skill_id_by_name('python', read_data_func=read_data_func)
        self.assertEqual(expected, result) 
    
    def test_returnSkillExist_returnsTrue_WhenSkillPresent(self):
        read_data_func = lambda q, skill: (1, 'python', 4)
        expected = True
        result = validations_and_methods.skill_exists('python', read_data_func=read_data_func)
        self.assertEqual(expected, result) 
    
    def test_returnSkillExist_returnsFalse_WhenSkillNotPresent(self):
        read_data_func = lambda q, skill: ()
        expected = False
        result = validations_and_methods.skill_exists('python', read_data_func=read_data_func)
        self.assertEqual(expected, result) 
    
    def test_AddSkill_returnsCorrect(self):
        generated_id = 2
        insert_data_func = lambda q, skill: generated_id
        result = validations_and_methods.add_skill('python', insert_data_func=insert_data_func)
        expected = generated_id
        self.assertEqual(expected, result)
    
    def test_validEmail_returns_Email_when_valid(self):
        email = 'yasen@gmail.com'
        expected = email
        result = validations_and_methods.valid_email(email)
        self.assertEqual(expected, result)

    def test_validEmail_returns_None_when_invalidEmailExtension(self):
        email = 'yasen@gmail'
        expected = None
        result = validations_and_methods.valid_email(email)
        self.assertEqual(expected, result)

    def test_validEmail_returns_None_when_invalidEmail_NoAtMail(self):
        email = 'yasengmail.com'
        expected = None
        result = validations_and_methods.valid_email(email)
        self.assertEqual(expected, result)


    def test_validUsername_returns_userName_when_valid(self):
        user_name = 'yasen_taha'
        expected = user_name
        result = validations_and_methods.valid_username(user_name)
        self.assertEqual(expected, result)

    def test_validUsername_returns_None_when_lessThanTwoChars(self):
        user_name = 'y'
        expected = None
        result = validations_and_methods.valid_username(user_name)
        self.assertEqual(expected, result)

    def test_validUsername_returns_None_when_moreThanThirtyChars(self):
        user_name = 'yasenyasenyasenyasenyasenyaseny'
        expected = None
        result = validations_and_methods.valid_username(user_name)
        self.assertEqual(expected, result)

    