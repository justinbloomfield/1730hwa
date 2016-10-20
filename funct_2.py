#┌──────────────┐
#│ --- Init --- │
#└──────────────┘

import re # for regex checking 
import numpy as np # linspace, as range() can't use floats
import matplotlib.pyplot as plt # for graphing

# user inputs datafile, L, mean_vert_disp, and mean_horiz_disp
#assignment of user inputs
path = input("Please enter the path to the desired data file for analysis: ")
mean_vert_dist = float(input("Please enter the mean vertical spacing for the provided data file: "))
mean_horiz_dist = float(input("Please enter the mean horizontal spacing for the provided data file: "))
sea_rise = float(input("Please enter a sea level height for remaining land area analysis: ")) #maybe an exception catcher here if we decide we want to account for user to not enter anything


#assignment of file object to user-provided file
datafile = open(path, 'r')
data_array = []

#┌───────────────────┐
#│ --- Functions --- │
#└───────────────────┘

def get_info():
    """Fetches each line in YXZ file.
    
    Retrieves each line in the YXZ file, which pertain to the latitude, longitude and
    elevation of a sample point. Splits the values for each line across whitespace, 
    and appends the three values for each line to an array called data_array. 
    """
    for line in datafile:
        data_array.append(line.split())

def validate(path): # maybs change this to read from data_array so the file doesn't have to be scanned twice, for speed. Not imperative.
     """Checks whether the filepath refers to a valid YXZ format file. 
    
    Retrieves the file located at the given filepath. Opens that file, and checks that
    the file contains the correct number of entries per line, and only valid characters
    in each entry. If the file is found to be invalid, the program quits and states the
    relevant error.
    
    Args:
        testing_file: The path to the file for validation.
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

    
def calc_area(L, mean_vert, mean_horiz, array):
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
    area = 0
    count = 0
    for item in array:
        if float(item[2]) > L:
            count += 1

    area = count * mean_vert * mean_horiz
    return area
    
def zero_rise(L, mean_vert, mean_horiz, array): #sea rise, array of data, height list and area list
    """Calculates land areas for a range of sea level increases
    
    Generates the remaining land areas, given sea level rises 
    at 1% increments of the highest elevation in the datafile. 
    
    Args:
       mean_vert: The numeric value for mean vertical spacing of
           data values in datafile.
       mean_horiz: The numeric value for mean horizontal spacing 
           of data values in datafile.
       array: The array containing line-split data values
           from the input datafile. 
       approximation: an integer value of 1 or 2, so that remaining 
           land areas are calculated using the respective
           area approximation function.
     
     Returns:
         height_list: A list of elevations, representing the elevation
            at 1% increments of the highest elevation in datafile.
         area_list: A list of areas, calculated for the relevant 
            approximation, which match the respective elevation value
            in height_list. 
    """
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

def tier1_disp_result(L, mean_vert, mean_horiz): 
    """Displays output for functionality level 1.
    
    Prints the required output for both the first and second approximations    
    Args:
        L: A numeric value representing sea level rise. 
        mean_vert: The numeric value for mean vertical spacing of
            data values in datafile.
        mean_horiz: The numeric value for mean horizontal spacing 
            of data values in datafile.   
    """
    current = calc_area(0, mean_vert, mean_horiz, data_array)
    absolute = calc_area(L, mean_vert, mean_horiz, data_array)
    percentage = (absolute/current) * 100
    
    print("At %0.0f metre(s) above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value" % (L, absolute, percentage))
    return True

def tier2_disp_result(L, mean_vert, mean_horiz, array): 
    """Plots graphs for functionality level 2.
    
    Displays two graphs for functionality level 2, one for each of 
    the first and second approximations.
    """
    
    height_list, area_list = zero_rise(L, mean_vert, mean_horiz, array)
    graph_plot(height_list, area_list)

    return True

def main(L, mean_vert, mean_horiz, array): 
    """Decides which functionality level (1 or 2) is required.
    
    Args:
        L: A numeric value representing sea level rise. 
        mean_vert: The numeric value for mean vertical spacing of
            data values in input data file.
        mean_horiz: The numeric value for mean horizontal spacing 
            of data values in input data file.
        array: The array containing line-split data values
            from the input data file.
    """
    if L == 0:
        tier2_disp_result(L, mean_vert, mean_horiz, array)
    else:
        tier1_disp_result(L, mean_vert, mean_horiz)

def graph_plot(heights, areas): 
    """Generates graph for functionality level 2.
    
    Generates a graph for sea level rise against remaining sea level rise, 
    for the respective approximation provided.
    
    Args:
        heights: The list of heights, at 1% increments of the highest elevation
        in datafile.
        areas: The remaining land area associated with each elevation level in
        heights.
    """
    plt.title("Sea level rise vs remaining land area")
    plt.xlabel("Sea level rise (m)")
    plt.ylabel("Remaining land area (km^2)")
    plt.plot(heights, areas, "b")
    plt.show()

        
#┌──────────────┐
#│ --- RUN! --- │
#└──────────────┘

main(sea_rise, mean_vert_dist, mean_horiz_dist, data_array)
