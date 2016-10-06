# user inputs datafile, L, mean_vert_disp, and mean_horiz_disp
#┌──────────────┐
#│ --- Init --- │
#└──────────────┘

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

def calc_area(L, mean_vert, mean_horiz):
    """
    calculates the area above sea level L, with mean vertical and horizontal spacing given
    """
    count = 0
    for line in datafile:
        data_list.append(line.split())
    for item in data_list:
        if float(item[2]) >= L:
            count += 1
    area = count * mean_vert * mean_horiz
    return area

def disp_result():

    current = calc_area(0, mean_vert_dist, mean_horiz_dist)
    print(current)
    absolute = calc_area(sea_rise, mean_vert_dist, mean_horiz_dist)
    print(absolute)
    percentage = absolute/current * 100

    print("At %0.0f metres above sea level, there will be %0.3f square kilometres of land, which is %0.3f percent of the current value" % (sea_rise, absolute, percentage))

disp_result()

#┌────────────────┐
#│ --- HCD4T ---  │
#└────────────────┘

#datafile = open("data_files/sydney250m.txt","r")
#mean_vert_dist = 0.278
#mean_horiz_dist = 0.231
#sea_rise = 13.000
