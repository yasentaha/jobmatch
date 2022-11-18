from server.common.responses import Success, BadRequest
from server.data.models import Resume, Status, Skill, CreateResume, JobAd, ResumeWithoutDescriptionAndSalary
from server.data.database import read_query, insert_query, update_query, read_query_single_element
from server.services.job_ad_service import get_job_ad_by_id
from server.common.validations_and_methods import (parse_salary_range,
                                                   parse_skills,
                                                   salary_range_threshold,
                                                   return_skills_with_ids,
                                                   get_town_id_by_name)


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
            data = get_active_by_salary_range(search, threshold)

        elif search_by == 'location':
            data = get_active_by_location(search)
        
        elif search_by == 'skills':
            data = get_active_by_skills(search, combined)

        elif search_by == 'job_ad':
            job_ad = get_job_ad_by_id(search)
            skill_names = tuple(skill.name for skill in job_ad.skill_requirements)

            if job_ad.work_place == "Onsite":
                data = get_active_by_job_ad_onsite(job_ad, skill_names)

            elif job_ad.work_place == "Remote":
                data = get_active_by_job_ad_remote(job_ad, skill_names)
            else:
                data = get_active_by_job_ad_hybrid(job_ad, skill_names)
    
    if not data:
        return None

    resumes = [Resume.from_query_result(*row) for row in data]

    for resume in resumes:
        resume.skills = get_all_resume_skills_by_id(resume.id)

    return resumes

def get_active_by_salary_range(salary_range: str, threshold: int | None):
    if not threshold:
        min_salary, max_salary = parse_salary_range(salary_range)
    else:
        min_salary, max_salary = salary_range_threshold(parse_salary_range(salary_range),int(threshold))
    
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
    return data

def get_active_by_location(location:str):
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
                    AND r.work_place != "Onsite"''',(f'%{location}%',))
    return data

def get_active_by_skills(skills:str, combined:bool):
    skills_tuple = parse_skills(skills)
    count = len(skills_tuple)
    if combined == True:
        if not isinstance(skills_tuple, tuple):
            count = 1
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
                        HAVING count(distinct s.name) = {count}''')
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
    return data

def get_active_by_job_ad_onsite(job_ad: JobAd, skill_names:tuple):
    data = read_query(f'''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                    r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    LEFT JOIN
                    resumes_skills AS r_s ON r.id = r_s.resume_id
                    LEFT JOIN
                    skills AS s ON r_s.skill_id = s.id
                    WHERE r.status='Active'
                    AND r.work_place="Onsite"
                    AND t.name=?
                    AND r.min_salary >=?
                    AND r.max_salary <=?
                    AND s.name IN {skill_names}
                    GROUP by r.id
                    HAVING count(distinct s.name) = {len(skill_names)}''', (job_ad.town_name, job_ad.min_salary, job_ad.max_salary))
    return data

def get_active_by_job_ad_remote(job_ad: JobAd, skill_names:tuple):
    data = read_query(f'''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                    r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    LEFT JOIN
                    resumes_skills AS r_s ON r.id = r_s.resume_id
                    LEFT JOIN
                    skills AS s ON r_s.skill_id = s.id
                    WHERE r.status='Active'
                    AND r.work_place!="Onsite"
                    AND r.min_salary >=?
                    AND r.max_salary <=?
                    AND s.name IN {skill_names}
                    GROUP by r.id
                    HAVING count(distinct s.name) = {len(skill_names)}''', (job_ad.min_salary, job_ad.max_salary))
    return data

def get_active_by_job_ad_hybrid(job_ad: JobAd, skill_names:tuple):
    data = read_query(f'''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                     r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    LEFT JOIN
                    resumes_skills AS r_s ON r.id = r_s.resume_id
                    LEFT JOIN
                    skills AS s ON r_s.skill_id = s.id
                    WHERE r.status="Active"
                    AND r.work_place != "Remote"
                    AND t.name = ?
                    AND r.min_salary >=?
                    AND r.max_salary <=?
                    AND s.name IN {skill_names}
                    GROUP by r.id
                    HAVING count(distinct s.name) = {len(skill_names)}

                    UNION    
                        
                    SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                    r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    LEFT JOIN
                    resumes_skills AS r_s ON r.id = r_s.resume_id
                    LEFT JOIN
                    skills AS s ON r_s.skill_id = s.id
                    WHERE r.status="Active"
                    AND r.work_place != "Onsite"
                    AND t.name != ?
                    AND r.min_salary >=?
                    AND r.max_salary <=?
                    AND s.name IN {skill_names}
                    GROUP by r.id
                    HAVING count(distinct s.name) = {len(skill_names)}    
                    ''', (job_ad.town_name, job_ad.min_salary, job_ad.max_salary,job_ad.town_name, job_ad.min_salary, job_ad.max_salary))
    return data



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
    if resume:
        resume.skills = get_all_resume_skills_by_id(resume.id)
        return resume
    else:
        return None


def edit_resume_by_id(resume_id: int, new_resume: Resume, update_data=None):
    if update_data is None:
        update_data = update_query

    town_id = get_town_id_by_name(new_resume.town_name)

    update_data(
        '''UPDATE resumes
            SET title=?, description=?, min_salary=?, max_salary=?,work_place=?,status=?,town_id=?,main=?
             WHERE id=?''',
        (new_resume.title, new_resume.description, new_resume.min_salary, new_resume.max_salary, new_resume.work_place,
         new_resume.status, town_id, new_resume.main, resume_id))

    old_resume_skills = get_all_resume_skills_by_id(resume_id)

    new_resume_skills = return_skills_with_ids(new_resume.skills)

    if new_resume_skills != old_resume_skills:
        delete_all_skills_from_resume(resume_id)
        [add_skill_to_resume(resume_id, skill)  for skill in new_resume_skills]

    return get_resume_by_id(resume_id)

def make_resume_matched(resume_id:int, update_data=update_query):
    return update_data('''UPDATE resumes
                        SET status=?
                        WHERE id= ?''', (Status.MATCHED, resume_id))

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

def get_all_resumes_by_professional_id(professional_id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, 
                    r.work_place, r.main, r.status, t.name, r.professional_id
                    FROM resumes as r
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE r.professional_id=?''', (professional_id,))
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


def get_number_of_all_active_resumes(professional_id: int):
    data = read_query(
        '''SELECT r.id FROM resumes as r 
        WHERE r.professional_id=? AND r.status=?''', (professional_id, Status.ACTIVE))

    return len(data)


def add_skill_to_resume(resume_id: int, skill: Skill):
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




