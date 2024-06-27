import keyboard
import mediapipe as mp
import csv
import os
import dataRetriever as dr

threshold = 0.939
previous_frame_data = []
momementBuffer = 3
dataFilename = './handData.csv'

record_output_file = './output.txt'
record = False

handLibraryData = []

"""input hand position data and optional list library for parsing, 
    if none is given it will load from csv"""

def findPositions(data, givenLibrary = None):

    global handLibraryData,previous_frame_data,record

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
    
    #if there is data for the previous frame 
    if previous_frame_data != []:
        for i in range(len(data)):
            #if the movement is less than the movement buffer then its 00
            if abs(data[i][1]-previous_frame_data[i][1]) < momementBuffer:
                positionalArray.append(0)
                positionalArray.append(0)
            #if the x-coordinate is greater then 10
            elif data[i][1] > previous_frame_data[i][1] and abs(data[i][1]-previous_frame_data[i][1]) > momementBuffer:
                positionalArray.append(1)
                positionalArray.append(0)
            #if position is less then 01
            elif data[i][1] < previous_frame_data[i][1] and abs(data[i][1]-previous_frame_data[i][1]) > momementBuffer:
                positionalArray.append(0)
                positionalArray.append(1) 

             #if the movement is less than the movement buffer then its 00
            if abs(data[i][2]-previous_frame_data[i][2]) < momementBuffer:
                positionalArray.append(0)
                positionalArray.append(0)
            #if the y-coordinate is greater then 10
            elif data[i][2] > previous_frame_data[i][2] and abs(data[i][2]-previous_frame_data[i][2]) > momementBuffer:
                positionalArray.append(1)
                positionalArray.append(0)
            #if position is less then 01
            elif data[i][2] < previous_frame_data[i][2] and abs(data[i][2]-previous_frame_data[i][2]) > momementBuffer:
                positionalArray.append(0)
                positionalArray.append(1)    
            
        """if abs(data[8][2]-previous_frame_data[8][2]) > momementBuffer:
            print(data[8][0])
            print("movement")"""
    
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
    
    
    """index = index_through_similarity(string)
    #replace previous frame data"""
    previous_frame_data = data
    
    
    if keyboard.is_pressed ('r') and record == False:
        print('recording- true')
        record = True
    elif keyboard.is_pressed('r') and record == True:
        print('recording- false')
        record = False

    if record == True:
        print('recorded')
        record_string(string)

    dr.findMovement(string)
    
    """
    #return/print the name of the index if it exists
    if index != None:
        #os.system('cls')
        #print(handLibraryData[index][0])
        return handLibraryData[index][0]
    else:
        
        #os.system('cls')
        #print("No match")
        return None"""
        


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

def record_string(string):
    string += ','
    try:
        with open(record_output_file, "a") as f:
            f.write(string)
    except Exception as e:
        print(e)

"""Return the similarity of two given strings in decimal """
def similarity(given, compare):
    #total
    total = len(given)
    
    
    same = 0
    try:
        
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

def index_through_similarity(string):
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
    return index