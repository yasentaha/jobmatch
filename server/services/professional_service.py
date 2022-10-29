from server.data.database import read_query, insert_query
from server.data.models import Professional, Resume, Status


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


def get_by_id(id: int):
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

