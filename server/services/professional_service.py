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

def get_professional_info_by_id(id: int):
    data = read_query(
        '''SELECT p.user_id, p.first_name, p.last_name, p.summary, p.busy
                FROM professionals as p
            WHERE p.user_id=?''', (id,))

    return (ProfessionalInfo(id=user_id,first_name=first_name,last_name=last_name, summary=summary,
                              busy=busy)
            for user_id, first_name,last_name,summary, busy in data)

def edit_professional_info(id:int,professional_info: ProfessionalInfo,update_data=None):
    if update_data is None:
        update_data = update_query

    update_data(
        '''UPDATE professionals
            SET first_name = ? ,last_name=?,summary=?,busy=?
             WHERE user_id = ?''', (professional_info.first_name, professional_info.last_name,
                                    professional_info.summary,professional_info.busy,
                                    id))

    return ProfessionalInfo(user_id=professional_info.id,first_name=professional_info.first_name,
                             last_name=professional_info.last_name,
                             summary=professional_info.summary,busy=professional_info.busy)


def sort(professionals: list[Professional], *, attribute='name', reverse=False):

    if attribute == 'name':
        def sort_fn(p: Professional): return p.first_name
    else:
        def sort_fn(p: Professional): return p.id

    return sorted(professionals, key=sort_fn, reverse=reverse)