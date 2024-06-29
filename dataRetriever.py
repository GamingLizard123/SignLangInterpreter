import csv

movementIndex = None
step = 0
threshold = 0.83#0.935

dataLibrary = []

def findMovement(inputString, optional_library = None):
    global movementIndex, step, dataLibrary

    #if there is a library given use it, else use the datalibrary
    if optional_library != None:
        dataLibrary = optional_library
    else:
        if dataLibrary == []:
            initialize()
        

    #if there is a movement index 
    if movementIndex != None:
        #print("foo")
        #TODO make the remaining step finding function
        similarity_of_movement = similarity(inputString, dataLibrary[movementIndex][step])
        if similarity_of_movement > threshold and len(dataLibrary[movementIndex])-1 > step:
            step += 1
            #if its at the last step
            if len(dataLibrary[movementIndex])-1 == step:
                #print movement name
                print(dataLibrary[movementIndex][step])
                #reset
                step = 0
                movementIndex = None
        else:
            step = 0
            movementIndex = None
    
    #else if there isnt't a movement index
    else:
        movementIndex = index_through_similarity(inputString)
        
        """try:
            print(f"index: {movementIndex} | Similarity: {similarity(inputString, dataLibrary[movementIndex][0])}")
        except Exception as e:
            print(f"Exception in find movement: {e}")"""

        step += 1
            
            

def index_through_similarity(inputString):
    global dataLibrary

    maxLikeness = 0
    index = None
    #compare all data with library data
    for i in range(len(dataLibrary)):
        #find similarity
        
        similarityVal = similarity(inputString, str(dataLibrary[i][0]))

        if  similarityVal > threshold:
            print(similarityVal, i)
            #if its greater than the likeness then add the index
            if similarityVal > maxLikeness:
                index = i
    
    return index

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
            return -2
    except:
        print('error with similarity input variables')
        exit()
    
    #compare and add to same counter
    for i in range(len(given)):
        if given[i] == compare[i]:
            same += 1
    
    #calculate percentage similarity and return
    return (same/total)

def initialize():
    global dataLibrary
    print("loading data...")
    try:
        with open("./data.csv", 'r') as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                dataLibrary.append(row)
        print("data loaded!")
        return dataLibrary
    except Exception as e:
        print(f"data loading error in initialize, dataRetriever.py: {e}")