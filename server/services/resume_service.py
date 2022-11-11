from sqlite3 import OperationalError
from server.common.responses import Success, BadRequest, NotFound
from server.data.database import read_query, insert_query, update_query, read_query_single_element
from server.data.models import Resume, Status, Skill, CreateResume, Role, JobAd, MatchRequestResponse, ResumeWithoutDescriptionAndSalary
from server.services.professional_service import get_professional_by_id
from server.services.job_ad_service import get_job_ad_by_id


# def all_active_resumes_without_job_salary_and_description_by_id(id: int):
#     data = read_query(
#         '''SELECT r.id, r.title, r.work_place, r.status, r.town_id
#                 FROM resumes as r
#                 WHERE r.professional_id=? AND r.status=?''', (id, f'%{Status.ACTIVE}%'))

#     return (Resume(id=id, title=title, description='None', min_salary=0, max_salary=0,
#                    work_place=work_place, status=status, town_id=town_id, main=main)
#             for id, title, description, min_salary, max_salary, work_place, status, town_id, main in data)

def all_active_resumes_without_job_salary_and_description_by_professional_id(professional_id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.work_place, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE r.professional_id=? AND r.status=?''', (professional_id, Status.ACTIVE))
    if data:
        return (ResumeWithoutDescriptionAndSalary.from_query_result(*row) for row in data)
    else:
        return None

def all_active(search: str | None = None, search_by: str | None = None, threshold: int | None = None, combined: bool | None = None):
    
    if search is None:
    
        data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                    r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE r.status=?''', (Status.ACTIVE,))

    else:
        if search_by == 'salary_range':
            if not threshold:
                min_salary, max_salary = parse_salary_range(search)
            else:
                min_salary, max_salary = salary_range_threshold(parse_salary_range(search),int(threshold))
            data = read_query(
                '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                    r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE r.status=?
                    AND r.min_salary >=?
                    AND r.max_salary <=?''', (Status.ACTIVE, min_salary, max_salary))

        elif search_by == 'location':
            data = read_query('''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                                r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE r.status='Active'
                    AND t.name LIKE ?

                    UNION
                    
                    SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                            r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE r.status='Active'
                    AND r.work_place="Remote"''',(f'%{search}%',))
        
        elif search_by == 'skills':
            skills_tuple = parse_skills(search)
            if combined == True:
                data = read_query(f'''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                            r.work_place, r.main, r.status, t.name, r.professional_id
                                FROM
                                    resumes AS r
                                        LEFT JOIN
                                    towns AS t ON r.town_id = t.id
                                        LEFT JOIN
                                    resumes_skills AS r_s ON r.id = r_s.resume_id
                                        LEFT JOIN
                                    skills AS s ON r_s.skill_id = s.id
                                WHERE
                                    r.status = "Active"
                                        AND s.name IN {skills_tuple}
                                        GROUP by r.id
                                        HAVING count(distinct s.name) = {len(skills_tuple)}''')
            else:
                data = read_query(f'''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                            r.work_place, r.main, r.status, t.name, r.professional_id
                                FROM
                                    resumes AS r
                                        LEFT JOIN
                                    towns AS t ON r.town_id = t.id
                                        LEFT JOIN
                                    resumes_skills AS r_s ON r.id = r_s.resume_id
                                        LEFT JOIN
                                    skills AS s ON r_s.skill_id = s.id
                                WHERE
                                    r.status = 'Active'
                                        AND s.name IN {skills_tuple}''')

        elif search_by == 'job_ad':
            job_ad = get_job_ad_by_id(search)
            if combined == True:
                data = read_query(f'''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                            r.work_place, r.main, r.status, t.name, r.professional_id
                                FROM
                                    resumes AS r
                                        LEFT JOIN
                                    towns AS t ON r.town_id = t.id
                                        LEFT JOIN
                                    resumes_skills AS r_s ON r.id = r_s.resume_id
                                        LEFT JOIN
                                    skills AS s ON r_s.skill_id = s.id
                                WHERE
                                    r.status = "Active"
                                        AND s.name IN {skills_tuple}
                                        GROUP by r.id
                                        HAVING count(distinct s.name) = {len(skills_tuple)}''')
            else:
                data = read_query(f'''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                            r.work_place, r.main, r.status, t.name, r.professional_id
                                FROM
                                    resumes AS r
                                        LEFT JOIN
                                    towns AS t ON r.town_id = t.id
                                        LEFT JOIN
                                    resumes_skills AS r_s ON r.id = r_s.resume_id
                                        LEFT JOIN
                                    skills AS s ON r_s.skill_id = s.id
                                WHERE
                                    r.status = 'Active'
                                        AND s.name IN {skills_tuple}''')

    if not data:
        return None

    #OSTAVAT OSHTE PO TOWNS VIJ REMOTE
    #PLUS PO SKILLS 

    return (Resume.from_query_result(*row) for row in data)


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


def all_hidden_resumes_by_id(id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, r.work_place, r.status, r.town_id,r.main 
                FROM resumes as r
                WHERE r.professional_id=? AND r.status=?''', (id, f'%{Status.HIDDEN}%'))

    return (Resume(id=id, title=title, description=description, min_salary=min_salary, max_salary=max_salary,
                   work_place=work_place, status=status, town_id=town_id, main=main)
            for id, title, description, min_salary, max_salary, work_place, status, town_id, main in data)

