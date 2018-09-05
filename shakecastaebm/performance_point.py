import math

def performance_point(capacity, demand):
    intersections = find_intersections(capacity, demand, 'disp', 'acc')

    # calculate periods for intersections
    for intersection in intersections:
        period = math.sqrt(intersection['disp'] / intersection['acc'] /  9.779738)
        intersection['period'] = round(period*100) / 100

    if len(intersections) == 1:
        return intersections

    # determine performance point from multiple intersections
  
def find_intersections(line1, line2, x='x', y='y'):
    intersections = []
    line1_idx = 0
    line2_idx = 0
    while line1_idx < len(line1) - 1 and line2_idx < len(line2) - 1:
        seg1 = [line1[line1_idx], line1[line1_idx + 1]]
        seg2 = [line2[line2_idx], line2[line2_idx + 1]]
        
        intersection = get_intersection(seg1, seg2, x, y)
        if intersection is not False:
            intersections += [intersection]
        
        if seg1[1][x] == seg2[1][x]:
            line1_idx += 1
            line2_idx += 1
        elif seg1[1][x] < seg2[1][x]:
            line1_idx += 1
        else:
            line2_idx += 1

    return intersections

def get_intersection(seg1, seg2, x, y):
    # seg1 and seg2 are 2d arrays 
    # [ {x: x1_val,  y: y1_val}, {x: x2_val, y: y2_val} ]
    dx1 = seg1[1][x] - seg1[0][x]
    dx2 = seg2[1][x] - seg2[0][x]
    dy1 = seg1[1][y] - seg1[0][y]
    dy2 = seg2[1][y] - seg2[0][y]

    # check for parallel segs
    if (dx2 * dy1 - dy2 * dx1) == 0:
        # The segments are parallel.
        return False
    
    s = ((dx1 * (seg2[0][y] - seg1[0][y]) + dy1 * (seg1[0][x] - seg2[0][x])) /
                (dx2 * dy1 - dy2 * dx1))
    t = ((dx2 * (seg1[0][y] - seg2[0][y]) + dy2 * (seg2[0][x] - seg1[0][x])) /
                (dy2 * dx1 - dx2 * dy1))
    
    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        return {x: seg1[0][x] + t * dx1, y: seg1[0][y] + t * dy1}
    else:
      return False

def weight_intersections(intersections, line1, line2):
    '''
    TODO: WRITE THIS FUNCTION

    In the event of multiple intersections, the performance point
    should be a weighted average of the outer intersections
    '''
    #on_top = []
    #inter_idx = 0
    #for idx in range(len(line1)):
    #    if line1[idx]['x'] > intersections[inter_idx]['x']:
    #        on_top += [line1] if line1[idx]['']
    return