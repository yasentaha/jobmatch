from server.data.database import read_query, update_query, insert_query, read_query_single_element
from server.data.models import Company, JobAd, Status, Skill, CreateJobAd



def create_job_ad(company_id: int, create_job_ad: CreateJobAd, insert_data=None):
    if insert_data is None:
        insert_data = insert_query

    town_id = get_town_id_by_name(create_job_ad.town_name)

    generated_job_ad_id = insert_data(
        '''INSERT INTO job_ads(title, description, min_salary, max_salary, work_place,status,town_name,company_id) 
        values(?,?,?,?,?,?,?,?,?)''',
        (create_job_ad.title, create_job_ad.description, create_job_ad.min_salary, create_job_ad.max_salary,
         create_job_ad.work_place,create_job_ad.status, create_job_ad.town_name, company_id))

    return get_job_ad_by_id(generated_job_ad_id)

def get_job_ad_by_id(job_ad_id: int):
    
    data = read_query(
        '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, j.work_place, j.status, j.views, t.name
        FROM   
            job_ads AS j
        LEFT JOIN
            towns AS t ON j.town_id=t.id
        WHERE j.id=?''', (job_ad_id,))

    return next((JobAd.from_query_result(*row) for row in data), None)

def get_all_active_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, Status.ACTIVE))
    if data:
        return (id for id in data)
    else:
        return [0]

def get_all_archived_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, Status.ARCHIVED))

    if data:
        return (id for id in data)
    else:
        return [0]

def get_number_of_all_active_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, Status.ACTIVE))
    
    return len(data)

def get_all_skills_for_job_ad_id(job_ad_id: int):
    data = read_query(
        '''SELECT s.id, s.name,j_s.stars
                 FROM skills as s 
                 RIGHT JOIN 
                job_ads_skills as j_s
                ON s.id=j_s.skill_id
                    WHERE j_s.resume_id=?''', (job_ad_id,))
    return (Skill(id=id, name=name, stars=stars)
            for id, name, stars in data)

def update_job_ads_views(id: int):
    current_job_ads_view = (read_query_single_element('SELECT views from job_ads where id=?', (id,)))[0]

    updated_job_ads_view = current_job_ads_view + 1

    update_query('UPDATE job_ads SET views=? WHERE id=?', (updated_job_ads_view, id))

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

def add_skill_to_job_ad(job_ad_id: int, skill: Skill):

    insert_query(
        '''INSERT INTO job_ads_skills(job_ad_id, skill_id, stars) VALUES (?,?,?)''',
        (job_ad_id, skill.id, skill.stars))

def get_town_name_by_id(town_id: int):
    data = read_query('''SELECT t.name
    FROM towns as t
    WHERE t.id=?''', (town_id,))[0]

    return data


def get_town_id_by_name(town_name: str) -> int:
    town_id = (read_query_single_element('SELECT id from towns where name = ?', (town_name,)))[0]

    return town_id


def get_list_of_matches(id: int):
    ...