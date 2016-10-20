
#┌──────────────┐
#│ --- Init --- │
#└──────────────┘

import re # for regex checking 

# user inputs datafile, L, mean_vert_disp, and mean_horiz_disp
#assignment of user inputs
path = input("Please enter the path to the desired data file for analysis: ")
mean_vert_dist = float(input("Please enter the mean vertical spacing for the provided data file: "))
mean_horiz_dist = float(input("Please enter the mean horizontal spacing for the provided data file: "))
sea_rise = float(input("Please enter a sea level height for remaining land area analysis: ")) # should this refer to height or increase?


#assignment of file object to user-provided file
datafile = open(path, 'r')
data_list = []


#┌───────────────────┐
#│ --- Functions --- │
#└───────────────────┘


def validate(path): # maybs change this to read from data_list so the file doesn't have to be scanned twice, for speed. Not imperative.
    """Checks whether the filepath refers to a valid YXZ format file. 
    
    Retrieves the file located at the given filepath. Opens that file, and checks that
    the file contains the correct number of entries per line, and only valid characters
    in each entry. If the file is found to be invalid, the program quits and states the
    relevant error.
    
    Args:
        testing_file: The path to the file for validation.
    """
    valid_chars = re.compile('[0-9\.\-]') # characters 0 through 9 
    with open(path, "r") as test: 
        for line in test: # test each line of file
            blocks = line.split()
            if len(blocks) == 3: # tests for correct number of entries in file
                for item in blocks:
                    if valid_chars.match(item): # regex matching #Hold on, this doesn't strictly verify that the file is in YXZ format,
                                                # what if it was actually a XYZ format file? Then it'd be wrong but our checker would accept it
                        pass
                    else:
                        print("Invalid characters")
                        return False
            else:
                print("Invalid file format")
                return False
    print("File type validated")
    return True

# validate file
validate(path)

def calc_area(L, mean_vert, mean_horiz):
    """Finds land area, as per first approximation.
    
    Args:
        L: A numeric value representing sea level rise. 
        mean_vert: The numeric value for mean vertical spacing of
            data values in datafile.
        mean_horiz: The numeric value for mean horizontal spacing 
            of data values in datafile.
        array: The array containing line-split data values
            from datafile.
            
    Returns:
        A float value representing the absolute area of land above sea 
        level (in square kilometres) for a given value of L, as per the
        first approximation. 
    """
    count = 0
    for line in datafile:
        data_list.append(line.split())
    for item in data_list:
        if float(item[2]) > L:
            count += 1
    area = count * mean_vert * mean_horiz
    return area

def disp_result():
    """Displays required output for first approximation.
    
    Prints absolute and relative land area remaining for a 
    given sea level rise.
    """
    current = calc_area(0, mean_vert_dist, mean_horiz_dist)
    absolute = calc_area(sea_rise, mean_vert_dist, mean_horiz_dist)
    percentage = (absolute/current) * 100


    print("At %0.0f metres above current sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value" % (sea_rise, absolute, percentage))

disp_result()
