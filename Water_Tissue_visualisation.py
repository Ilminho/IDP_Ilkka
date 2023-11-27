import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

filepath='result.csv'
headers = ['startTime','endTime', 'Water']
df = pd.read_csv(filepath, names=headers)
df = df.iloc[1:]
chunksize=50000

peaks=df.loc[:,'startTime']
reducer = 1

def process_row(row):
    peak = row.iloc[0]
    return round(float(peak)*chunksize)

result = df.apply(process_row,axis=1)
currentChunkStart=0
currentChunkEnd=chunksize
currentChunkIndex=0
peakList = []

def updateChunks():
    global currentChunkStart
    global currentChunkEnd
    global currentChunkIndex
    currentChunkStart=currentChunkIndex*chunksize
    currentChunkEnd=currentChunkStart+chunksize
    currentChunkIndex=currentChunkIndex+1
    
def addPeakToPlotList(value):
    global currentChunkStart
    global currentChunkEnd
    global peakList
    if((value>currentChunkStart)&(value<currentChunkEnd)):
        peakList.append(value-(chunksize*(currentChunkIndex-1)))
     
    
def updateRelevantTimestamps():
    global peakList
    peakList=[]
    workList = list(result)
    for value in workList:
        addPeakToPlotList(value)
    print(peakList)

timestamps=peaks

print(result)

def update_plot(frame):
    updateRelevantTimestamps()
    row = next(csv_stream)
    adc2.clear()
    adc2.extend(row['adc2'])
    ax.clear()
    ax.plot(adc2, color='r')
    for x_value in peakList:
        ax.axvline(x=x_value, color='blue', linestyle='--', label=f'Line at {x_value}')
    ax.set_ylim(bottom=0, top=2500)
    updateChunks()

    

file_path = 'Benchmark signal.csv'
csv_stream = pd.read_csv(file_path, chunksize=chunksize)
adc2 = []
adc2_water=[]
adc2_tissue=[]
fig3, ax = plt.subplots()
ani3 = FuncAnimation(fig3, update_plot, blit=False, interval=1000, cache_frame_data=False)

plt.show()