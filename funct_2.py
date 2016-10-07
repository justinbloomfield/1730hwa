
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
    return True

# validate file
validate(path)

def calc_area(mean_vert, mean_horiz):
    """
    calculates the area above sea level L, with mean vertical and horizontal spacing given
    """
    count = 0
    for line in datafile:
        data_list.append(line.split())
        height_list = []
        area_list = []
    for L in range(max_alt):
        for item in data_list:
            if float(item[2]) > L:
                count += 1
        area = count * mean_vert * mean_horiz
        height_list.append(L)
        area_list.append(area)
    

def disp_result():
    percent_list = []
    for item in area_list:
        percentage = (item/area_list[0]) * 100
        percent_list.append(percentage)

        
#┌───────────────────┐
#│ --- Graphing ---  │
#└───────────────────┘

import matplotlib.pyplot as plt
calc_area(mean_vert_dist, mean_horiz_dist)
disp_results()


plt.title("Sea level rise vs remaining land area")
plt.xlabel("Sea level rise (m)")
plt.ylabel("Remaining land area (km^2)")
plt.plot(height_list, percent_list, "b")
plt.show()



#┌────────────────┐
#│ --- HCD4T ---  │
#└────────────────┘

#datafile = open("data_files/sydney250m.txt","r")
#mean_vert_dist = 0.278
#mean_horiz_dist = 0.231
#sea_rise = 13.000
