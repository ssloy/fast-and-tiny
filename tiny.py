import numpy as np
import matplotlib.pyplot as plt

def sphere_intersect(center, radius, ray_origin, ray_direction):
    proj = np.dot(ray_direction, center-ray_origin)
    delta = radius**2 + proj**2 - np.dot((center-ray_origin),(center-ray_origin))
    if delta>0 and (t:=proj - np.sqrt(delta)) > 0: # the smallest root suffices (one-sided walls, no rendering from the inside of a sphere)
        point = ray_origin + t * ray_direction
        return True,point,(point-center)/radius    # we have a hit, intersection point, surface normal at the point
    return False,None,None # no intersection

def normalized(vector):
    return vector / np.linalg.norm(vector)

def trace(eye, ray, depth):
    hit,point,normal = sphere_intersect(np.array([6, 0, 7]), 2., eye, ray)
    if hit: return np.array([1., .4, .6])
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
