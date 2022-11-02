from server.data.database import read_query, update_query, insert_query, read_query_single_element
from server.data.models import Company, CompanyInfo, JobAd, Status



def get_company_by_id(id: int):
    
    data = read_query(
        '''SELECT u.id,u.user_name,c.company_name,c.description,u.email,u.phone,u.address,
                t.name,c.successful_matches
        FROM 
            users as u
        LEFT JOIN
            companies AS c ON c.user_id=u.id
        LEFT JOIN
            towns AS t ON u.town_id=t.id
        WHERE u.id=?''', (id,))

    return next((Company.from_query_result(*row) for row in data), None)

def get_all_companies(search: str = None):
    
    if search is None:
        data = read_query(
        '''SELECT u.id, u.user_name,c.company_name,c.description,u.email,u.phone,u.address,
                t.name,c.successful_matches
        FROM 
            users as u
        LEFT JOIN
            companies AS c ON c.users_id=u.id
        LEFT JOIN
            towns AS t ON u.town_id=t.id
        WHERE u.id=?''')

    else:
        data = read_query(
        '''SELECT u.id, u.user_name,c.company_name,c.description,u.email,u.phone,u.address,
                    t.name,c.successful_matches
        FROM 
            users as u
        LEFT JOIN
            companies AS c ON c.users_id=u.id
        LEFT JOIN
            towns AS t ON u.town_id=t.id
        WHERE c.company_name LIKE ?''', (f'%{search}%',))

    return (Company.from_query_result(*row) for row in data)

def get_number_of_all_active_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, f'%{Status.ACTIVE}%'))
    
    return len(data)

def get_company_info_by_id(id: int):
    data = read_query(
        '''SELECT u.id, u.email,u.phone,u.address,
                c.company_name,c.description,c.successful_matches,t.name
        FROM 
            users as u
        LEFT JOIN
            companies AS c ON c.users_id=u.id
        LEFT JOIN
            towns AS t ON u.town_id=t.id
        WHERE u.id=?''', (id,))

    return next((CompanyInfo.from_query_result(*row) for row in data), None)

# def edit_company_info(id:int ,company_info: CompanyInfo,update_data=None):
#     if update_data is None:
#         update_data = update_query

def update_successful_matches(id: int):
    current_company_matches = (read_query_single_element('SELECT successful_matches from companies where id=?', (id,)))[0]

    updated_company_matches = current_company_matches + 1

    update_query('UPDATE companies SET successful_matches=? WHERE id=?', (updated_company_matches, id))

def sort(companies: list[Company], *, attribute='name', reverse=False):

    if attribute == 'name':
        def sort_fn(c: Company): return c.company_name
    else:
        def sort_fn(c: Company): return c.id

    return sorted(companies, key=sort_fn, reverse=reverse)