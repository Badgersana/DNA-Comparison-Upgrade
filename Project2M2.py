#gets menu choice, validates input and reasks if incorrect
def get_menu_choice():
    userInput = int(input('Please choose an option: '))
    while userInput < 1 or userInput > 5:
        userInput = int(input('Please choose an option: '))
        
    return userInput

#prints menu
def print_menu():
    print('Main Menu')
    print('1. Insert an indel')
    print('2. Remove an indel')
    print('3. Score similarity')
    print('4. Suggest indel')
    print('5. Quit\n')  

#asks user to select a sequence, validates input and reasks if incorrect
def get_sequence_number():
    sequenceNumber = int(input('Sequence 1 or 2? '))
    while sequenceNumber < 1 or sequenceNumber > 2:
        sequenceNumber = int(input('Sequence 1 or 2? '))
    
    return sequenceNumber

#adds missing number of indels to end so both sequences are even in length   
def pad_with_indels(sequence, num):
    sequence = sequence + (num * '-')

    return sequence

#asks the user what position an indel should be inserted at
def get_insert_position(sequence):
    position = int(input('Please choose a position: '))
    while position - 1 < 0 or position > len(sequence):
        position = int(input('Please choose a position: '))

    return position

#asks user what indel should be removed based on position
#validates this answer and reasks if incorrect
def get_remove_position(sequence):
    position = int(input('Please choose a position: '))
    while sequence[position - 1] != '-':
        position = int(input('Please choose a position: '))

    return position

#removes an indel in a sequence based off of get_remove_position(sequence)
def remove_indel(sequence, index):
    if index == -1 and sequence[index] == '-':
        replacementSequence = sequence[:-1]
    else:
        replacementSequence = sequence[:index - 1] +  sequence[index:]

    return replacementSequence

#checks specified sequence and brute forces a solution to optimal indel position for the highest similarity
#I initially transfer the sequence into a new string so that we can maintain the
#original for each pass of the loop.
#After this I insert an indel at 'count' index and check if there is any need to add or
#remove padding.
#I then change the string to upper case and then call 'make_lower_case' which changes any matches
#to lower case
#I then work out what the match rate is and compare it to the current best, if it is larger
#I record all results, otherwise I move on to the next iteration.
#After going through all iterations of my loop I print the results to the user
#(couldnt think of another way after staring at this for 11 hours).
def find_optimal_indel_position(sequence, otherSequence):
    bestMatchRate = 0
    bestPosition = 0
    bestPositionMatches = 0
    bestPositionMismatches = 0
    newSequence = ''
    
    for count in range(len(sequence)):
        newSequence = sequence
        
        newSequence = insert_indel(sequence, count)
        newSequence, otherSequence = check_for_padding(newSequence, otherSequence)

        newSequence, otherSequence = make_upper_case(newSequence, otherSequence)
        newSequence, otherSequence = make_lower_case(newSequence, otherSequence)
        
        
        matches = count_matches(newSequence, otherSequence)
        
        mismatches = len(newSequence) - matches

        matchRate = (matches / (matches + mismatches)) * 100

        if matchRate > bestMatchRate:
            bestPosition = count + 1
            bestMatchRate = matchRate
            bestPositionMatches = matches
            bestPositionMismatches = (len(sequence) - matches) + 1
            
    print(f'\nInsert an indel into Sequence 1 at position {bestPosition}.')
    print(f'Similarity: {bestPositionMatches} matches, {bestPositionMismatches} mismatches. {bestMatchRate:.1f}% match rate. ')

    return bestPosition

#adds an indel at index position and returns the new sequence
def insert_indel(sequence, index):
    if index == len(sequence):
        sequence = sequence + '-'
    else:
        sequence = sequence[:index] + '-' + sequence[index:]
        
    return sequence

#counts number of matches
def count_matches(sequence1, sequence2):
    matches = 0
    
    for i in range(len(sequence1)):
        if sequence1[i] == sequence2[i] and sequence1[i] != '-' and sequence2[i] != '-':
            matches += 1

    return matches

#changes all characters to uppercase and returns the uppercase sequences
def make_upper_case(sequence1, sequence2):
    newSequence1 = sequence1.upper()
    newSequence2 = sequence2.upper()

    return newSequence1, newSequence2

