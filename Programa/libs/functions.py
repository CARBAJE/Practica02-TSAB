import numpy as np
from PIL import Image
from scipy.stats import entropy

def ImgRGB2Gray(file):
    """ Convierte una imagen RGB a escala de grises y la normaliza en el rango [0,1] """
    img_rgb = Image.open(file)
    img_gray = img_rgb.convert('L')

    # Convertir a numpy array y normalizar
    img_rgb = np.array(img_rgb, dtype=np.float64) / 255.0
    img_gray_norm = np.array(img_gray, dtype=np.float64) / 255.0
    
    return img_rgb, img_gray_norm

def sigmoid_transformation(x, alpha, delta):
    """ Aplica una transformación sigmoide a la imagen """
    x = np.clip(x - delta, -500, 500)  # Evita overflow en np.exp()
    return 1 / (1 + np.exp(-alpha * x))

def apply_sigmoid(img, alpha, delta):
    """ Aplica la transformación sigmoide y normaliza la imagen en [0,1] """
    img_with_contrast = sigmoid_transformation(img, alpha, delta)
    
    min_val, max_val = np.min(img_with_contrast), np.max(img_with_contrast)
    if max_val == min_val:  # Evita división por cero
        return np.zeros_like(img_with_contrast, dtype=np.float64)
    
    return (img_with_contrast - min_val) / (max_val - min_val)

def std_img(img, X):
    """ Calcula la desviación estándar de la imagen tras la transformación sigmoide """
    alpha, delta = X
    img_new = apply_sigmoid(img, alpha, delta)
    return - np.std(img_new)

def Entropy(img, X):
    """ Calcula la entropía de la imagen tras la transformación sigmoide """
    alpha, delta = X
    img_new = apply_sigmoid(img, alpha, delta)

    hist, _ = np.histogram(img_new, bins=256, range=(0, 1), density=True)
    #hist = hist[hist > 0]  # Evita valores cero en el logaritmo
    
    return - entropy(hist, base=2) if hist.sum() > 0 else 0  # Evita NaN si histograma está vacío

def f1(x):
    """Funcion del LABORATORIO: ALGORITMO GENÉTICO CON PENALIZACIÓN"""
    return 4*(x[0]-3)**2 + 3*(x[1]-3)**2

def g1_1(x):
    """Restricción 1 del LABORATORIO: ALGORITMO GENÉTICO CON PENALIZACIÓN"""
    return 2*x[0] + x[1] - 2

def g1_2(x):
    """Restricción 2 del LABORATORIO: ALGORITMO GENÉTICO CON PENALIZACIÓN"""
    return 3*x[0] + 4*x[1] - 6

def f_finanzas(x):
    """Función objetivo para el problema de finanzas"""
    return -((0.2 * x[0]) + (0.42 * x[1]) + (1 * x[2]) + (0.5 * x[3]) + (0.46 * x[4]) + (0.3*x[5]))

def h1_finanzas(x):
    return 1 - np.sum(x)