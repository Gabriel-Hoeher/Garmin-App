import pandas as pd

# returns static sets
def findStatics(stringNum):
    temp = setData.loc[setData[f'Field {stringNum}'] == 'repetitions']
    return temp.loc[temp[f'Value {stringNum}'].astype(float) == 0]

def getTotalSets(df):
    return df.shape[0]

def calcTimeTotal(df):
    return df['Value 2'].astype(float).sum()

# Get data and condense 
file = pd.read_csv('../activity_data/10346562007_ACTIVITY.csv', dtype=str)
file = file.drop(file.iloc[:, 25:],axis=1)

# Get Set and rest data
setData = file.loc[(file['Message'] == 'set') & (file['Type'] == 'Data')]

restData = setData.loc[setData['Field 4'] != 'category'] 
setData = setData.loc[setData['Field 4'] == 'category']

# remove hold data
staticSetData = pd.concat([findStatics('5'), findStatics('6')])

staticRestData = pd.DataFrame()
staticMatch = False

for i, row in setData.iterrows():
    if staticMatch:
        staticMatch = not staticMatch
        row = pd.DataFrame(row.to_numpy().reshape(1,25), columns=setData.columns)
        staticRestData = pd.concat([staticRestData, row])
        setData = setData.drop([i])
    for y in staticSetData.index:
        if i == y:
            staticMatch = not staticMatch

setData = pd.merge(setData,staticSetData, indicator=True, how='outer')
setData = setData.query('_merge=="left_only"').drop('_merge', axis=1)

# rep (sum of setData col) and set total (dimension)
setTotal = getTotalSets(setData)

repTotal = setData.loc[setData['Field 5'] == 'repetitions']['Value 5'].astype(float).sum()
repTotal += setData.loc[setData['Field 6'] == 'repetitions']['Value 6'].astype(float).sum()

# Time totals 
restTotalSec = calcTimeTotal(restData)
setTotalSec = calcTimeTotal(setData)

# static data
staticSetTotal = getTotalSets(staticSetData)
staticTimeTotal = calcTimeTotal(staticSetData)
staticRestTotal = calcTimeTotal(staticRestData)

print(f'avg working time/rep {round(setTotalSec/repTotal, 1)} sec')
print(f'avg working time/set {round(setTotalSec/setTotal, 1)} sec')
print(f'avg rest time/set {round(restTotalSec/setTotal, 1)} sec')
print(f'avg time/set {round((setTotalSec+restTotalSec)/setTotal, 1)} sec')
print(f'avg rep/set {round(repTotal/setTotal, 2)} reps')

print(f'static: avg hold time {round(staticTimeTotal/staticSetTotal, 1)} sec')
print(f'static: avg rest time/set {round(staticRestTotal/staticSetTotal, 1)} sec')

# setData.to_csv('temp.csv')