####### ------ REMEMBER TO CHECK IF WE SHOULD INCLUDE THE 0 SEA LEVEL STUFF IN THE CALCULATION OF CURRENT????????
####### ------ DO WE NEED TO ACCOUNT FOR NEGATIVE SEA ????

#┌──────────────┐
#│ --- Init --- │
#└──────────────┘

import re # for regex checking 
import numpy as np # linspace, as range() can't use floats
#import matplotlib.pyplot as plt # for graphing

# user inputs datafile, L, mean_vert_disp, and mean_horiz_disp
#assignment of user inputs
#path = input("Please enter the path to the desired data file for analysis: ")
#mean_vert_dist = float(input("Please enter the mean vertical spacing for the provided data file: "))
#mean_horiz_dist = float(input("Please enter the mean horizontal spacing for the provided data file: "))
#sea_rise = float(input("Please enter a sea level height for remaining land area analysis: ")) 


#assignment of file object to user-provided file
path = "data_files/sydney250m.txt"
datafile = open(path, 'r')
data_array = []


mean_vert_dist = 0.278
mean_horiz_dist = 0.231
sea_rise = 2
#┌───────────────────┐
#│ --- Functions --- │
#└───────────────────┘

def get_info():
    for line in datafile:
        data_array.append(line.split())

def validate(path): # maybs change this to read from data_array so the file doesn't have to be scanned twice, for speed. Not imperative.
    """
    Takes the path to the file, and checks that it contains the correct number of entries per line and only valid characters. Quits when file is found to be invalid, stating the error.
    """
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
    get_info()
    return True

# validate file
validate(path)

def main(L, mean_vert, mean_horiz):
    """
    calculates the area above sea level L, with mean vertical and horizontal spacing given
    """
    height_list = []
    area_list = []
    empty_L = False
    max_alt = 0
    count = 0

    #for line in datafile:
    #    data_array.append(line.split())

    if L == 0:
        empty_L = True


    for item in data_array:
        if float(item[2]) > L:
            count += 1
        if empty_L == True:
            if float(item[2]) > max_alt:
                max_alt = float(item[2])
            else:
                pass
    area = count * mean_vert * mean_horiz 

    if empty_L == True:
        #step_size = max_alt / 100
        step_num = np.linspace(0, max_alt, 100)
        #print(step_size)
    #    #val = 0
    #    #while val < max_alt:
    #        ### THIS ARE WRONG BURJ KHALIFA       
    #    #val = max_alt
    #     
        for step in step_num: 
            for item in data_array:
                if float(item[2]) > L:
                    area_two = count * mean_vert * mean_horiz
            area_list.append(area_two)
            count += 1

        for step in step_num:
            height = step
            height_list.append(step)
            #calc area for these, then display (maybe a separate function? this one is getting pretty big...)
    #print(area)
    (area_list)
    (height_list)
    return area
    
#def calc_area(L, mean_vert, mean_horiz, data):
#    for item in data:
#        if float(item[2]) > L:
#            count += 1

#    area = count * mean_vert * mean horiz
#    return area
    

def disp_result(L, mean_vert, mean_horiz):
    current = main(0, mean_vert, mean_horiz)
    absolute = main(L, mean_vert, mean_horiz)
    percentage = (absolute/current) * 100
    
    print("At %0.0f metre(s) above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value" % (L, absolute, percentage))

    #percent_list = []
    #for item in area_list:
    #    percentage = (item/area_list[0]) * 100
    #    percent_list.append(percentage)

def graph_plot(hl, pl): 
    '''
    Plots data for function level 2 (this is a shit description and
    should be fixed
    '''
    plt.title("Sea level rise vs remaining land area")
    plt.xlabel("Sea level rise (m)")
    plt.ylabel("Remaining land area (km^2)")
    plt.plot(height_list, percent_list, "b")
    plt.show()

#def tier2_disp_result():
#    for index in range(len(height_list)):
#        printheight = height_list(index)
#        printarea = area_list(index)
#        printpercent = percent_list(index)
#        print("At %0.0f metres above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value" % (printheight, printarea, printpercent))
#        
#tier2_disp_result()
        
#calc_area(mean_vert_dist, mean_horiz_dist)
disp_result(sea_rise, mean_vert_dist, mean_horiz_dist)




#┌────────────────┐
#│ --- HCD4T ---  │
#└────────────────┘

#datafile = open("data_files/sydney250m.txt","r")
#mean_vert_dist = 0.278
#mean_horiz_dist = 0.231
#sea_rise = 13.000
