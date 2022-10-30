from server.data.database import read_query, insert_query, update_query
from server.data.models import Resume, Status, Skill


def create(resume: Resume, insert_data=None):
    if insert_data is None:
        insert_data = insert_query

    generated_id = insert_data(
        'insert into resumes(title, description, min_salary, max_salary, work_place, status, town_id,main) values(?,?,?,?,?,?,?)',
        (resume.title, resume.description, resume.min_salary, resume.max_salary, resume.work_place, resume.status,
         resume.town_id, resume.main))

    resume.id = generated_id

    return resume


def get_resume_by_id(professional_id: int, resume_id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, r.work_place, r.status, r.town_id,r.main 
                    FROM resumes as r
                    WHERE r.professional_id=? AND r.id=?''', (professional_id, resume_id))

    return (Resume(id=id, title=title, description=description, min_salary=min_salary, max_salary=max_salary,
                   work_place=work_place, status=status, town_id=town_id, main=main)
            for id, title, description, min_salary, max_salary, work_place, status, town_id, main in data)

def edit_resume_by_id(professional_id: int, resume_id: int, title: str, description: str, min_salary: int,
                      max_salary: int, work_place: int, status: str, town_id: int, main: int, update_data=None):
    if update_data is None:
        update_data = update_query

    update_data(
        '''UPDATE resumes
            SET title=?, description=?, min_salary=?, max_salary=?,work_place=?,status=?,town_id=?,main=?
             WHERE professional_id = ? AND resumes.id=?''',
        (title, description, min_salary, max_salary, work_place,
         status, town_id, main, professional_id, resume_id))

    return (Resume(id=resume_id, title=title, description=description, min_salary=min_salary,
                   max_salary=max_salary, work_place=work_place, status=status, town_id=town_id, main=main))


def get_all_active_resumes_by_professional_id(professional_id: int):
    data = read_query(
        '''SELECT r.id
                    FROM resumes as r
                    WHERE r.professional_id=? AND r.status=?''', (professional_id, f'%{Status.ACTIVE}%'))
    if data:
        return (id for id in data)
    else:
        return [0]


def get_all_archived_resumes_by_professional_id(professional_id: int):
    data = read_query(
        '''SELECT r.id
                    FROM resumes as r
                    WHERE r.professional_id=? AND r.status=?''', (professional_id, f'%{Status.ARCHIVED}%'))

    if data:
        return (id for id in data)
    else:
        return [0]


def get_all_skills_resume_by_id(resume_id: int):
    data = read_query(
        '''SELECT s.id, s.name,r_s.stars
                 FROM skills as s 
                 RIGHT JOIN 
                resumes_skills as r_s
                ON s.id=r_s.skill_id
                    WHERE r_s.resume_id=?''', (resume_id,))
    return (Skill(id=id, name=name, stars=stars)
            for id, name, stars in data)


def get_number_of_all_active_resumes_by_company(professional_id: int):
    data = read_query(
        '''SELECT r.id FROM RESUMES
        WHERE r.professional_id=? AND r.status=?''', (professional_id, f'%{Status.ACTIVE}%',))

    return len(data)


def get_list_of_matches(id:int):
    return None