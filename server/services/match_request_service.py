from server.services.user_service import get_user_by_id
from server.data.models import MatchRequest
from server.data.database import insert_query, read_query, read_query_single_element, update_query

def initiate_match_request(requestor_id:int, resume_id:int, job_ad_id:int ,insert_data_func=insert_query):
    generated_id = insert_data_func(
            'INSERT INTO match_requests(resume_id, job_ad_id, is_match, request_from) VALUES (?,?,?,?)',
            (resume_id, job_ad_id, 0, requestor_id))
    
    return generated_id

def get_match_request_by_id(id:int, get_data_func = read_query) -> MatchRequest | None:
    data = get_data_func(
        'SELECT id, resume_id, job_ad_id, request_from FROM match_requests WHERE id = ?',
        (id,))

    return next((MatchRequest(id=id, resume_id=resume_id, job_ad_id=job_ad_id, requestor_id=requestor_id) for id, resume_id, job_ad_id, requestor_id in data), None)

def match_request_exists(id: int):
    data = read_query('''SELECT 1 FROM match_requests as mr
                     WHERE mr.id = ? 
                     AND mr.is_match = ?''', (id, 0))

    return any(data)

def match_request_by_combined_key(resume_id:int, job_ad_id:int, get_data_func = read_query):
    data = get_data_func(
        '''SELECT mr.id, mr.resume_id, mr.job_ad_id, request_from 
            FROM match_requests as mr 
            WHERE mr.resume_id = ? 
            AND mr.job_ad_id = ? 
            AND mr.is_match = ?''',
        (resume_id, job_ad_id, 0))

    return next((MatchRequest(id=id, resume_id=resume_id, job_ad_id=job_ad_id, requestor_id=requestor_id) for id, resume_id, job_ad_id, requestor_id in data), None)


def its_a_match(id: int, update_data=update_query):
    return update_data('''UPDATE match_requesets 
                    SET is_match = ?
                    WHERE id = ?''', (1,id))
    

def delete_match_request(id: int, update_data=update_query): #THIS IS FOR REJECT
    return update_data('''DELETE FROM match_requests WHERE id=?''',(id,))

def get_match_requests_by_professional_id(professional_id:int, read_data=read_query):
    data = read_data('''SELECT mr.id, mr.resume_id, mr.job_ad_id, mr.requestor_id from match_requests as mr
                        LEFT JOIN resumes as r 
                        ON mr.resume_id = r.id
                        WHERE r.professional_id =?
                        AND mr.requestor_id !=?''', (professional_id, professional_id))
    
    if data:
        return (MatchRequest.from_query_result(*row) for row in data)

def get_match_requests_by_company_id(company_id:int, read_data=read_query):
    data = read_data('''SELECT mr.id, mr.resume_id, mr.job_ad_id, mr.requestor_id from match_requests as mr
                        LEFT JOIN job_ads as j 
                        ON mr.job_ad_id = j.id
                        WHERE j.company_id =?
                        AND mr.requestor_id !=?''', (company_id, company_id))
    if data:
        return (MatchRequest.from_query_result(*row) for row in data)

def professional_owns_match_request(professional_id:int, match_request_id:int, read_data=read_query):
    data = read_data('''SELECT 1 from match_requests as mr
                        LEFT JOIN resumes as r
                        ON mr.resume_id = r.id
                        WHERE mr.id = ?
                        AND r.professional_id =?''', (match_request_id, professional_id))

    return any(data)

def company_owns_match_request(company_id:int, match_request_id:int, read_data=read_query):
    data = read_data('''SELECT 1 from match_requests as mr
                        LEFT JOIN job_ads as j
                        ON mr.job_ad_id = j.id
                        WHERE mr.id = ?
                        AND j.company_id =?''', (match_request_id, company_id))

    return any(data)