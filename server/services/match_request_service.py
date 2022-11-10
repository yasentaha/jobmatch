from server.services.user_service import get_user_by_id
from server.data.models import MatchRequest, MatchRequestResponse
from server.data.database import insert_query, read_query, read_query_single_element, update_query



def initiate_match_request(requestor_id:int, resume_id:int, job_ad_id:int ,insert_data_func=insert_query):
    generated_id = insert_data_func(
            'INSERT INTO match_requests(resume_id, job_ad_id, match, request_from) VALUES (?,?,?,?)',
            (resume_id, job_ad_id, 0, requestor_id))
    
    return generated_id

def get_match_request_by_id(id:int, get_data_func = read_query) -> MatchRequest | None:
    data = get_data_func(
        'SELECT id, resume_id, job_ad_id, request_from FROM match_requests WHERE id = ?',
        (id,))

    return next((MatchRequest(id=id, resume_id=resume_id, job_ad_id=job_ad_id, requestor_id=requestor_id) for id, resume_id, job_ad_id, requestor_id in data), None)

def match_request_exists(id: int):
    data = read_query('SELECT 1 from match_requests where id = ?', (id,))

    return any(data)

def match_request_by_combined_key(resume_id:int, job_ad_id:int, get_data_func = read_query):
    data = get_data_func(
        'SELECT id, resume_id, job_ad_id, request_from FROM match_requests WHERE resume_id = ? AND job_ad_id = ?',
        (resume_id, job_ad_id))

    return next((MatchRequest(id=id, resume_id=resume_id, job_ad_id=job_ad_id, requestor_id=requestor_id) for id, resume_id, job_ad_id, requestor_id in data), None)


def its_a_match(id: int, update_data=update_query):
    return update_data('''UPDATE match_requesets 
                    SET match = ?
                    WHERE id = ?''', (1,id))
    

def delete_match_request(id: int, update_data=update_query): #THIS IS FOR REJECT
    return update_data('''DELETE FROM match_requests WHERE id=?''',(id,))

