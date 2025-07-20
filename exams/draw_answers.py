from PIL import Image, ImageDraw

# Gốc và khoảng cách
START_X = 267
START_Y = 1286
DX = 98
DY = 60
DIAMETER = 20  # ~0.5cm nếu DPI ~100

# Map A/B/C/D → 0/1/2/3
CHOICE_MAP = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

def parse_answers(answer_list):
    coords = []
    for ans in answer_list:
        question = int(ans[:-1])  # 1, 2, ...
        choice = ans[-1]          # A, B, ...
        x = START_X + CHOICE_MAP[choice] * DX
        y = START_Y + (question - 1) * DY
        coords.append((x, y))
    return coords

def draw_circles_on_form(answer_list, input_path, output_path):
    img = Image.open(input_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    coords = parse_answers(answer_list)
    r = DIAMETER // 2

    for (x, y) in coords:
        draw.ellipse((x - r, y - r, x + r, y + r), fill="black")

    img.save(output_path)
