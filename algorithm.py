import keyboard
import mediapipe as mp
from shared_data import lock

def run(data):
   
   hashpositions(data)


def hashpositions(data):
    
    unhashedData = []
    
    for datum in data:
        for comparisonData in data:
            #compare the two ids
            
            if datum[0] != comparisonData[0]:
                #do comparisons and add 1s or 0s to data based on position
                
                if(datum[1] > comparisonData[1]):
                    
                    unhashedData.append(1)
                else:
                    unhashedData.append(0)
                if(datum[2] > comparisonData[2]):
                    unhashedData.append(1)
                else:
                    unhashedData.append(0)
                

    string = ''.join(str(i) for i in unhashedData)
    #print(string, end="\n\n")
    correct = 111111111111111111111111010101010101010100111111011111110101010101010101010101010000111101010101010101010101010101010101000000110101010101010101010101010101010100000000000101010001010100010101000101010010101011111111010101010001010100010101000010101000111100010101000001010000000100001010100000110000010100000001000000000000101010000000000000010000000000000000001010101110111111111111000101010001010100101010101010111100111100000101000000010010101010101010110000110000000100000000001010101010101010000000000000000000000010101010111111111111111111011111000101011010101010101111111011111110111100000001101010101010101111101011110000110000000010101010101010101110101011000000000000001010101011111111111111111111111111010101101010101010111111101111111011111110010110101010101011111110111111101111111010011010101010101011111010111110101111101010
    similar = similarity(string, str(correct))

    if similar > .93:
        print(f"success | similarity: {similar}")
    return 0




"""Return the similarity of two given strings in decimal """
def similarity(given, compare):
    #total
    total = len(given)
    
    same = 0
    
    #if they are not of the same length terminate
    if(len(given) != len(compare)):
        return -1
    
    #compare and add to same counter
    for i in range(len(given)):
        if given[i] == compare[i]:
            same += 1
    
    #calculate percentage similarity and return
    return (same/total)
