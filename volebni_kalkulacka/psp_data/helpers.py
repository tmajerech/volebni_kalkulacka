
from .models import Organy

def get_current_election_period():
    id_org = ''
    try:
        #get latest election period id
        id_org = Organy.objects.filter(zkratka__regex="PSP\d+\d?").latest('id_organ').id_organ

    except Exception as e:
        print('error getting last election period')
        print(e)

    return id_org
