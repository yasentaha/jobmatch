from server.data.models import Company, JobAd, Resume, Skill, Status
from server.common.validations_and_methods import (add_skill,
                                                   parse_salary_range,
                                                   parse_skills,
                                                   remove_under_from_skill,
                                                   salary_range_threshold,
                                                   validate_stars,
                                                   validate_work_place,
                                                   add_skills,
                                                   return_skills_with_ids,
                                                   skill_exists,
                                                   get_skill_id_by_name,
                                                   get_town_id_by_name,
                                                   get_town_name_by_id)
from server.data.database import (insert_query, 
                                  read_query,
                                  read_query_single_element, update_query)


def create_job_ad(company_id: int, job_ad: JobAd, insert_data=None):
    if insert_data is None:
        insert_data = insert_query

    town_id = get_town_id_by_name(job_ad.town_name)

    generated_job_ad_id = insert_data(
        '''INSERT INTO job_ads(title, description, min_salary, max_salary, work_place,status,town_id,company_id, views) 
        values(?,?,?,?,?,?,?,?,?)''',
        (job_ad.title, job_ad.description, job_ad.min_salary, job_ad.max_salary,
         job_ad.work_place,job_ad.status, town_id,company_id, 0))
        
    skills_with_ids = return_skills_with_ids(job_ad.skill_requirements)
    if generated_job_ad_id:
        [add_skill_to_job_ad(generated_job_ad_id, skill) for skill in skills_with_ids]

    return get_job_ad_by_id(generated_job_ad_id)

def get_job_ad_by_id(job_ad_id: int):
    
    data = read_query(
        '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, j.work_place, j.status, t.name, j.company_id, j.views
        FROM   
            job_ads AS j
        LEFT JOIN
            towns AS t ON j.town_id=t.id
        WHERE j.id=?''', (job_ad_id,))

    job_ad = next((JobAd.from_query_result(*row) for row in data), None)

    if job_ad:
        job_ad.skill_requirements = get_all_skills_for_job_ad_id(job_ad.id)
        return job_ad
    
    else:
        return None

def edit_job_ad_by_company_and_job_ad_ids(company_id: int, job_ad_id: int, new_job_ad: JobAd,
                                                 update_data=None):
    if update_data is None:
        update_data = update_query

    town_id = get_town_id_by_name(new_job_ad.town_name)

    update_data(
        '''UPDATE job_ads
            SET title=?, description=?, min_salary=?, max_salary=?,work_place=?,status=?,town_id=?
             WHERE company_id = ? AND job_ads.id=?''',
        (new_job_ad.title, new_job_ad.description, new_job_ad.min_salary, new_job_ad.max_salary, new_job_ad.work_place,
         new_job_ad.status, town_id, company_id, job_ad_id))

    old_job_ad_skill_requirements = get_all_skills_for_job_ad_id(job_ad_id)

    new_job_ad_skill_requirements = return_skills_with_ids(new_job_ad.skill_requirements)

    if new_job_ad_skill_requirements != old_job_ad_skill_requirements:
        delete_all_skills_from_job_ad(job_ad_id)
        [add_skill_to_job_ad(job_ad_id, skill)  for skill in new_job_ad_skill_requirements]

    return get_job_ad_by_id(job_ad_id)

def delete_all_skills_from_job_ad(job_ad_id:int):

    update_query('''DELETE from job_ads_skills where job_ad_id = ?''', (job_ad_id,))


def all_active_job_ads(search: str | None = None, search_by: str | None = None, threshold: int | None = None, combined: bool | None = None):
    
    if search is None:
    
        data = read_query(
        '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM job_ads as j
                    LEFT JOIN
                    towns as t
                    ON j.town_id = t.id
                    WHERE j.status=?''', (Status.ACTIVE,))


    else:
        if search_by == 'salary_range':
            data = get_all_active_by_salary_range(search, threshold)

        elif search_by == 'location':
            data = get_all_active_by_location(search)
        
        elif search_by == 'skills':
            data = get_all_active_by_skills(search, combined)

        elif search_by == 'resume':
            resume = get_resume_by_id(search)
            if not resume:
                return None
            
            skill_names = tuple(skill.name for skill in resume.skills)

            if resume.work_place == "Onsite":
                data = get_all_active_by_resume_onsite(resume, skill_names)

            elif resume.work_place == "Remote":
                data = get_all_active_by_resume_remote(resume, skill_names)
            else:
                data = get_all_active_by_resume_hybrid(resume, skill_names)
    
    if not data:
        return None

    job_ads =  [JobAd.from_query_result(*row) for row in data]

    for job_ad in job_ads:
        job_ad.skill_requirements = get_all_skills_for_job_ad_id(job_ad.id)

    return job_ads