#changes all matching characters to lowercase and returns the new sequences
def make_lower_case(sequence1, sequence2):
    newSequence1 = ''
    newSequence2 = ''
    
    for i in range(len(sequence1)):
        if sequence1[i] == sequence2[i] and sequence1[i] != '-' and sequence2[i] != '-':
            newSequence1 += sequence1[i].lower()
            newSequence2 += sequence2[i].lower()
                
        elif sequence1[i] != sequence2[i] or (sequence1[i] == '-' and sequence2[i] == '-'):
            newSequence1 += sequence1[i]
            newSequence2 += sequence2[i]

    sequence1 = newSequence1
    sequence2 = newSequence2

    return sequence1, sequence2

#checks if padding needs to be added because lengths are different, or taken away because the last character
#in both strings are indels
def check_for_padding(sequence1, sequence2):

    if sequence1[-1] == '-' and sequence2[-1] == '-':
        sequence1 = remove_indel(sequence1, -1)
        sequence2 = remove_indel(sequence2, -1)
        
    elif len(sequence1) < len(sequence2):
        num = len(sequence2) - len(sequence1)
        sequence1 = pad_with_indels(sequence1, num)
        
    elif len(sequence2) < len(sequence1):
        num = len(sequence1) - len(sequence2)
        sequence2 = pad_with_indels(sequence2, num)

    return sequence1, sequence2

#checks for matches to allow for printing the similarities to users
def match_check(sequence1, sequence2):
    matches = count_matches(sequence1, sequence2)

    mismatches = len(sequence1) - matches

    matchRate = (matches / (matches + mismatches)) * 100

    return matchRate, matches, mismatches

def print_similarity(matchRate, matches, mismatches):
    print(f'\nSimilarity: {matches} matches, {mismatches} mismatches. {matchRate:.1f}% match rate.')
    
    

if __name__ == '__main__':
    running = True
    sequence1 = input('Please enter DNA Sequence 1: ')
    sequence2 = input('Please enter DNA Sequence 2: ')

        
    while running == True:
        sequence1, sequence2 = check_for_padding(sequence1, sequence2)

        #make lower case
        sequence1, sequence2 = make_lower_case(sequence1, sequence2)
        print(f'\nSequence 1: {sequence1}')
        print(f'Sequence 2: {sequence2}\n')
        
        print_menu()
        userInput = get_menu_choice()

        if userInput == 1: #INSERT INDEL, WORKS
            sequenceNumber = get_sequence_number()

            if sequenceNumber == 1:
                inputPosition = get_insert_position(sequence1) - 1 
                sequence1 = insert_indel(sequence1, inputPosition)
                
            elif sequenceNumber == 2:
                inputPosition = get_insert_position(sequence2) - 1
                sequence2 = insert_indel(sequence2, inputPosition)

            sequence1, sequence2 = make_upper_case(sequence1, sequence2)

        elif userInput == 2: # REMOVE INDEL, WORKS
            sequenceNumber = get_sequence_number()

            if sequenceNumber == 1:
                removePosition = get_remove_position(sequence1)
                sequence1 = remove_indel(sequence1, removePosition)
                sequence2 = remove_indel(sequence2, -1)
                

            elif sequenceNumber == 2: 
                removePosition = get_remove_position(sequence2)
                sequence2 = remove_indel(sequence2, removePosition)
                sequence1 = remove_indel(sequence1, -1)

            sequence1, sequence2 = make_upper_case(sequence1, sequence2)
    
        elif userInput == 3: # CHECK SIMILARITY, WORKS
            matchRate, matches, mismatches = match_check(sequence1, sequence2)
            print_similarity(matchRate, matches, mismatches)
            
        elif userInput == 4: # CHECKS FOR BEST INDEL POSITION, WORKS
            sequenceNumber = get_sequence_number()

            if sequenceNumber == 1:
                bestPosition = find_optimal_indel_position(sequence1, sequence2)
                
                
            elif sequenceNumber == 2:
                bestPosition = find_optimal_indel_position(sequence2, sequence1)

            sequence1, sequence2 = make_upper_case(sequence1, sequence2)

        elif userInput == 5: # QUITS, WORKS
            running == False
            break
