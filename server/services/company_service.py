from server.data.database import read_query, update_query, read_query_single_element
from server.data.models import Company, Role
from mariadb import DataError



def get_company_by_id(id: int, read_data = read_query):
    
    data = read_data(
        '''SELECT u.id,u.user_name,c.company_name,c.description,u.email,u.phone,u.address,
                t.name,c.successful_matches
        FROM 
            users as u
        LEFT JOIN
            companies AS c ON c.user_id=u.id
        LEFT JOIN
            towns AS t ON u.town_id=t.id
        WHERE u.id=? and u.role=?''', (id, Role.COMPANY))

    return next((Company.from_query_result(*row) for row in data), None)

def get_all_companies(search: str | None = None, search_by: str | None = None):
    if search is None:
        data = read_query(
            '''SELECT u.id,u.user_name,c.company_name,c.description,u.email,u.phone,u.address,
                t.name,c.successful_matches
                FROM 
                    users as u
                LEFT JOIN
                    companies AS c ON c.user_id=u.id
                LEFT JOIN
                    towns AS t ON u.town_id=t.id
                WHERE u.role=?''',(Role.COMPANY,))
    else:
        if search_by != 'town_name':
            data = read_query(
                f'''SELECT u.id,u.user_name,c.company_name,c.description,u.email,u.phone,u.address,
                    t.name,c.successful_matches
                FROM 
                        users as u
                LEFT JOIN
                    companies AS c ON c.user_id=u.id
                LEFT JOIN
                    towns AS t ON u.town_id=t.id
                WHERE u.role=? AND c.{search_by} LIKE ?''', (Role.COMPANY,f'%{search}%'))
    
        else:
            data = read_query(
                f'''SELECT u.id,u.user_name,c.company_name,c.description,u.email,u.phone,u.address,
                    t.name,c.successful_matches
                FROM 
                    users as u
                LEFT JOIN
                    companies AS c ON c.user_id=u.id
                LEFT JOIN
                    towns AS t ON u.town_id=t.id
                WHERE u.role=? AND t.name LIKE ?''', (f'{Role.COMPANY}',f'%{search}%'))
    if not data:
        return None
        
    return (Company.from_query_result(*row) for row in data)


def edit_company(id:int, company:Company, update_data=None):
    if update_data is None:
        update_data = update_query
    try:
        update_data(
        '''UPDATE companies
                SET company_name = ? ,description = ?, successful_matches = ?
                WHERE user_id = ?''', (company.company_name, company.description,
                                        company.successful_matches,id))

        return True
    
    except DataError:
        return False


def update_successful_matches(id: int):
    current_company_matches = (read_query_single_element('SELECT successful_matches from companies where user_id=?', (id,)))[0]

    updated_company_matches = current_company_matches + 1

    update_query('UPDATE companies SET successful_matches=? WHERE user_id=?', (updated_company_matches, id))



def sort(companies: list[Company], *, attribute='name', reverse=False):

    if attribute == 'name':
        def sort_fn(c: Company): return c.company_name
    else:
        def sort_fn(c: Company): return c.id

    return sorted(companies, key=sort_fn, reverse=reverse)