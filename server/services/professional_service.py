from server.data.database import read_query, insert_query, update_query
from server.data.models import Professional, Resume, Status, ProfessionalInfo


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT u.id, u.user_name,u.email,u.phone,u.address,t.id,
            p.first_name,p.last_name,p.summary,p.busy
                FROM users as u
                LEFT JOIN professionals as p 
                ON u.id= p.user_id
                LEFT JOIN towns as t
                ON t.id=u.town_id''')

    else:
        data = read_query(
            '''SELECT u.id, u.user_name,u.email,u.phone,u.address,t.id,
            p.first_name,p.last_name,p.summary,p.busy
                FROM users as u
                LEFT JOIN professionals as p 
                ON u.id= p.user_id
                LEFT JOIN towns as t
                ON t.id=u.town_id
               WHERE p.first_name LIKE ?''', (f'%{search}%',))

    return (Professional.from_query_result(*row) for row in data)


def get_professional_by_id(id: int):
    data = read_query(
        '''SELECT u.id, u.user_name,u.email,u.phone,u.address,t.id,
            p.first_name,p.last_name,p.summary,p.busy
                FROM users as u
                LEFT JOIN professionals as p 
                ON u.id= p.user_id
                LEFT JOIN towns as t
                ON t.id=u.town_id
            WHERE u.id=?''', (id,))

    return (Professional.from_query_result(*row) for row in data)


def edit_professional_info(professional_info: ProfessionalInfo, first_name: str, last_name: str,
                           summary: str | None, busy: int, update_data=None):
    if update_data is None:
        update_data = update_query

    update_data(
        '''UPDATE professionals
            SET first_name = ? ,last_name=?,summary=?,busy=?
             WHERE user_id = ?''', (first_name, last_name,summary,busy,professional_info.id))

    return (ProfessionalInfo(user_id=professional_info.id,first_name=first_name,last_name=last_name,
                             summary=summary,busy=busy))
