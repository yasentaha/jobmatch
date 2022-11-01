from server.common.responses import Success
from server.data.database import read_query, insert_query, update_query, read_query_single_element
from server.data.models import Resume, Status, Skill, CreateResume


def all_active_resumes_without_job_salary_and_description(id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, r.work_place, r.status, r.town_id,r.main 
                FROM resumes as r
                WHERE r.professional_id=? AND r.status=?''', (id, f'%{Status.ACTIVE}%'))

    return (Resume(id=id, title=title, description='None', min_salary=0, max_salary=0,
                   work_place=work_place, status=status, town_id=town_id, main=main)
            for id, title, description, min_salary, max_salary, work_place, status, town_id, main in data)


def all_hidden_resumes(id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, r.work_place, r.status, r.town_id,r.main 
                FROM resumes as r
                WHERE r.professional_id=? AND r.status=?''', (id, f'%{Status.HIDDEN}%'))

    return (Resume(id=id, title=title, description=description, min_salary=min_salary, max_salary=max_salary,
                   work_place=work_place, status=status, town_id=town_id, main=main)
            for id, title, description, min_salary, max_salary, work_place, status, town_id, main in data)


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
        (create_resume.id, skill.id, create_resume.stars)
    )

    return Success(f'Resume with title {create_resume.title} was created!')


def get_resume_by_id(professional_id: int, resume_id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description, r.min_salary, r.max_salary, r.work_place, r.status, r.town_id,r.main 
                    FROM resumes as r
                    WHERE r.professional_id=? AND r.id=?''', (professional_id, resume_id))

    return Resume(id=data.id, title=data.title, description=data.description, min_salary=data.min_salary,
                  max_salary=data.max_salary, work_place=data.work_place, status=data.status,
                  town_id=data.town_id, main=data.main)


def edit_resume_by_professional_id_and_resume_id(professional_id: int, resume_id: int, resume: Resume,
                                                 update_data=None):
    if update_data is None:
        update_data = update_query

    update_data(
        '''UPDATE resumes
            SET title=?, description=?, min_salary=?, max_salary=?,work_place=?,status=?,town_id=?,main=?
             WHERE professional_id = ? AND resumes.id=?''',
        (resume.title, resume.description, resume.min_salary, resume.max_salary, resume.work_place,
         resume.status, resume.town_id, resume.main, professional_id, resume_id))

    return Resume(id=update_data.id, title=update_data.title, description=update_data.description,
                  min_salary=update_data.min_salary, max_salary=update_data.max_salary,
                  work_place=update_data.work_place, status=update_data.status,
                  town_id=update_data.town_id, main=update_data.main)


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


def get_all_resume_skills_by_id(resume_id: int):
    data = read_query(
        '''SELECT s.id, s.name,r_s.stars
                 FROM skills as s 
                 RIGHT JOIN 
                resumes_skills as r_s
                ON s.id=r_s.skill_id
                    WHERE r_s.resume_id=?''', (resume_id,))
    return (Skill(id=id, name=name, stars=stars)
            for id, name, stars in data)


def get_town_name_by_id(town_id: int):
    data = read_query('''SELECT t.name
    FROM towns as t
    WHERE t.id=?''', (town_id,))

    return data


def get_town_id_by_name(town_name: str) -> int:
    town_id = (read_query_single_element('SELECT id from towns where name = ?', (town_name,)))[0]

    return town_id


def get_number_of_all_active_resumes(professional_id: int):
    data = read_query(
        '''SELECT r.id FROM RESUMES
        WHERE r.professional_id=? AND r.status=?''', (professional_id, f'%{Status.ACTIVE}%',))

    return len(data)


def add_skill(professional_id: int, resume_id: int, skill: Skill):
    return None


def if_skill_not_exist_return_true_else_false(professional_id: int, resume_id: int, skill: Skill):
    data = read_query(
        '''SELECT s.name FROM resumes as r
        LEFT JOIN resumes_skills rs on r.id = rs.resume_id
        LEFT JOIN skills s on rs.skill_id = s.id
        WHERE r.professional_id=? AND r.id=?''', (professional_id, resume_id))

    for name in data:
        if skill.name.lower() == name.lower():
            return False

    return True

def get_list_of_matches(id: int):
    return None


def sort(professionals, reverse):
    return None
