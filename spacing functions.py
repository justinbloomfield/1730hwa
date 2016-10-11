mean_horiz_dist = spacing(1)
mean_vert_dist = spacing(2)

def spacing(i):
  diff_list = []
  col_entries = []
  for line in datafile:
    col_entries.append(line[i])
  for num in range(len(col_entries)-1):
    difference = col_entries[num] - col_entries[num+1]
    if difference <= 0:
      difference *= -1
    diff_list.append(difference)
  total = 0
  for val in diff_list:
    total += x
    return total
  elem_count = len(diff_list)
  mean_spacing = total/elem_count
  return mean_spacing

