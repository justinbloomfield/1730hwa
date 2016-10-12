####### ------ DO WE NEED TO ACCOUNT FOR NEGATIVE SEA ????

#┌──────────────┐
#│ --- Init --- │
#└──────────────┘

import re # for regex checking 
import numpy as np # linspace, as range() can't use floats
import matplotlib.pyplot as plt # for graphing
import math

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

def spacing(index): # currently not working. Needs to do second approximation as well, which is that arc degree shit.
    diff_list = []
    col_entries = []

    for line in datafile:
        col_entries.append(line[index])

    for num in range(len(col_entries)-1):
        difference = col_entries[num] - col_entries[num+1]
        print(difference)
        if difference <= 0:
            difference *= -1
            diff_list.append(difference)

    total = 0
    for val in diff_list:
        total += x

    elem_count = len(diff_list)
    mean_spacing = total/elem_count
    print(mean_spacing)
    return mean_spacing

def get_info():
    for line in datafile:
        data_array.append(line.split())

def validate(path): # maybs change this to read from data_array so the file doesn't have to be scanned twice, for speed. Not imperative.
    """
    Takes the path to the file, and checks that it contains the correct number of entries per line and only valid characters. Quits when file is found to be invalid, stating the error.
    """
    print("Validating file...")
    valid_chars = re.compile('[0-9\.\-]') # characters 0 through 9 
    with open(path, "r") as test: 
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
    get_info() #when file has passed, get data from file
    return True

# validate file
validate(path)

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
    
def zero_rise(L, mean_vert, mean_horiz, array): #sea rise, array of data, height list and area list
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
        area = calc_area(alt, mean_vert, mean_horiz, array)
        area_list.append(area)

    return height_list, area_list

def tier1_disp_result(L, mean_vert, mean_horiz): # shows data function level 1
    current = calc_area(0, mean_vert, mean_horiz, data_array)
    absolute = calc_area(L, mean_vert, mean_horiz, data_array)
    percentage = (absolute/current) * 100
    
    print("At %0.0f metre(s) above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value" % (L, absolute, percentage))
    return True

def tier2_disp_result(): # shows data for function level 2

    height_list, area_list = zero_rise(L, mean_vert, mean_horiz, array)
    graph_plot(height_list, area_list)

    return True

#def tier3_disp_result(): #shows data for function level 3
    

def tier3_calc(L, mean_horiz, mean_vert,array): #shows data for function level 3 ^M
    latitudes = []
    widths = []
    areas = []
    for item in array:
        if item[2] > L:
            latitudes.append(item[0])
    for lat in latitudes:
        widths.append(((40075/360)*math.cos(lat))*mean_horiz)
    height = (40075/360)*mean_vert
    for width in widths:
        areas.append(width*height) 
    total_area = 0
    for val in areas:
        total_area += val
        return total_area
    #tier3_disp_result()
    

def main(L, mean_vert, mean_horiz, array): # put everything together!
    empty_L = False

    if L == 0:
        empty_L = True

    if empty_L == True:
        height_list, area_list = zero_rise(L, mean_vert, mean_horiz, array)
        graph_plot(height_list, area_list)
    else:
        tier1_disp_result(L, mean_vert, mean_horiz)
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
