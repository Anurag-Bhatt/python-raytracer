# pyright: reportOptionalSubscript=false
from PIL import Image
from math import sqrt

from vec3 import Vec3, unit_vector, dot
from ray import Ray
from color import write_color

print("Raytracing")

# returns true if ray hit sphere
def hit_sphere(center:Vec3, radius:float, r:Ray):
    origin_to_center = center - r.origin
    a = r.direction.length_squared()
    h = dot(r.direction, origin_to_center)
    c = origin_to_center.length_squared() - (radius * radius)

    discrimant = h*h - (a*c)
    if discrimant < 0:
        return -1.0
    else:
        return (h-(sqrt(discrimant)/a))

# Returns color of ray
def ray_color(r:Ray):
    
    t = hit_sphere(Vec3(0, 0, -1), 0.5, r)
    if t > 0.0:
        normal = unit_vector(r.at(t) - Vec3(0, 0, -1))
        return 0.5 * (normal + Vec3(1,1,1))

    unit_direction:Vec3 = unit_vector(r.direction)
    a = 0.5 * (unit_direction.y + 1)
    return (1.0-a)*Vec3(1.0, 1.0, 1.0) + a*Vec3(0.5, 0.7, 1.0)

def main():
    
    aspect_ratio = 16.0 / 9.0
    image_width:int = 400

    image_height = int(image_width / aspect_ratio)
    image_height = image_height if image_height > 1 else 1

    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (image_width / image_height)
    camera_center = Vec3(0, 0, 0)

    viewport_u = Vec3(viewport_width, 0, 0)
    viewport_v = Vec3(0, -viewport_height, 0)

    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    viewport_upper_left = camera_center - Vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
    pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    im = Image.new("RGB", (image_width, image_height))
    pixels= im.load()
    
    for i in range(image_width):
        for j in range(image_height):

            pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
            ray_direction = pixel_center - camera_center

            #pixel = Vec3(float(i)/(image_width-1), float(j)/(image_height-1), 0)
            r = Ray(camera_center, ray_direction)
            r, g, b = write_color(ray_color(r))
            pixels[i,j] = (r, g, b)
    
    im.show()

main()