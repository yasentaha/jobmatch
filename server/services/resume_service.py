from server.data.database import read_query
from server.data.models import Resume, Status, Skill


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


def get_number_of_all_active_resumes_by_company():
    data = read_query(
        '''SELECT r.id FROM RESUMES
        WHERE r.status=?''',(f'%{Status.ACTIVE}%',))

    return len(data)