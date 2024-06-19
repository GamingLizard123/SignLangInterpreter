import keyboard
import mediapipe as mp
from shared_data import lock
import csv
import os

threshold = 0.939
dataFilename = './handData.csv'

handLibraryData = []

def run(data):
   
   findPositions(data)

"""input hand position data and optional list library for parsing, if none is given it will load from csv"""
def findPositions(data, givenLibrary = None):
    global handLibraryData
    #check for library if not load
    if givenLibrary == None:
        initializeData()
    else:
        handLibraryData = givenLibrary      
    
    #get data
    positionalArray = []
    
    for datum in data:
        for comparisonData in data:
            #compare the two ids
            
            if datum[0] != comparisonData[0]:
                #do comparisons and add 1s or 0s to data based on position
                #x-position
                if(datum[1] > comparisonData[1]):
                    
                    positionalArray.append(1)
                else:
                    positionalArray.append(0)
                #y-position
                if(datum[2] > comparisonData[2]):
                    positionalArray.append(1)
                else:
                    positionalArray.append(0)
    #if it is only one hand
    if len(positionalArray) == 840:
        #get handedness
        if data[0][0] == 21:
            #right hand
            positionalArray.append(0)
            positionalArray.append(1)
        elif data[0][0] == 0:
            #left hand
            positionalArray.append(1)
            positionalArray.append(0)
        
                

    string = ''.join(str(i) for i in positionalArray)
    
    #print(string, end="\n\n")
    
    
    maxLikeness = 0
    index = None
    #compare all data with library data
    for i in range(len(handLibraryData)):
        #find similarity
        
        similarityVal = similarity(string, str(handLibraryData[i][1]))
        #print(f"comparing with {handLibraryData[i][0]} similarity: {similarityVal}")
        
        if  similarityVal > threshold:
            #if its greater than the likeness then add the index
            if similarityVal > maxLikeness:
                index = i
    #return/print the name of the index if it exists
    
    if index != None:
        os.system('cls')
        print(handLibraryData[index][0])
        return handLibraryData[index][0]
    else:
        
        os.system('cls')
        print("No match")
        return None
        


"""loads data into python list and returns it if given input"""
def initializeData(with_return = False):
    
    #read through csv and put it in a list
    try:
        with open(dataFilename, 'r') as f:
            csv_reader = csv.reader(f)
            #iterate through every row
            print("loading data...")
            for row in csv_reader:
                handLibraryData.append(row)
            print('data loaded')
        handLibraryData.pop(0)
    except:
        print("failed to load data")
        exit()
    finally:
        if with_return:
            return handLibraryData

"""Return the similarity of two given strings in decimal """
def similarity(given, compare):
    #total
    total = len(given)
    
    
    same = 0
    try:
        
        #print(len(given), len(compare))
        #if they are not of the same length terminate
        #if they are not the same hand terminate
        if(total != len(compare)):
            return -1
        
        if given[total - 2] != compare[total - 2]:
            return -1
    except:
        print('error with similarity input variables')
        exit()
    
    #compare and add to same counter
    for i in range(len(given)):
        if given[i] == compare[i]:
            same += 1
    
    #calculate percentage similarity and return
    return (same/total)
