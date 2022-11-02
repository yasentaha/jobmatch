from server.data.database import read_query, update_query, insert_query, read_query_single_element
from server.data.models import Company, JobAd, Status, Skill


def create(job_ad: JobAd, company: Company) -> JobAd:
    generated_id = insert_query(
        '''INSERT INTO job_ads(title, description, min_salary, max_salary, work_place, status, town_id, company_id, views) VALUES(?,?,?,?,?,?,?,?,?)''',
        (job_ad.title, job_ad.description, job_ad.min_salary, job_ad.max_salary, job_ad.work_place, job_ad.status, job_ad.town_name, company.id, 0)
    )
    job_ad.id = generated_id

    new_job_ad= get_job_ad_by_id(company.id,generated_id)

    return new_job_ad

def get_job_ad_by_id(company_id:int, job_id: int):
    
    data = read_query(
        '''SELECT j.id, j.title, j.description, j.min_salary, j.max_salary, j.work_place, j.status, j.views, t.name
        FROM   
            job_ads AS j
        LEFT JOIN
            towns AS t ON j.town_id=t.id
        WHERE company_id=? AND j.id=?''', (company_id, job_id))

    return next((JobAd.from_query_result(*row) for row in data), None)

def get_all_active_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, f'%{Status.ACTIVE}%'))
    if data:
        return (id for id in data)
    else:
        return [0]

def get_all_archived_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, f'%{Status.ARCHIVED}%'))

    if data:
        return (id for id in data)
    else:
        return [0]

def get_number_of_all_active_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, f'%{Status.ACTIVE}%'))
    
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

def get_list_of_matches(id: int):
    return None