def create_resume(professional_id: int, resume: Resume, insert_data=None):
    if insert_data is None:
        insert_data = insert_query

    town_id = get_town_id_by_name(resume.town_name)

    generated_resume_id = insert_data(
        '''insert into resumes(title, description, min_salary, max_salary, work_place,main,status,town_id,professional_id) 
        values(?,?,?,?,?,?,?,?,?)''',
        (resume.title, resume.description, resume.min_salary, resume.max_salary,
         resume.work_place, resume.main, resume.status, town_id, professional_id))
    
    skills_with_ids = return_skills_with_ids(resume.skills)
    if generated_resume_id:
        [add_skill_to_resume(generated_resume_id, skill) for skill in skills_with_ids]

    return get_resume_by_id(generated_resume_id)

def create_resume_and_add_skill(professional_id: int, create_resume: CreateResume, insert_data=None):
    if insert_data is None:
        insert_data = insert_query

    town_id = get_town_id_by_name(create_resume.town_name)

    generated_resume_id = insert_data(
        '''insert into resumes(title, description, min_salary, max_salary, work_place,main,status,town_id,professional_id) 
        values(?,?,?,?,?,?,?,?,?)''',
        (create_resume.title, create_resume.description, create_resume.min_salary, create_resume.max_salary,
         create_resume.work_place, create_resume.main, town_id, professional_id))

    generated_skill_id = insert_data(
        '''insert into skills(name) 
        values(?)''', (create_resume.skill_name))

    skill: Skill

    skill = read_query_single_element(
        '''SELECT s.id, s.name FROM skills as s 
        WHERE s.name=?''', (create_resume.skill_name))

    create_resume.id = generated_resume_id
    skill.id = generated_skill_id

    insert_data(
        '''insert into resumes_skills (resume_id, skill_id, stars) values (?,?,?)''',
        (create_resume.id, skill.id, create_resume.stars))

    return Success(f'Resume with title {create_resume.title} was created!')


def get_resume_by_id(resume_id: int) -> Resume:
    data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                    r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE r.id=?
                    AND r.status != ?''', (resume_id, Status.HIDDEN))

    resume = next((Resume.from_query_result(*row) for row in data), None)
    resume.skills = get_all_resume_skills_by_id(resume.id)
    return resume


def edit_resume_by_professional_id_and_resume_id(professional_id: int, resume_id: int, new_resume: Resume,
                                                 update_data=None):
    if update_data is None:
        update_data = update_query

    town_id = get_town_id_by_name(new_resume.town_name)

    update_data(
        '''UPDATE resumes
            SET title=?, description=?, min_salary=?, max_salary=?,work_place=?,status=?,town_id=?,main=?
             WHERE professional_id = ? AND resumes.id=?''',
        (new_resume.title, new_resume.description, new_resume.min_salary, new_resume.max_salary, new_resume.work_place,
         new_resume.status, town_id, new_resume.main, professional_id, resume_id))

    old_resume_skills = get_all_resume_skills_by_id(resume_id)

    new_resume_skills = return_skills_with_ids(new_resume.skills)

    if new_resume_skills != old_resume_skills:
        delete_all_skills_from_resume(resume_id)
        [add_skill_to_resume(resume_id, skill)  for skill in new_resume_skills]

    return get_resume_by_id(resume_id)


def get_all_active_resumes_by_professional_id(professional_id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                    r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE r.professional_id=? AND r.status=?''', (professional_id, Status.ACTIVE))
    if data:
        return (Resume.from_query_result(*row) for row in data)
    else:
        return None



def get_all_archived_resumes_by_professional_id(professional_id: int):
    data = read_query(
        '''SELECT r.id
                    FROM resumes as r
                    WHERE r.professional_id=? AND r.status=?''', (professional_id, f'%{Status.ARCHIVED}%'))

    if data:
        return (id for id in data)
    else:
        return [0]


def get_all_resume_skills_by_id(resume_id: int):
    data = read_query(
        '''SELECT s.id, s.name,r_s.stars
                 FROM skills as s 
                 RIGHT JOIN 
                resumes_skills as r_s
                ON s.id=r_s.skill_id
                    WHERE r_s.resume_id=?''', (resume_id,))
    return [Skill.from_query_result(*row) for row in data]


def get_town_name_by_id(town_id: int):
    data = read_query('''SELECT t.name
    FROM towns as t
    WHERE t.id=?''', (town_id,))[0]

    return data


def get_town_id_by_name(town_name: str) -> int:
    town_id = (read_query_single_element('SELECT id from towns where name = ?', (town_name,)))[0]

    return town_id


