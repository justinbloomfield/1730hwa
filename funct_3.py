#┌──────────────┐
#│ --- Init --- │
#└──────────────┘

import re # for regex checking 
import numpy as np # linspace, as range() can't use floats
import matplotlib.pyplot as plt # for graphing
import math as mth # for cos and radians -> degrees conversion

# user inputs datafile, L, mean_vert_disp, and mean_horiz_disp
#assignment of user inputs
path = input("Please enter the path to the desired data file for analysis: ")
sea_rise = float(input("Please enter a sea level height for remaining land area analysis: ")) #maybe an exception catcher here if we decide we want to account for user to not enter anything
#assignment of file object to user-provided file
datafile = open(path, 'r')
data_array = []

#┌───────────────────┐
#│ --- Functions --- │
#└───────────────────┘


def get_info(): # gets data from file and enters it into an array
    for line in datafile:
        data_array.append(line.split())


def validate(testing_file): # maybs change this to read from data_array so the file doesn't have to be scanned twice, for speed. Not imperative.
    """
    Takes the path to the file, and checks that it contains the correct number of entries per line and only valid characters. Quits when file is found to be invalid, stating the error.
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

    diff_list = []
    col_entries = []
    abs_float = lambda x: abs(float(x))
 
    for entry in data_array:
        col_entries.append(entry[index])

    for num in range(1, len(col_entries)):
        if index == 1: # calculating horizontal spacing
            difference = abs_float(col_entries[num]) - abs_float(col_entries[num-1]) # this was using arc_calc(), but that wasn't working. 
        else:
            difference = abs_float(col_entries[num]) - abs_float(col_entries[num-1])
        
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
    for item in array:
        if float(item[2]) > L:
            count += 1
    area = count * mean_vert * mean_horiz
    return area    
    
def tier3_calc_area(L, mean_horiz_dist, mean_vert_dist, array): # calculates area using arc degrees
    lat_list = list()
    width_list = list()
    height_list = list()
    area_list = list()
    total_area = 0

    for item in array:
        if float(item[2]) > L:
            lat_list.append(float(item[0]))
            width_list.append(float(item[1]))
            width = 40075/360 * mth.cos(mth.radians(float(item[0])))*mean_horiz_dist
            height = 40075/360 * mean_vert_dist
            area_list.append(width*height)

    total_area = sum(area_list)
    print(total_area)
    return total_area
    
def zero_rise(mean_vert, mean_horiz, array, approximation): 
    '''
    performs function level 2 operations (i.e. when no sea rise is given)
    '''
    height_list = []
    area_list = []
    max_alt = 0

    for item in array: # find highest altitude in data
        if float(item[2]) > max_alt:
            max_alt = float(item[2])

    step_num = np.linspace(0, max_alt, 100)

    for step in step_num:
        height_list.append(step)

    for alt in height_list:
        if approximation == 1:
            area = calc_area(alt, mean_vert, mean_horiz, array)
        else:
            area = tier3_calc_area(alt, mean_vert_mean_horiz, array)
        area_list.append(area)

    return height_list, area_list

    
    
def tier1_disp_result(L, mean_vert, mean_horiz): # shows data for function level 1
    current = calc_area(0, mean_vert, mean_horiz, data_array)
    absolute = calc_area(L, mean_vert, mean_horiz, data_array)
    percentage = (absolute/current) * 100
    
    print("At %0.0f metre(s) above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value" % (L, absolute, percentage))
    return True

    current = tier3_calc_area(0, mean_vert, mean_horiz, data_array)
    absolute = tier3_calc_area(L, mean_vert, mean_horiz, data_array)
    percentage = (absolute/current) * 100
    
    print("At %0.0f metre(s) above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value" % (L, absolute, percentage))
    return True

def tier2_disp_result(): # shows data for function level 2

    height_list_1, area_list_1 = zero_rise(mean_vert, mean_horiz, array, 1)
    graph_plot(height_list_1, area_list_1)
    
    height_list_2, area_list_2 = zero_rise(mean_vert_dist, mean_horiz_dist, 2)
    graph_plot(height_list_2, area_list_2)

    return True


def main(L, mean_vert, mean_horiz, array): # put everything together!
    empty_L = False

    if L == 0:
        empty_L = True
    #tier3_disp_result(L, mean_horiz_dist, mean_vert_dist, array)
    #if empty_L == True:
    #    height_list, area_list = zero_rise(L, mean_vert, mean_horiz, array)
    #    graph_plot(height_list, area_list)
    #else:
    tier1_disp_result(L, mean_vert, mean_horiz)
    tier2_disp_result()
    #invoke function to calculate tier 3

def graph_plot(al, pl): 
    '''
    Plots data for function level 2. When a zero sea level increase is given, plots the area for a 1% increase in maximum altitude of the land.
    '''
    plt.title("Sea level rise vs remaining land area")
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
