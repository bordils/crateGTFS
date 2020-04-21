
def parseStops(stops):
    '''

    There is an extra in some of the elements of the third column (stop_name)
    to repair this, we must concatenate 3rd and 4th column and bring forward
    the rest of the line and delete the last empty element.
    '''

    lineIndex = 1
    # accesing line by line
    for line in stops[1][1:]:
        if(len(line) > 11):
            # check if the line had an extra comma in the naming
            eIndex = 2
            # starting on the conflicting element
            for eIndex in range(2,len(line)):
                if eIndex == 2:
                    # if there was a comma, we must concatenate with the following value
                    stops[1][lineIndex][eIndex] += stops[1][lineIndex][eIndex + 1]

                if (eIndex > 2 and eIndex< len(line)-1):
                    # now we must bring forward the rest of the values
                    stops[1][lineIndex][eIndex] = stops[1][lineIndex][eIndex + 1]

                if eIndex == (len(line)-1):
                    # the last column is not there anymore
                    del line[eIndex]
        lineIndex +=1


def columnToFloat(table,columnIndex):
    '''

    Given a table and the index of a column to convert, this function will cast
    all the values of the column into float (except the header).

    TODO: handle exceptions. We are currently removing rows that do not contain
    geographic information.
    '''
    # list of indexes that do not contain a number in the expected positions
    # later to be removed
    indexesOfEmpty = []

    lineIndex = 1
    for line in table[1][1:]:
        try:
            # try to remove over quotation mark to be able to cast as a float.
            a = float(table[1][lineIndex][columnIndex].replace('"',''))
            table[1][lineIndex][columnIndex] = a
        except ValueError:
            # otherWise remove
            indexesOfEmpty.append(lineIndex)
        lineIndex += 1

    # removing lines with empty values
    for i in indexesOfEmpty[len(indexesOfEmpty):0:-1]:
        table[1].pop(i)




def columnToBool(table,columnIndex):
    '''

    given a table and the index of a column to convert, this function will cast
    all the vlues of the column into boolean (except the header).
    '''

    lineIndex = 1
    for line in table[1][1:]:
        # casting to boolean type
        table[1][lineIndex][columnIndex] = bool(table[1][lineIndex][columnIndex])
        lineIndex += 1
