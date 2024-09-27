def clamp(val, bottom, top):
    if bottom < val < top:
        return val
    return min(bottom, top, key=lambda x: abs(val-x))


def check_in_shape(point, edges):
    count = 0

    for edge in edges:
        xp, yp = point

        (x1, y1), (x2, y2) = edge

        if not (y1 < yp < y2):
            continue

        if max(x1, x2) < xp:
            continue

        x_intercept = x1+((yp-y1)/(y2-y1)*(x2-x1))

        if xp < x_intercept:
            count += 1

    if count == 1:
        return True
    return False

