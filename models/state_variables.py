genesis_states = {
    'Reservoir_Capacity': 73000,        #The total amount of water that the Grand Ethiopian Renaissance Dam's reservoir can hold.
    'Reservoir_Level': 0,               #The starting amount of water within the GERD's reservoir.
    'Reserve_Percent': .05,              #A variable that will be updated with each time step that keeps track of how much of the water flowing through the dam to hold back to fill the reservoir.
    'Current_Month': 0,                 #Tracks what month the model is in so that the proper river water level can be pulled.
    'Number_of_Years': 0                #Tracks how many years it takes to fill the reservoir.
}