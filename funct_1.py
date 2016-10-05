#user inputs datafile, L, mean_vert_disp, and mean_horiz_disp


def calc_area(L, mean_vert, mean_horiz):
	"calculates the area above sea level L, with mean vertical and horizontal spacing given"
	count = 0
	for line in datafile:
		if line[2] >= 0:
			count += 1
	area = count*mean_vert*mean_horiz
	return area



current = calc_area(0, mean_vert_disp, mean_horiz_disp)
absolute = calc_area(L, mean_vert_disp, mean_horiz_disp)
percentage = absolute/current * 100


print("At %s metres above sea level, there will be %s kilometres of land area, which is %s percent of the current value" % (L, absolute, percentage))