from server.data.models import WorkPlace, Skill, Status
from server.data import database
import re

def validate_work_place(work_place:str):
    validation_work_places = [WorkPlace.HYBRID, WorkPlace.ONSITE, WorkPlace.REMOTE]
    if not work_place in validation_work_places:
        return False
    return True

def validate_status(status:str, for_job_ad: bool):
    validation_status = []
    if for_job_ad:
        validation_status = [Status.ACTIVE, Status.ARCHIVED]
    else:
        validation_status = [Status.ACTIVE, Status.HIDDEN, Status.PRIVATE]
    
    if not status in validation_status:
        return False
    return True


def parse_salary_range(salary_range:str):
    min_salary, max_salary = (int(min_max) for min_max in salary_range.split('-'))
    return min_salary, max_salary

def salary_range_threshold(salary_range:tuple, threshold=int):
    min_salary, max_salary = salary_range
    min_salary -= threshold
    max_salary += threshold
    return int(min_salary), int(max_salary)

def parse_skills(skills:str) -> tuple:
    parsed_skills = tuple(remove_under_from_skill(skill) for skill in skills.split(','))

    return parsed_skills

def remove_under_from_skill(skill:str):
    if '_' in skill:
        str_list = skill.split('_')
        new_skil = ' '.join(str_list)

        return new_skil
    else:
        return skill

def validate_stars(skills: list[Skill]):
    for skill in skills:
        if not 1 <= skill.stars <= 5:
            return False
    return True


def validate_salary(min_salary, max_salary):
    if not 1 <= min_salary <= max_salary:
        return False
    return True

def add_skills(skills: list[Skill]): #add skill in DB
    for skill in skills:
        if not skill_exists(skill.name):
            add_skill(skill.name)

def return_skills_with_ids(skills: list[Skill]) -> list[Skill]:
    skills_with_ids = []
    for skill in skills:
        skill.id = get_skill_id_by_name(skill.name)
        skills_with_ids.append(skill)

    return skills_with_ids

def add_skill(skill_name: str, insert_data_func=database.insert_query):
    generated_id = insert_data_func(
        '''INSERT INTO skills(name) VALUES (?)''', (skill_name,))

    return generated_id

def skill_exists(skill_name:str, read_data_func=database.read_query) -> bool:
    skill_name = skill_name.lower()
    data = read_data_func('SELECT 1 from skills where name = ?', (skill_name,))

    return any(data)

def get_skill_id_by_name(skill_name:str, read_data_func=database.read_query_single_element) -> int:
    skill_id = (read_data_func('SELECT id from skills where name = ?', (skill_name,)))

    return skill_id[0] if skill_id else None

def get_town_name_by_id(town_id: int, read_data_func=database.read_query):
    town_name = read_data_func('''SELECT t.name
    FROM towns as t
    WHERE t.id=?''', (town_id,))

    return town_name[0] if town_name else None

def get_town_id_by_name(town_name:str, read_data_func=database.read_query_single_element) -> int:
    town_id = (read_data_func('SELECT id from towns where name = ?', (town_name,)))

    return town_id[0] if town_id else None


def valid_username(user_name: str):
    '''Expects a user name as string, and if valid, it will return it, otherwise it will return None.'''
    if len(user_name) < 2 or len(user_name) > 30:
        return None
    else:
        return user_name

def valid_email(email: str):
    '''Expects an email address as string, and if valid, it will return it, otherwise it will return None.'''
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return email
    else:
        return None