def get_number_of_all_active_resumes(professional_id: int):
    data = read_query(
        '''SELECT r.id FROM resumes as r 
        WHERE r.professional_id=? AND r.status=?''', (professional_id, f'%{Status.ACTIVE}%',))

    return len(data)


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
    auto_increment_id = insert_query(
        '''INSERT INTO skills(name) VALUES (?)''', (skill_name,))

    return auto_increment_id

def skill_exists(skill_name:str) -> bool:
    skill_name = skill_name.lower()
    data = read_query('SELECT 1 from skills where name = ?', (skill_name,))

    return any(data)

def get_skill_id_by_name(skill_name:str) -> int:
    skill_id = (read_query_single_element('SELECT id from skills where name = ?', (skill_name,)))

    return skill_id[0] if skill_id else None

def add_skill_to_resume(resume_id: int, skill: Skill):
    # auto_increment_id = insert_query(
    #     '''INSERT INTO skills(name) VALUES (?)''', (skill.name))

    # skill.id = auto_increment_id

    insert_query(
        '''INSERT INTO resumes_skills(resume_id, skill_id, stars) VALUES (?,?,?)''',
        (resume_id, skill.id, skill.stars))

def delete_all_skills_from_resume(resume_id:int):

    update_query('''DELETE from resumes_skills where resume_id = ?''', (resume_id,))


def main_resume_for_professional_exists(professional_id:int):
    data = read_query('SELECT 1 from resumes where main = 1 and professional_id = ?', (professional_id,))

    return any(data)

def change_resume_main(professional_id:int):
    update_query(
        '''UPDATE resumes
            SET main=0
             WHERE professional_id = ? and main=1''',
        (professional_id,))

def not_exist_skill(professional_id: int, resume_id: int, skill: Skill):
    data = read_query(
        '''SELECT s.name FROM resumes as r
        LEFT JOIN resumes_skills rs on r.id = rs.resume_id
        LEFT JOIN skills s on rs.skill_id = s.id
        WHERE r.professional_id=? AND r.id=?''', (professional_id, resume_id))

    for name in data:
        if skill.name.lower() == name.lower():
            return False

    return True


def search_all_active_job_ads(search: str | None = None, search_by: str | None = None):
    if search is None:
        data = read_query(
            '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, j.work_place, j.status, j.views, t.name
            FROM   
                job_ads AS j
            LEFT JOIN
                towns AS t ON j.town_id=t.id
            WHERE j.status=?''', (f'{Status.ACTIVE}',))
    else:
        try:

            data = read_query(
                '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, j.work_place, j.status, j.views, t.name
                FROM   job_ads AS j
                LEFT JOIN towns AS t ON j.town_id=t.id
                WHERE j.status=? AND j.{search_by} LIKE ?''', (f'{Status.ACTIVE}', f'%{search}%'))

        except OperationalError:
            return BadRequest('Invalid search_by query.')

    return (JobAd.from_query_result(*row) for row in data)


def create_match_request_by_professional(professional_id: int, resume_id: int):
    # no match by skills !!!

    selected_resume: Resume
    professional = get_professional_by_id(professional_id)
    success = False

    selected_resume = get_resume_by_id(professional_id, resume_id)

    town_name = get_town_name_by_id(selected_resume.town_id)

    all_active_job_ads = search_all_active_job_ads()

    for job_ad in all_active_job_ads:
        if selected_resume.title == job_ad.title and selected_resume.min_salary <= job_ad.min_salary and town_name == job_ad.town_name:
            data = insert_query('''
            INSERT INTO match_requests(id, resume_id, job_ad_id, `match`, request_from) VALUES (?,?,?,?)''',
                                (selected_resume.id, job_ad.id, 1, professional.first_name))
            success = True
            break

    if success:
        return MatchRequestResponse(data.id, data.resume_id, data.job_ad, data.match, data.request_from)

    return NotFound('You do not have to satisfy every requirement or meet every qualification listed!')


def get_professional_match_request_by_resume_id(resume_id: int):
    try:
        data = read_query('''
                    SELECT m_r.id,m_r.resume_id, m_r.job_ad_id, m_r.match, m_r.request_from FROM match_requests AS m_r
                    WHERE m_r.resume_id=?''', (resume_id,))
    except OperationalError:
        return NotFound('You do not have to satisfy every requirement or meet every qualification listed!')

    return MatchRequestResponse(data.id, data.resume_id, data.job_ad_id,
                                data.match, data.request_from)


def get_match_request_by_id(match_request_id: int):
    try:
        data = read_query('''
        SELECT m_r.id,m_r.resume_id,m_r.job_ad_id,m_r.`match`,m_r.request_from FROM match_requests AS m_r
        WHERE m_r.id=?''', (match_request_id,))
    except OperationalError:
        return NotFound(f'Match request with id {match_request_id} not found!')

    return MatchRequestResponse(data.id, data.resume_id, data.job_ad_id,
                                data.match, data.request_from)


def get_list_of_matches(id: int):
    return None


def sort(professionals, reverse):
    return None
