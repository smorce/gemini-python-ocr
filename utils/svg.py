def average(a: float, b: float) -> float:
    return (a + b) / 2

def get_svg_path_from_stroke(points: list[list[float]], closed=True) -> str:
    length = len(points

    if length < 4:
        return ""

    a = points[0]
    b = points[1]
    c = points[2]

    result = f"M{a[0]:.2f},{a[1]:.2f} Q{b[0]:.2f},{b[1]:.2f} {average(b[0], c[0]):.2f},{average(b[1], c[1]):.2f} T"

    for i in range(2, length - 1):
        a = points[i]
        b = points[i + 1]
        result += f"{average(a[0], b[0]):.2f},{average(a[1], b[1]):.2f} "

    if closed:
        result += "Z"

    return result
