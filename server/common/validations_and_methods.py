from server.data.models import WorkPlace, Skill, Status, Town
from server.data.database import read_query, update_query, read_query_single_element, insert_query
'''
validacii za kinti
i vsichko keoto se setim
i koeto se preizpolzva kato naprimer get town by id i tn i tn

'''

def validate_work_place(work_place:str):
    validation_work_places = [WorkPlace.HYBRID, WorkPlace.ONSITE, WorkPlace.REMOTE]
    if not work_place in validation_work_places:
        return False
    return True

def validate_status(status:str):
    validation_status = [Status.ACTIVE, Status.HIDDEN, Status.PRIVATE]
    if not status in validation_status:
        return False
    return True


def parse_salary_range(salary_range:str):
    #IN ROUTER VALIDATION
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

def add_skill(skill_name: str):
    generated_id = insert_query(
        '''INSERT INTO skills(name) VALUES (?)''', (skill_name,))

    return generated_id

def skill_exists(skill_name:str) -> bool:
    skill_name = skill_name.lower()
    data = read_query('SELECT 1 from skills where name = ?', (skill_name,))

    return any(data)

def get_skill_id_by_name(skill_name:str) -> int:
    skill_id = (read_query_single_element('SELECT id from skills where name = ?', (skill_name,)))

    return skill_id[0] if skill_id else None

def get_town_name_by_id(town_id: int):
    data = read_query('''SELECT t.name
    FROM towns as t
    WHERE t.id=?''', (town_id,))[0]

    return data

def get_town_id_by_name(town_name: str) -> int:
    town_id = (read_query_single_element('SELECT id from towns where name = ?', (town_name,)))[0]

    return town_id