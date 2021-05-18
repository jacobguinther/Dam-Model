from models.updates import *

partial_state_update_blocks = [
    {
        'policies': {
            'Dam_Policy': Dam_Policy
        },    
        'states': {
            'Reservoir_Level': Reservoir_Update,
            'Current_Month': Month_Update,
            'Number_of_Years' : Year_Update
        }
    }

]