import random
from numpy.random import rand
import matplotlib.pyplot as plt
import pandas as pd

# import requests
from cadCAD.configuration.utils import bound_norm_random, config_sim, time_step, env_trigger, policy
from models.experiments import exp

# seeds = {
#     'Reservoir_Capacity': 73000,        #The total amount of water that the Grand Ethiopian Renaissance Dam's reservoir can hold.
#     'Reservoir_Level': 0,               #The starting amount of water within the GERD's reservoir.
#     'Reserve_Percent': .05,              #A variable that will be updated with each time step that keeps track of how much of the water flowing through the dam to hold back to fill the reservoir.
#     'Current_Month': 0,                 #Tracks what month the model is in so that the proper river water level can be pulled.
#     'Number_of_Years': 0                #Tracks how many years it takes to fill the reservoir.
# }
# seeds_policy = policy('seeds', seeds)

df = pd.DataFrame({
    'Month':['January','February','March','April','May','June','July','August','September','October','November','December'],
    'Blue_Nile_Water_Flow':[724,448,406,427,503,1084,4989,15237,13625,7130,2451,1257],
    'White_Nile_Water_Flow':[2469,1905,2014,2225,2026,1792,1368,1435,2236,3024,2786,2747],
    'Atbara_River_Water_Flow':[17,6,1,3,8,88,1536,5126,3306,770,145,46],
    'Total_Water_Flow':[3210,2359,2421,2655,2537,2964,7893,21798,19167,10924,5382,4050]
})

# Policies per Mechanism
def Dam_Policy(params, step, sL, s):
  f = 0
  m = s['Current_Month']

  if s['Reservoir_Level'] < s['Reservoir_Capacity']:
    f = df.at[m, 'Blue_Nile_Water_Flow'] * s['Reserve_Percent']
    if m == 11:
      u = -11
      y = 1
    else:
      u = 1
      y = 0
    return({'Dam_Reserve': f, 'Month_Update': u, 'Year_Update': y})
  else:
    f = 0
    if m == 11:
      u = -11
      y = 0
    else:
      u = 1
      y = 0
    return({'Dam_Reserve': f, 'Month_Update': u, 'Year_Update': y})

def Reservoir_Update(params, step, sL, s, _input):
  k = 'Reservoir_Level'
  v = s['Reservoir_Level'] + _input['Dam_Reserve']
  return (k,v)

def Month_Update(params, step, sL, s, _input):
  k = 'Current_Month'
  v = s['Current_Month'] + _input['Month_Update']
  return (k,v)

def Year_Update(params, step, sL, s, _input):
  k = 'Number_of_Years'
  v = s['Number_of_Years'] + _input['Year_Update']
  return (k,v)




# Genesis States
genesis_states = {
    'Reservoir_Capacity': 73000,        #The total amount of water that the Grand Ethiopian Renaissance Dam's reservoir can hold.
    'Reservoir_Level': 0,               #The starting amount of water within the GERD's reservoir.
    'Reserve_Percent': .05,              #A variable that will be updated with each time step that keeps track of how much of the water flowing through the dam to hold back to fill the reservoir.
    'Current_Month': 0,                 #Tracks what month the model is in so that the proper river water level can be pulled.
    'Number_of_Years': 0                #Tracks how many years it takes to fill the reservoir.
}


# # Environment Process
# trigger_timestamps = ['2018-10-01 15:16:25', '2018-10-01 15:16:27', '2018-10-01 15:16:29']
# env_processes = {
#     "s3": [lambda _g, x: 5],
#     "s4": env_trigger(3)(trigger_field='timestamp', trigger_vals=trigger_timestamps, funct_list=[lambda _g, x: 10])
# }


partial_state_update_blocks = [
    {
        'policies': {
            Dam_Policy
        },    
        'variables': {
            'Reservoir_Level': Reservoir_Update,
            'Current_Month': Month_Update,
            'Number_of_Years' : Year_Update
        }
    }

]


sim_config_dict = {
        "N": 1,
        "T": range(5)
    }

sim_config = config_sim(sim_config_dict)
exp.append_model(
    user_id='user_a',
    model_id='sys_model_1',
    sim_configs=sim_config,
    initial_state=genesis_states,
    env_processes=env_processes,
    partial_state_update_blocks=partial_state_update_blocks
)
#
# class Struct:
#     def __init__(self, **entries):
#         self.__dict__.update(entries)
#
# job = exp.configs[0]
# ser_job = exp.ser_flattened_configs[0]
# psub_struct = deepcopy(Struct(**job.partial_state_update_blocks[0]))

# +++++
# print(psub_struct.__dict__)
# ser_psubs = dill.dumps(partial_state_update_blocks)
# encoded_psubs = codecs.encode(ser_psubs, "base64").decode()
# json_obj = {
#     "partial_state_update_blocks": encoded_psubs
# }

# url = 'http://0.0.0.0:5000'
# job = exp.configs[0]
# pickled_encoded_job = codecs.encode(dill.dumps(job), "base64").decode()
# r = requests.post(f'{url}/job', json={'job': pickled_encoded_job})
# print(r.text)
# print()

# jobs = deepcopy(exp.configs)
#
# url = 'http://0.0.0.0:5000'
# # print(type(jobs[0]))
# # exit()
# dill.detect.trace(True)
#
# print()
# job = jobs[0]
# job_dict = job.__dict__
#
# # help(job)
# # print(job.__slotnames__)
# # exit()
#
# r = requests.post(f'{url}/psubs', json={
#         "partial_state_update_blocks": codecs.encode(dill.dumps(job.partial_state_update_blocks), "base64").decode()
#     }
# )
#
# print(r.text)
# print()
