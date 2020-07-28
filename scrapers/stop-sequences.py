import numpy as np 
import json
import os

def add_stop_sequences():
    filename = os.path.join(os.path.dirname(__file__),'data/routes_23_12_2019.txt')

    stopid = np.loadtxt(filename,delimiter='\t',usecols=[0],dtype=str)
    routeData = np.loadtxt(filename,delimiter='\t',usecols=[14],dtype=str)
    direction = np.loadtxt(filename,delimiter='\t',usecols=[5],dtype=str)
    atcoCode = np.loadtxt(filename,delimiter='\t',usecols=[6],dtype=str)
    operator = np.loadtxt(filename,delimiter='\t',usecols=[2],dtype=str)
    name_en = np.loadtxt(filename,delimiter='\t',usecols=[8],dtype=str)
    name_ga = np.loadtxt(filename,delimiter='\t',usecols=[9],dtype=str)
    stop_order = np.loadtxt(filename,delimiter='\t',usecols=[3],dtype=str)
    routenames = np.loadtxt(filename,delimiter='\t',usecols=[4],dtype=str)

    stop_sequences = dict()

    for i,route in enumerate(routenames):
        if operator[i] in ['Dublin Bus','Go-Ahead']:
            if route not in stop_sequences:
                stop_sequences[route] = dict()
                stop_sequences[route]['Inbound'] = {'sequence':[],'atcocodes':[]}
                stop_sequences[route]['Outbound'] = {'sequence':[],'atcocodes':[]}
            if atcoCode[i] not in stop_sequences[route][direction[i]]['atcocodes'] and stop_order[i] not in stop_sequences[route][direction[i]]['sequence']:
                stop_sequences[route][direction[i]]['atcocodes'] += [atcoCode[i]]
                stop_sequences[route][direction[i]]['sequence'] += [int(stop_order[i])]
    
    for i, seq in enumerate(stop_sequences['11']['Inbound']['sequence']):
        print(seq,stop_sequences['11']['Inbound']['atcocodes'][i])
    print()

    for route in stop_sequences:
        for direction in stop_sequences[route]:
            stop_sequences[route][direction]['atcocodes'] = [x for _,x in sorted(zip(stop_sequences[route][direction]['sequence'],stop_sequences[route][direction]['atcocodes']))]
            stop_sequences[route][direction]['sequence'] = sorted(stop_sequences[route][direction]['sequence'])

    for i, seq in enumerate(stop_sequences['11']['Inbound']['sequence']):
        print(seq,stop_sequences['11']['Inbound']['atcocodes'][i])
    print()

    for route in stop_sequences:
        for direction in stop_sequences[route]:
            sequence_int = [int(x) for x in stop_sequences[route][direction]['sequence']]
            if sequence_int != sorted(sequence_int):
                print(route, direction)

    for route in stop_sequences:
        for direction in stop_sequences[route]:
            stop_sequences[route][direction].pop('sequence')

    with open('dublinbus/local-bus-data/all-routes-sequences.json','w') as outfile:
        json.dump(stop_sequences,outfile)
    
add_stop_sequences()