from server.data.database import read_query, update_query, insert_query, read_query_single_element
from server.data.models import Company, JobAd, Status



def get_all_active_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, f'%{Status.ACTIVE}%'))
    if data:
        return (id for id in data)
    else:
        return [0]

def get_all_archived_job_ads_by_company_id(company_id: int):
    data = read_query(
        '''SELECT j.id
                FROM job_ads as j
                    WHERE j.company_id=? AND j.status=?''', (company_id, f'%{Status.ARCHIVED}%'))

    if data:
        return (id for id in data)
    else:
        return [0]