def get_all_active_by_salary_range(salary_range: str, threshold: int | None):
    if not threshold:
        min_salary, max_salary = parse_salary_range(salary_range)
    else:
        min_salary, max_salary = salary_range_threshold(parse_salary_range(salary_range),int(threshold))
    
    data = read_query(
                '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM job_ads as j
                    LEFT JOIN
                    towns as t
                    ON j.town_id = t.id
                    WHERE j.status=?
                    AND j.min_salary >=?
                    AND j.max_salary <=?''', (Status.ACTIVE, min_salary, max_salary))
    return data

def get_all_active_by_location(location:str):
    data = read_query('''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM job_ads as j
                    LEFT JOIN
                    towns as t
                    ON j.town_id = t.id
                    WHERE j.status='Active'
                    AND t.name LIKE ?

                    UNION
                    
                    SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM job_ads as j
                    LEFT JOIN
                    towns as t
                    ON j.town_id = t.id
                    WHERE j.status='Active'
                    AND j.work_place != "Onsite"''',(f'%{location}%',))
    return data

def get_all_active_by_skills(skills:str, combined:bool):
    skills_tuple = parse_skills(skills)
    if combined == True:
        data = read_query(f'''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                        j.work_place, j.status, t.name, j.company_id, j.views
                        FROM 
                        job_ads as j
                        LEFT JOIN
                        towns AS t ON j.town_id = t.id
                        LEFT JOIN
                        job_ads_skills AS j_s ON j.id = j_s.job_ad_id
                        LEFT JOIN
                        skills AS s ON j_s.skill_id = s.id
                        WHERE
                        j.status = "Active"
                        AND s.name IN {skills_tuple}
                        GROUP by j.id
                        HAVING count(distinct s.name) = {len(skills_tuple)}''')
    else:
        data = read_query(f'''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                        j.work_place, j.status, t.name, j.company_id, j.views
                        FROM 
                        job_ads as j
                        LEFT JOIN
                        towns AS t ON j.town_id = t.id
                        LEFT JOIN
                        job_ads_skills AS j_s ON j.id = j_s.job_ad_id
                        LEFT JOIN
                        skills AS s ON j_s.skill_id = s.id
                        WHERE
                        j.status = "Active"
                        AND s.name IN {skills_tuple}''')
    return data

def get_all_active_by_resume_onsite(resume: Resume, skill_names:tuple):
    data = read_query(f'''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM 
                    job_ads as j
                    LEFT JOIN
                    towns AS t ON j.town_id = t.id
                    LEFT JOIN
                    job_ads_skills AS j_s ON j.id = j_s.job_ad_id
                    LEFT JOIN
                    skills AS s ON j_s.skill_id = s.id
                    WHERE j.status='Active'
                    AND j.work_place="Onsite"
                    AND t.name=?
                    AND j.min_salary >=?
                    AND j.max_salary <=?
                    AND s.name IN {skill_names}
                    GROUP by j.id
                    HAVING count(distinct s.name) = {len(skill_names)}''', (resume.town_name, resume.min_salary, resume.max_salary))
    return data

def get_all_active_by_resume_remote(resume: Resume, skill_names:tuple):
    data = read_query(f'''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM 
                    job_ads as j
                    LEFT JOIN
                    towns AS t ON j.town_id = t.id
                    LEFT JOIN
                    job_ads_skills AS j_s ON j.id = j_s.job_ad_id
                    LEFT JOIN
                    skills AS s ON j_s.skill_id = s.id
                    WHERE j.status='Active'
                    AND j.work_place!="Onsite"
                    AND j.min_salary >=?
                    AND j.max_salary <=?
                    AND s.name IN {skill_names}
                    GROUP by j.id
                    HAVING count(distinct s.name) = {len(skill_names)}''', (resume.min_salary, resume.max_salary))
    return data

def get_all_active_by_resume_hybrid(resume: Resume, skill_names:tuple):
    data = read_query(f'''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM 
                    job_ads as j
                    LEFT JOIN
                    towns AS t ON j.town_id = t.id
                    LEFT JOIN
                    job_ads_skills AS j_s ON j.id = j_s.job_ad_id
                    LEFT JOIN
                    skills AS s ON j_s.skill_id = s.id
                    WHERE j.status="Active"
                    AND j.work_place != "Remote"
                    AND t.name = ?
                    AND j.min_salary >=?
                    AND j.max_salary <=?
                    AND s.name IN {skill_names}
                    GROUP by j.id
                    HAVING count(distinct s.name) = {len(skill_names)}

                    UNION    
                        
                    SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM 
                    job_ads as j
                    LEFT JOIN
                    towns AS t ON j.town_id = t.id
                    LEFT JOIN
                    job_ads_skills AS j_s ON j.id = j_s.job_ad_id
                    LEFT JOIN
                    skills AS s ON j_s.skill_id = s.id
                    WHERE j.status="Active"
                    AND j.work_place != "Onsite"
                    AND t.name != ?
                    AND j.min_salary >=?
                    AND j.max_salary <=?
                    AND s.name IN {skill_names}
                    GROUP by j.id
                    HAVING count(distinct s.name) = {len(skill_names)}    
                    ''', (resume.town_name, resume.min_salary, resume.max_salary,resume.town_name, resume.min_salary, resume.max_salary))
    return data



def get_all_active_job_ads_by_company_id(company_id: int):
    
    data = read_query(
        '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM job_ads AS j
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE j.company_id=? AND j.status=?''', (company_id, Status.ACTIVE))
    if data:
        return (JobAd.from_query_result(*row) for row in data)
    else:
        return None

