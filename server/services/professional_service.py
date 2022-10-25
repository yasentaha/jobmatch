from server.data.database import read_query
from server.data.models import Professional


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT p.id, p.user_name, p.password,p.role,p.first_name,p.last_name,p.summary,p.busy,p.image_url,
            c.email,c.phone,c.address,c.town_id
                FROM professionals as p
                LEFT JOIN
                contacts as c
                ON p.contact_id=c.id''')

    else:
        data = read_query(
            '''SELECT p.id, p.user_name, p.password,p.role,p.first_name,p.last_name,p.summary,p.busy,p.image_url,
            c.email,c.phone,c.address,c.town_id
                FROM professionals as p
                LEFT JOIN
                contacts as c
                ON p.contact_id=c.id
               WHERE p.first_name LIKE ?''', (f'%{search}%',))

    return (Professional.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query(
        '''SELECT p.id, p.user_name, p.password,p.role,p.first_name,p.last_name,p.summary,p.busy,p.image_url,
        c.email,c.phone,c.address,c.town_id
            FROM professionals as p
            LEFT JOIN
            contacts as c
            ON p.contact_id=c.id
            WHERE p.id=?'''(id,))

    return (Professional.from_query_result(*row) for row in data)

def get_all_active_resumes_by_id(id:int):
    pass