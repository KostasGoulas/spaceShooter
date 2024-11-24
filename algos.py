import math
def is_point_inside_box( point, box_point, box_width, box_heigth ):
    return (point[0] >= box_point[0] and point[0] <= box_point[0]+box_width) and (point[1] >= box_point[1] and point[1] <= box_point[1]+box_heigth)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def dv( pos1, pos2 ):
    return ( pos2[0] - pos1[0], pos2[1] - pos1[1] )

def normalize( p ):
    len = math.sqrt(p[0]*p[0] + p[1]*p[1])
    return ( p[0]/len, p[1]/len )