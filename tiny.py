import numpy as np
import matplotlib.pyplot as plt

def box_intersect(bmin, bmax, ray_origin, ray_direction):
    ray_direction = np.where(np.abs(ray_direction)<1e-3, 1e-3, ray_direction)                  # avoid division by zero
    entries = (np.where(np.sign(ray_direction) == 1, bmin, bmax) - ray_origin) / ray_direction # here we test against 3 planes (instead of 6), i.e.
    t, t_axis = np.max(entries), np.argmax(entries)                                            # no rendering from the inside of a box
    point = ray_origin + t * ray_direction                                                     # intersection between the ray and the plane
    normal = np.zeros(3)                                                                       # normal at the intersection
    normal[t_axis] = -np.sign(ray_direction[t_axis])                                           # both point and normal contain junk values if no intersection
    return (t>0) and np.all((point>bmin-1e-3) & (point<bmax+1e-3)), point, normal              # check whether the intersection lies in the (eroded) box

def sphere_intersect(center, radius, ray_origin, ray_direction):
    proj = np.dot(ray_direction, center-ray_origin)
    delta = radius**2 + proj**2 - np.dot((center-ray_origin),(center-ray_origin))
    if delta>0 and (t:=proj - np.sqrt(delta)) > 0: # the smallest root suffices (one-sided walls, no rendering from the inside of a sphere)
        point = ray_origin + t * ray_direction
        return True,point,(point-center)/radius    # we have a hit, intersection point, surface normal at the point
    return False,None,None # no intersection

def scene_intersect(ray_origin, ray_direction):
    nearest = np.inf                             # the (squared) distance from the ray origin to the nearest point in the scene
    point,normal,color = None,None,None # the information about the intersection point we want to return
    for o in [ {'center': np.array([  6,   0,  7]), 'radius':  2, 'color': np.array([1., .4, .6])}, # description of the scene:
               {'center': np.array([2.8, 1.1,  7]), 'radius': .9, 'color': np.array([1., 1., .3])}, # two spheres and two boxes
               {'min': np.array([3, -4, 11]), 'max': np.array([ 7,   2, 13]), 'color': np.array([.4, .7, 1.])},
               {'min': np.array([0,  2,  6]), 'max': np.array([11, 2.2, 16]), 'color': np.array([.6, .7, .6])} ]:
        if 'center' in o: # is it a sphere or a box?
            hit,p,n = sphere_intersect(o['center'], o['radius'], ray_origin, ray_direction)
        else:
            hit,p,n = box_intersect(o['min'], o['max'], ray_origin, ray_direction)
        if hit and (d2:=np.dot(p-ray_origin, p-ray_origin))<nearest: # we have encountered the closest point so far
            nearest,point,normal,color = d2,p,n,o['color']
    return nearest<np.inf, point, normal, color # hit or not, intersection point, normal at the point, color of the object

def normalized(vector):
    return vector / np.linalg.norm(vector)

def trace(eye, ray, depth):
    hit,point,normal,color = scene_intersect(eye, ray)             # find closest point along the ray
    if hit: return color
    return ambient_color                                           # no intersection

width, height, ambient_color = 640, 480, np.array([.5]*3)
focal, azimuth  = 500, 30*np.pi/180
maxdepth = 3
image = np.zeros((height, width, 3))
for i in range(height):
    for j in range(width):
        ray = normalized(np.array([j-width/2, i-height/2, focal]))        # emit the ray along Z axis
        ray[0],ray[2] = (np.cos(azimuth)*ray[0] + np.sin(azimuth)*ray[2], # and then rotate it 30 degrees around Y axis
                        -np.sin(azimuth)*ray[0] + np.cos(azimuth)*ray[2])
        image[i, j] += trace(np.zeros(3), ray, 0)
    print("%d/%d" % (i + 1, height))
plt.imsave('result.png', np.clip(image, 0, 1))
