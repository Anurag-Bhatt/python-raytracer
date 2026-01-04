import numpy as np

def write_color(pixel_color: np.ndarray) -> tuple[int, int, int]:
    
    gamma_corrected = np.sqrt(np.clip(pixel_color, 0.0, 0.999))

    rbyte, gbyte, bbyte = (gamma_corrected * 256).astype(int)
    return rbyte, gbyte, bbyte