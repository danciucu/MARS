def init():
    global user_units, count, array_x, array_y, coef_units, points_x, points_y, points_xyz, no, all_units, max_degree

    no = 9

    user_units = ""
    count = 0
    array_x = []
    array_y = []
    points_x = [0] * no
    points_y = [0] * no
    points_xyz = [0] * no * 3
    coef_units = 0
    max_degree = 0



    all_units = ['km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm']
    all_coef_units = [1/1000000, 1/100000, 1/10000, 1/1000, 1/100, 1/10, 1]

    for i in range(3):
        if user_units == all_units:
            coef_units = all_coef_units[i]
