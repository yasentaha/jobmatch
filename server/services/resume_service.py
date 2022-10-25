from server.data.database import read_query
from server.data.models import Resume, Status


def get_all_active_resumes_by_id(id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description,r.min_salary,r.max_salary,r.work_place,r.status,r.town_id,r.main
                    FROM resumes as r
                    WHERE r.id=? AND r.status=?''', (id, f'%{Status.ACTIVE}%'))

    return (Resume(id=id, title=title, description=description, min_salary=min_salary, max_salary=max_salary,
                   work_place=work_place, status=status, town_id=town_id, main=main)
            for id, title, description, min_salary, max_salary, work_place, status, town_id, main in data)

def get_all_archived_resumes_by_id(id: int):
    data = read_query(
        '''SELECT r.id, r.title, r.description,r.min_salary,r.max_salary,r.work_place,r.status,r.town_id,r.main
                    FROM resumes as r
                    WHERE r.id=? AND r.status=?''', (id, f'%{Status.ARCHIVED}%'))

    return (Resume(id=id, title=title, description=description, min_salary=min_salary, max_salary=max_salary,
                   work_place=work_place, status=status, town_id=town_id, main=main)
            for id, title, description, min_salary, max_salary, work_place, status, town_id, main in data)