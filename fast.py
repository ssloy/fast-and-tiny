import matplotlib.pyplot as plt
import numpy as np

def box_intersect(bmin, bmax, ray_origins, ray_directions):
    ray_directions = np.where(np.abs(ray_directions)<1e-3, 1e-3, ray_directions)
    sign_mask = np.sign(ray_directions)
    entries = (np.where(sign_mask == 1, bmin, bmax) - ray_origins) / ray_directions
    t, t_axes = np.max(entries, axis=1), np.argmax(entries, axis=1)
    points = ray_origins + t[:, np.newaxis]*ray_directions
    hit = (t>0) & np.all((points>bmin-1e-3) & (points<bmax+1e-3), axis=1)
    normals = np.column_stack( [ np.where(t_axes[hit] == i, -sign_mask[hit, i], 0) for i in range(3) ] )
    return hit, points[hit], normals

def sphere_intersect(center, radius, ray_origins, ray_directions):
    z = center-ray_origins
    proj = np.sum(ray_directions*z, axis=1)
    delta = radius**2 + proj*proj - np.sum(z**2, axis=1)
    t = proj[delta>0] - np.sqrt(delta[delta>0])
    hit = np.zeros(ray_origins.shape[0], dtype=bool)
    hit[delta>0] = t>0
    points  = ray_origins[hit] + t[t>0, np.newaxis]*ray_directions[hit]
    return hit, points, (points - center) / radius

def scene_intersect(ray_origins, ray_directions): # find closest point in the scene along the ray
    nrays   = ray_origins.shape[0]
    nearest = np.full(nrays, np.inf)     # the (squared) distance from the ray origin to the nearest point in the scene
    points  = np.zeros_like(ray_origins) # nearest point,         \
    normals = np.zeros_like(ray_origins) # its normal,            | the information about the intersection points we want to return
    colors  = np.zeros_like(ray_origins) # color of the surface,  | (junk values if no intersection)
    hot     = np.full(nrays, False)      # hot or not             /
    for o in [ {'center': np.array([  6,   0,  7]), 'radius':  2, 'color': np.array([1., .4, .6]), 'hot': False}, # description of the scene:
               {'center': np.array([2.8, 1.1,  7]), 'radius': .9, 'color': np.array([1., 1., .3]), 'hot': False}, # three spheres and two boxes
               {'center': np.array([  5, -10, -7]), 'radius':  8, 'color': np.array([1., 1., 1.]), 'hot': True},  # one of the spheres is "hot" (incandescent)
               {'min': np.array([3, -4, 11]), 'max': np.array([ 7,   2, 13]), 'color': np.array([.4, .7, 1.]), 'hot': False},
               {'min': np.array([0,  2,  6]), 'max': np.array([11, 2.2, 16]), 'color': np.array([.6, .7, .6]), 'hot': False} ]:
        if 'center' in o: # is it a sphere or a box?
            hit,p,n = sphere_intersect(o['center'], o['radius'], ray_origins, ray_directions)
        else:
            hit,p,n = box_intersect(o['min'], o['max'], ray_origins, ray_directions)
        z = (p-ray_origins[hit])
        dist = np.sum(z**2, axis=1)
        closer = dist<nearest[hit] # closest points so far
        hiti = np.where(hit)[0]
        nearest[hiti[closer]] = dist[closer]
        points[hiti[closer]]  = p[closer]
        normals[hiti[closer]] = n[closer]
        colors[hiti[closer]]  = o['color']
        hot[hiti[closer]]     = o['hot']
    return (nearest<np.inf),points,normals,colors,hot

def normalized(vectors):
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

def reflect(vectors, normals):
    return normalized(vectors - 2*np.sum(vectors*normals, axis=1, keepdims=True)*normals + np.random.uniform(low=-1., high=1., size=vectors.shape)/6.)

def trace(ray_origins, ray_directions, depth):
    if depth>maxdepth: return np.full(ray_origins.shape, ambient_color)
    hit,points,normals,colors,hot = scene_intersect(ray_origins, ray_directions)
    colors[~hit] = ambient_color
    bounce = hit & ~hot
    colors[bounce] = colors[bounce] * trace(points[bounce], reflect(ray_directions[bounce], normals[bounce]), depth+1)
    return colors

width, height, ambient_color = 640, 480, np.array([.5]*3)
focal, azimuth  = 500, 30*np.pi/180
nrays, maxdepth = 10, 3

x, z = np.tile(np.linspace(-width/2, width/2, width), height), np.full(width*height, focal)
eye = np.zeros((width*height,3))
rays = normalized(np.column_stack((
                np.cos(azimuth)*x + np.sin(azimuth)*z,                       # dir x
                np.repeat(np.linspace(-height/2, height/2, height), width),  # dir y
               -np.sin(azimuth)*x + np.cos(azimuth)*z)))                     # dir z
image = np.zeros((height*width, 3))
for r in range(nrays):
    print("Pass %d/%d" % (r + 1, nrays))
    image += trace(eye, rays, 0)
plt.imsave('result.png', np.clip(image.reshape(height, width, 3)/nrays, 0, 1))
