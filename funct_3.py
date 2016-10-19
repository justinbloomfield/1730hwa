#┌──────────────┐
#│ --- Init --- │
#└──────────────┘

import re # for regex checking 
import numpy as np # linspace, as range() can't use floats
import matplotlib.pyplot as plt # for graphing
import math as mth # for cos and radians -> degrees conversion

# user inputs datafile, L, user_vert_dist, and user_horiz_dist
#assignment of user inputs
#path = input("Please enter the path to the desired data file for analysis: ")
sea_rise = float(input("Please enter a sea level height for remaining land area analysis: ")) #maybe an exception catcher here if we decide we want to account for user to not enter anything
user_vert_dist = float(input("Please enter the mean vertical spacing for the provided data file: "))
user_horiz_dist = float(input("Please enter the mean horizontal spacing for the provided data file: "))

path = "data_files/sydney250m.txt"

#assignment of file object to user-provided file
datafile = open(path, 'r')
data_array = []


#┌───────────────────┐
#│ --- Functions --- │
#└───────────────────┘


def get_info(): # gets data from file and enters it into an array
    '''Fetches each line in YXZ file.
    
    Retrieves each line in the YXZ file, which pertain to the latitude, longitude and
    elevation of a sample point. Splits the values for each line across whitespace, 
    and appends the three values for each line to an array called data_array. 
    '''
    for line in datafile:
        data_array.append(line.split())


def validate(testing_file): # maybs change this to read from data_array so the file doesn't have to be scanned twice, for speed. Not imperative.
    """Checks whether the filepath refers to a valid YXZ format file. 
    
    Retrieves the file located at the given filepath. Opens that file, and checks that
    the file contains the correct number of entries per line, and only valid characters
    in each entry. If the file is found to be invalid, the program quits and states the
    relevant error.
    
    Args:
        testing_file: The path to the file for validation.
        
    Returns:
        True
    """
    print("Validating file...")
    valid_chars = re.compile('[0-9\.\-]') # characters 0 through 9 
    with open(testing_file, "r") as test: 
        for line in test: # test each line of file
            blocks = line.split()
            if len(blocks) == 3: # tests for correct number of entries in file
                for item in blocks:
                    if valid_chars.match(item): # regex matching
                        pass
                    else:
                        print("Invalid characters")
                        return False
            else:
                print("Invalid file format")
                return False
    print("Valid file")
    get_info() # when file has passed, get data from file
    return True

# validate file
validate(path)


def spacing(index): # horizontal currently not working. 
    '''
    
    '''
    diff_list = []
    col_entries = []
    af = lambda x: abs(float(x))
 
    for entry in data_array:
        col_entries.append(entry[index])

    for num in range(1, len(col_entries)):
        difference = af(col_entries[num]) - af(col_entries[num-1])
        diff_list.append(abs(difference))
     
    mean_spacing = sum(diff_list) / len(diff_list)

    return mean_spacing

# calculate mean_spacing, maybe include this part in main()?
mean_horiz_dist = spacing(1) 
mean_vert_dist = spacing(0)


def calc_area(L, mean_vert, mean_horiz, array):
    """
    calculates the area above sea level L, with mean vertical and horizontal spacing given
    """
    area = 0
    count = 0
    for item in data_array:
        if float(item[2]) > L:
            count += 1
    area = count * mean_vert * mean_horiz
    return area    
    

def tier3_calc_area(L, mean_horiz, mean_vert, array): # calculates area using arc degrees
    lat_list = []
    width_list = []
    height_list = []
    area_list = []
    total_area = 0

    for item in data_array:
        if float(item[2]) > L:
            lat_list.append(float(item[0]))
            width_list.append(float(item[1]))
            width = 40075/360 * mth.cos(mth.radians(float(item[0])))*mean_horiz_dist
            height = 40007/360 * mean_vert_dist
            area_list.append(width*height)

    total_area = sum(area_list)*100
    return total_area
    

def zero_rise(mean_vert, mean_horiz, array, approximation): 
    '''
    performs function level 2 operations (i.e. when no sea rise is given)
    '''
    height_list = []
    area_list = []
    max_alt = 0

    for item in data_array: # find highest altitude in data
        if float(item[2]) > max_alt:
            max_alt = float(item[2])

    step_num = np.linspace(0, max_alt, 100)

    for step in step_num:
        height_list.append(step)

    if approximation == 1: # I split this up for speed reasons. This way it doesn't have to do the check every time it runs the for loop. It's not as neat, but it'll save cycles especially on the bigger files.
        for alt in height_list:
            area = calc_area(alt, mean_vert_dist, mean_horiz_dist, data_array)
            area_list.append(area)
    else:
        for alt in height_list:
            area = tier3_calc_area(alt, mean_vert_dist, mean_horiz_dist, data_array)
            area_list.append(area)

    return height_list, area_list
    

def tier1_disp_result(L, mean_vert, mean_horiz): # shows data for function level 1
    current = calc_area(0, user_vert_dist, user_horiz_dist, data_array)
    absolute = calc_area(L, user_vert_dist, user_horiz_dist, data_array)
    percentage = (absolute/current) * 100
    
    print("First Approximation: At %0.0f metre(s) above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value\n" % (L, absolute, percentage))

    current = tier3_calc_area(0, mean_vert_dist, mean_horiz_dist, data_array)
    absolute = tier3_calc_area(L, mean_vert_dist, mean_horiz_dist, data_array)
    percentage = (absolute/current) * 100
    
    print("Second Approximation: At %0.0f metre(s) above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value\n" % (L, absolute, percentage))
    return True


def tier2_disp_result(): # shows data for function level 2

    height_list_1, area_list_1 = zero_rise(mean_vert_dist, mean_horiz_dist, data_array, 1)
    graph_plot(height_list_1, area_list_1, 1)
    
    height_list_2, area_list_2 = zero_rise(mean_vert_dist, mean_horiz_dist, data_array, 2)
    graph_plot(height_list_2, area_list_2, 2)

    return True


def main(L, mean_vert, mean_horiz, array): # put everything together!

    tier1_disp_result(L, mean_vert_dist, mean_horiz_dist)
    if L == 0:
           tier2_disp_result()


def graph_plot(al, pl, approximation): 
    '''
    Plots data for function level 2. When a zero sea level increase is given, plots the area for a 1% increase in maximum altitude of the land.
    '''
    if approximation == 1:
        plt.title("Sea level rise vs remaining land area (First Approximation)")
    else:
        plt.title("Sea level rise vs remaining land area (Second Approximation)")
    plt.xlabel("Sea level rise (m)")
    plt.ylabel("Remaining land area (km^2)")
    plt.plot(al, pl, "b")
    plt.show()

        
#┌──────────────┐
#│ --- RUN! --- │
#└──────────────┘

main(sea_rise, mean_vert_dist, mean_horiz_dist, data_array)



#┌────────────────┐
#│ --- HCD4T ---  │
#└────────────────┘

#datafile = open("data_files/sydney250m.txt","r")
#mean_vert_dist = 0.278
#mean_horiz_dist = 0.231
#sea_rise = 13.000
