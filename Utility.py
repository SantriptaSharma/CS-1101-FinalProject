from typing import Tuple

def Squared_Distance(a : Tuple[float, float, float], b : Tuple[float, float, float]):
    """Returns the squared distance between two 3D vectors a and b."""
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

def Add_Positions(a : Tuple[float, float, float], b : Tuple[float, float, float]):
    """Adds vector a to vector b and returns the result."""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def Scale_Positions(a : Tuple[float, float, float], n : int):
    """Scales vector a by scalar n and returns the result."""
    return (a[0] * n, a[1] * n, a[2] * n)