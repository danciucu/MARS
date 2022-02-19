def init():
    global user_units, count, array_x, array_y, points_x, points_y, points_xyz, no, max_degree, user_degree, units_coef

    no = 9

    user_units = ""
    count = 0
    array_x = []
    array_y = []
    points_x = [0] * no
    points_y = [0] * no
    points_xyz = [0] * no * 3
    max_degree = 0
    user_degree = 0
    units_coef = 0