def get_all_archived_job_ads_by_company_id(company_id: int):
    
    data = read_query(
        '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, 
                    j.work_place, j.status, t.name, j.company_id, j.views
                    FROM job_ads AS j
                    LEFT JOIN
                    towns as t
                    ON r.town_id = t.id
                    WHERE j.company_id=? AND j.status=?''', (company_id, Status.ARCHIVED))
    if data:
        return (JobAd.from_query_result(*row) for row in data)
    else:
        return None

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
                    WHERE j_s.job_ad_id=?''', (job_ad_id,))
    return [Skill(id=id, name=name, stars=stars)
            for id, name, stars in data]

def update_job_ads_views(id: int):
    current_job_ads_view = (read_query_single_element('SELECT views from job_ads where id=?', (id,)))[0]

    updated_job_ads_view = current_job_ads_view + 1

    update_query('UPDATE job_ads SET views=? WHERE id=?', (updated_job_ads_view, id))


def add_skill_to_job_ad(job_ad_id: int, skill: Skill):

    insert_query(
        '''INSERT INTO job_ads_skills(job_ad_id, skill_id, stars) VALUES (?,?,?)''',
        (job_ad_id, skill.id, skill.stars))

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

def get_all_resume_skills_by_id(resume_id: int):
    data = read_query(
        '''SELECT s.id, s.name,r_s.stars
                 FROM skills as s 
                 RIGHT JOIN 
                resumes_skills as r_s
                ON s.id=r_s.skill_id
                    WHERE r_s.resume_id=?''', (resume_id,))
    return [Skill.from_query_result(*row) for row in data]

def get_list_of_matches(id: int):
    ...