
INT_MAX = 2147483647
INT_MIN = -2147483648

def clamp_sub(a, b):
    if a > 0 and b < 0 and a - b < 0:
        result = INT_MAX
    elif a < 0 and b > 0 and a - b > 0:
        result = INT_MIN
    else:
        result = a - b

    return result
