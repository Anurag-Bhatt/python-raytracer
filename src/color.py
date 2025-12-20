from vec3 import Vec3

Color = Vec3

def write_color(pixel_color: Color) -> tuple[int, int, int]:
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    rbyte = int(255.999 * r)
    gbyte = int(255.999 * g)
    bbyte = int(255.999 * b)

    return rbyte, gbyte, bbyte