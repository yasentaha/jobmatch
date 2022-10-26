from server.data.database import read_query, update_query, insert_query, read_query_single_element
from server.data.models import Company, JobAd, Status



def get_company_by_id(id: int):
    
    data = read_query(
        '''SELECT c.id, c.user_name, c.password,c.company_name,p.description,c.logo_url,c.successful_matches
        ct.email,ct.phone,ct.address,t.name
        FROM 
            companies as c
        LEFT JOIN
            contacts AS ct ON c.contact_id=ct.id
        LEFT JOIN
            towns AS t ON ct.town_id=t.id
        WHERE c.id=?''', (id,))

    return (Company.from_query_result(*row) for row in data)

def get_all_companies(search: str = None):
    
    if search is None:
        data = read_query(
            '''SELECT c.id, c.user_name, c.password,c.company_name,p.description,c.logo_url,c.successful_matches
        ct.email,ct.phone,ct.address,t.name
        FROM 
            companies as c
        LEFT JOIN
            contacts AS ct ON c.contact_id=ct.id
        LEFT JOIN
            towns AS t ON ct.town_id=t.id
        WHERE c.id=?''')

    else:
        data = read_query(
            '''SELECT c.id, c.user_name, c.password,c.company_name,p.description,c.logo_url,c.successful_matches
        ct.email,ct.phone,ct.address,t.name
        FROM 
            companies as c
        LEFT JOIN
            contacts AS ct ON c.contact_id=ct.id
        LEFT JOIN
            towns AS t ON ct.town_id=t.id
        WHERE c.company_name LIKE ?''', (f'%{search}%',))

    return (Company.from_query_result(*row) for row in data)

def update_successful_matches(id: int):
    current_company_matches = (read_query_single_element('SELECT successful_matches from companies where id=?', (id,)))[0]

    updated_company_matches = current_company_matches + 1

    update_query('UPDATE companies SET successful_matches=? WHERE id=?', (updated_company_matches, id))

