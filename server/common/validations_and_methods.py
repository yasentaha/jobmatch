from server.data.models import WorkPlace

'''
validacii za kinti
i vsichko keoto se setim
i koeto se preizpolzva kato naprimer get town by id i tn i tn

'''

def validate_work_place(work_place:str):
    validation_work_places = [WorkPlace.HYBRID, WorkPlace.ONSITE, WorkPlace.REMOTE]
    if work_place in validation_work_places:
        return True