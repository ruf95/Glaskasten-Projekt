def mix(x, y, a):
    return (x * (1.0 - a) + y * a)

def saturate(x):
    return min(max(x, 0.0), 1.0)

def clamp(x, a, b):
    return min(max(x, a), b)

def HSVtoRGB(H, S, V):
    K1 = 1.0
    K2 = 2.0/3.0
    K3 = 1.0/3.0
    
    R = abs(((H + K1) % 1) * 6.0 - 3.0)
    G = abs(((H + K2) % 1) * 6.0 - 3.0)
    B = abs(((H + K3) % 1) * 6.0 - 3.0)

    R = 255.0 * V * mix(K1, saturate(R - K1), S)
    G = 255.0 * V * mix(K1, saturate(G - K1), S)
    B = 255.0 * V * mix(K1, saturate(B - K1), S)
    
    return (R, G, B)