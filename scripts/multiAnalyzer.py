import os
import glob
import pandas as pd
import json

# Import csv list
path = '../activity_data/' #relative path
extension = 'csv'
os.chdir(path)
csvList = glob.glob('*.{}'.format(extension))

setData = pd.DataFrame()

# Get data and condense 
for i in range(len(csvList)):
    csv = pd.read_csv(csvList[i], dtype=str)
    csv = csv.drop(csv.iloc[:, 25:],axis=1)

    csv = csv.loc[(csv['Message'] == 'set') & (csv['Type'] == 'Data')]

    dayData = {
        'date':[], 'exercise':[], 'reps':[], 'weight':[], 
        'time':[], 'rest':[], 'isStatic':[]
    } 

    for y, row in csv.iterrows():
        if row['Field 4'] == 'category':
            dayData['date'].append(pd.to_datetime(row['Value 1'], unit='s').date())
            dayData['exercise'].append(row['Value 4'])
            dayData['time'].append(float(row['Value 2']))

            if row['Field 5'] == 'repetitions':
                dayData['reps'].append(int(row['Value 5']))
                dayData['weight'].append(float(row['Value 6']))
            else:
                dayData['reps'].append(int(row['Value 6']))
                dayData['weight'].append(float(row['Value 7']))
            
            if dayData['reps'][len(dayData['reps']) - 1] == 0:
                dayData['isStatic'].append(True) 
            else: 
                dayData['isStatic'].append(False)

        else: 
            dayData['rest'].append(float(row['Value 2']))

    for i in range(len(dayData['date']) - len(dayData['rest'])):
        dayData['rest'].append(0) 

    setData = pd.concat([setData, pd.DataFrame(dayData)], ignore_index=True)

calcData = {}
jsonData = pd.DataFrame()
for i, row in setData.iterrows():
    key = f"{row['exercise']}@{row['date']}"
    if key in calcData:
        continue
    
    subset = setData.loc[
        (setData['exercise'] == row['exercise']) & 
        (setData['date'] == row['date'])
    ]
    calcData[key] = {'rep': 'subset'} 
    # print(subset)
    jsonData = pd.concat([jsonData, subset])
# print(jsonData)

# print(jsonData.to_json())
jsonData = jsonData.to_json(orient='split')
jsonData = json.loads(jsonData)
jsonData = json.dumps(jsonData, indent=4)

with open('../activity_data/jsonData.json', 'w') as outfile:
    outfile.write(jsonData)







    # repVolTot = 0
    # print('\n', key)
    # rep, weight, volume, set (size)
        # for y, subRow in subset.iterrows():
        # print(y)
        # repVol = subRow['weight'] * subRow['reps']
        # repVolTot += repVol 
        # print(f"repvol: {repVol}, weight: {subRow['weight']}, reps: {subRow['reps']}")
    

    # repTotal = subset['reps'].sum()
    # weightTotal = subset['weight'].sum()

    # print(f"Avg rep/set: {repTotal / subset.shape[0]}, Rep Total: {round(repTotal, 1)}")
    # print(f"Avg weight/set: {round(weightTotal / subset.shape[0])}, Weight Total: {round(weightTotal, 1)}")
    # print(f"Avg volume/set: {round(repVolTot / subset.shape[0])}, Volume Total: {round(repVolTot, 1)}")


# restTime = setData.loc[setData['isStatic'] != True]['rest'].sum()
# staticRestTime = setData.loc[setData['isStatic'] != False]['rest'].sum()
# workTime = setData.loc[setData['isStatic'] != True]['time'].sum()
# staticWorkTime = setData.loc[setData['isStatic'] != False]['time'].sum()