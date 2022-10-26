from server.data.database import read_query, insert_query
from server.data.models import Professional, Resume, Status


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT u.id, u.user_name, u.password,u.role,p.first_name,p.last_name,p.summary,p.busy,p.image_url,
            c.email,c.phone,c.address,t.id
                FROM users as u
                LEFT JOIN professionals as p 
                ON u.id= p.user_id
                LEFT JOIN contacts as c
                ON p.contact_id=c.id
                LEFT JOIN towns as t
                ON c.town_id=t.id''')

    else:
        data = read_query(
            '''SELECT u.id, u.user_name, u.password,u.role,p.first_name,p.last_name,p.summary,p.busy,p.image_url,
            c.email,c.phone,c.address,t.id
                FROM users as u
                LEFT JOIN professionals as p 
                ON u.id= p.user_id
                LEFT JOIN contacts as c
                ON p.contact_id=c.id
                LEFT JOIN towns as t
                ON c.town_id=t.id
               WHERE p.first_name LIKE ?''', (f'%{search}%',))

    return (Professional.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query(
        '''SELECT u.id, u.user_name, u.password,u.role,p.first_name,p.last_name,p.summary,p.busy,p.image_url,
            c.email,c.phone,c.address,t.id
                FROM users as u
                LEFT JOIN professionals as p 
                ON u.id= p.user_id
                LEFT JOIN contacts as c
                ON p.contact_id=c.id
                LEFT JOIN towns as t
                ON c.town_id=t.id
            WHERE u.id=?''', (id,))

    return (Professional.from_query_result(*row) for row in data)

#
# def create(professional: Professional, insert_data=None):
#     user=get_user_or
#     if insert_data is None:
#         insert_data = insert_query
#
#     professional_generated_id = insert_data(
#         'INSERT INTO professionals(user_name,password,first_name,last_name,summary,busy,image_url,email,phone,address,town_id) values(?,?,?,?,?,?,?,?,?,?,?)',
#         (professional.user_name, password,))
#
#     professional_generated_id.id = professional_generated_id
#
#     return
