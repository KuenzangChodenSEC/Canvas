import tkinter as tk

# ==========================================
# GROUP 5: PEDESTRIAN CROSSING SIMULATOR
# ==========================================

WIDTH = 489
HEIGHT = 694

root = tk.Tk()
root.title("Group 5 - Pedestrian Crossing Simulator")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="white",
    highlightthickness=0
)
canvas.pack()

# ==========================================
# COLORS
# ==========================================

WHITE = "#FFFFFF"
ROAD = "#41434E"
YELLOW = "#FFAD18"
WINDOW = "#55BBD0"
GREEN = "#159D4A"
BLUE = "#087AC1"
SKIN = "#FFD1A0"
BLACK = "#242424"

# ==========================================
# SIMULATION SETTINGS
# ==========================================

CAR_SPEED = 1.2
CAR_SCALE_SPEED = 0.007
BOY_SPEED = 2.5

FRAME_DELAY = 30
YELLOW_TRANSITION_FRAMES = 35
GREEN_WAIT_FRAMES = 12

ROAD_CENTER = WIDTH / 2

# Car begins in the distance on the road
car_y = 276
car_scale = 0.35
car_x = ROAD_CENTER - 80 * car_scale

# Car stopping point before zebra crossing
STOP_Y = 330
STOP_SCALE = 0.73

# Boy starts outside the left edge
boy_x = -45
boy_y = 310
boy_visible = False

car_stopped = False
animation_running = True

# APPROACH -> CROSSING -> YELLOW_BEFORE_GO
# -> GREEN_BEFORE_DRIVE -> DRIVE_AWAY
state = "APPROACH"
transition_frames = 0

# ==========================================
# DRAW BACKGROUND AND FULL-WIDTH ROAD
# ==========================================

def draw_background():
    canvas.create_rectangle(
        0, 0, WIDTH, HEIGHT,
        fill=WHITE,
        outline=WHITE
    )

    # Perspective road fills the whole foreground
    canvas.create_polygon(
        0, 430,
        168, 276,
        330, 276,
        WIDTH, 430,
        WIDTH, HEIGHT,
        0, HEIGHT,
        fill=ROAD,
        outline=ROAD
    )

    # Zebra crossing stripes across the foreground road
    stripes = [
        [0, 435, 16, 435, 0, 451],
        [29, 434, 49, 434, 0, 474, 0, 451],
        [61, 434, 82, 434, 35, 474, 13, 474],
        [95, 434, 116, 434, 70, 474, 48, 474],
        [129, 434, 150, 434, 105, 474, 83, 474],
        [164, 434, 185, 434, 141, 474, 119, 474],
        [198, 434, 219, 434, 176, 474, 154, 474],
        [232, 434, 253, 434, 211, 474, 189, 474],
        [266, 434, 287, 434, 246, 474, 224, 474],
        [300, 434, 321, 434, 281, 474, 259, 474],
        [334, 434, 355, 434, 316, 474, 294, 474],
        [368, 434, 389, 434, 351, 474, 329, 474],
        [402, 434, 423, 434, 386, 474, 364, 474],
        [436, 434, 457, 434, 421, 474, 399, 474],
        [470, 434, 489, 434, 456, 474, 434, 474],
        [489, 451, 489, 474, 469, 474]
    ]

    for points in stripes:
        canvas.create_polygon(
            points,
            fill=WHITE,
            outline=WHITE
        )

    # Left traffic-light pole
    canvas.create_rectangle(
        21, 253, 33, 410,
        fill="#9DA4AA",
        outline="#9DA4AA"
    )
    canvas.create_rectangle(
        19, 322, 37, 406,
        fill="#8D959B",
        outline="#8D959B"
    )

    # Right traffic-light pole
    canvas.create_rectangle(
        459, 253, 478, 410,
        fill="#9DA4AA",
        outline="#9DA4AA"
    )
    canvas.create_rectangle(
        458, 322, 478, 406,
        fill="#8D959B",
        outline="#8D959B"
    )


# ==========================================
# DRAW TRAFFIC LIGHT
# ==========================================

def draw_traffic_light(x, y, signal):
    canvas.create_rectangle(
        x, y, x + 39, y + 84,
        fill="#48505A",
        outline="#48505A"
    )

    colors = {
        "RED": "#FF202A" if signal == "RED" else "#713D40",
        "YELLOW": "#FFB927" if signal == "YELLOW" else "#765E35",
        "GREEN": "#13C45B" if signal == "GREEN" else "#24533A"
    }

    for name, cy in [
        ("RED", y + 10),
        ("YELLOW", y + 34),
        ("GREEN", y + 57)
    ]:
        canvas.create_oval(
            x + 7, cy,
            x + 25, cy + 18,
            fill=colors[name],
            outline="#343B43"
        )


# ==========================================
# DRAW YELLOW CAR
# ==========================================

def draw_yellow_car(x, y, scale):
    def p(value):
        return value * scale

    # Shadow
    canvas.create_oval(
        x + p(3), y + p(105),
        x + p(162), y + p(119),
        fill="#555C60",
        outline="#555C60"
    )

    # Mirrors
    canvas.create_rectangle(
        x + p(1), y + p(39),
        x + p(19), y + p(48),
        fill="#7F9295",
        outline="#7F9295"
    )
    canvas.create_rectangle(
        x + p(145), y + p(39),
        x + p(164), y + p(48),
        fill="#7F9295",
        outline="#7F9295"
    )

    # Roof
    canvas.create_polygon(
        x + p(40), y + p(1),
        x + p(108), y + p(1),
        x + p(128), y + p(12),
        x + p(21), y + p(12),
        fill="#FFB52A",
        outline="#FFB52A"
    )

    # Windshield
    canvas.create_polygon(
        x + p(21), y + p(12),
        x + p(128), y + p(12),
        x + p(138), y + p(47),
        x + p(12), y + p(47),
        fill=WINDOW,
        outline="#E6A21A",
        width=2
    )

    # Windshield reflections
    canvas.create_line(
        x + p(57), y + p(16),
        x + p(44), y + p(45),
        fill="#3996AD",
        width=max(1, int(scale * 2))
    )
    canvas.create_line(
        x + p(99), y + p(16),
        x + p(86), y + p(45),
        fill="#3996AD",
        width=max(1, int(scale * 2))
    )

    # Main yellow body
    canvas.create_polygon(
        x + p(13), y + p(47),
        x + p(137), y + p(47),
        x + p(158), y + p(68),
        x + p(158), y + p(98),
        x + p(1), y + p(98),
        x + p(1), y + p(68),
        fill=YELLOW,
        outline="#E89C12",
        width=2
    )

    # Front grille
    canvas.create_rectangle(
        x + p(26), y + p(71),
        x + p(133), y + p(95),
        fill="#AAB7B9",
        outline="#87999E"
    )

    for line_y in [75, 80, 85, 90]:
        canvas.create_line(
            x + p(29), y + p(line_y),
            x + p(130), y + p(line_y),
            fill="#6F858A",
            width=max(1, int(scale))
        )

    # Headlights
    canvas.create_rectangle(
        x + p(1), y + p(68),
        x + p(9), y + p(84),
        fill="#FF653F",
        outline="#FF653F"
    )
    canvas.create_rectangle(
        x + p(150), y + p(68),
        x + p(158), y + p(84),
        fill="#E7E9E8",
        outline="#E7E9E8"
    )

    # Bumper
    canvas.create_rectangle(
        x, y + p(96),
        x + p(159), y + p(105),
        fill="#B8C5C6",
        outline="#A4B0B2"
    )

    # Wheels
    for wx in (15, 125):
        canvas.create_oval(
            x + p(wx), y + p(101),
            x + p(wx + 20), y + p(117),
            fill="#657980",
            outline="#657980"
        )


# ==========================================
# DRAW BOY
# ==========================================

def draw_boy(cx, cy):
    # Backpack
    canvas.create_polygon(
        cx + 12, cy + 40,
        cx + 29, cy + 48,
        cx + 34, cy + 91,
        cx + 20, cy + 97,
        cx + 10, cy + 65,
        fill="#D83237",
        outline="#C6252C"
    )

    # Neck
    canvas.create_rectangle(
        cx - 5, cy + 24,
        cx + 7, cy + 37,
        fill=SKIN,
        outline=SKIN
    )

    # Left leg
    canvas.create_polygon(
        cx - 8, cy + 80,
        cx + 5, cy + 82,
        cx - 4, cy + 119,
        cx - 13, cy + 155,
        cx - 27, cy + 153,
        cx - 20, cy + 117,
        fill=BLUE,
        outline=BLUE
    )

    # Right leg
    canvas.create_polygon(
        cx + 4, cy + 81,
        cx + 16, cy + 80,
        cx + 18, cy + 115,
        cx + 33, cy + 150,
        cx + 20, cy + 155,
        cx + 3, cy + 121,
        fill=BLUE,
        outline=BLUE
    )

    # Shoes
    canvas.create_polygon(
        cx - 27, cy + 151,
        cx - 13, cy + 153,
        cx - 18, cy + 160,
        cx - 39, cy + 160,
        fill="#AF302F",
        outline="#AF302F"
    )
    canvas.create_polygon(
        cx + 20, cy + 151,
        cx + 32, cy + 148,
        cx + 42, cy + 157,
        cx + 39, cy + 161,
        cx + 20, cy + 161,
        fill="#AF302F",
        outline="#AF302F"
    )

    # Green shirt
    canvas.create_polygon(
        cx - 10, cy + 34,
        cx + 9, cy + 33,
        cx + 21, cy + 45,
        cx + 15, cy + 83,
        cx - 15, cy + 83,
        cx - 21, cy + 48,
        fill=GREEN,
        outline=GREEN
    )

    # Left arm
    canvas.create_line(
        cx - 17, cy + 43,
        cx - 24, cy + 65,
        cx - 34, cy + 82,
        fill=SKIN,
        width=7,
        capstyle=tk.ROUND,
        joinstyle=tk.ROUND
    )
    canvas.create_oval(
        cx - 39, cy + 78,
        cx - 28, cy + 87,
        fill=SKIN,
        outline=SKIN
    )

    # Right arm
    canvas.create_line(
        cx + 16, cy + 44,
        cx + 22, cy + 62,
        cx + 18, cy + 81,
        fill=SKIN,
        width=7,
        capstyle=tk.ROUND,
        joinstyle=tk.ROUND
    )
    canvas.create_oval(
        cx + 13, cy + 78,
        cx + 23, cy + 87,
        fill=SKIN,
        outline=SKIN
    )

    # Backpack strap
    canvas.create_line(
        cx + 8, cy + 38,
        cx + 18, cy + 51,
        cx + 23, cy + 77,
        fill="#D83237",
        width=4
    )

    # Face
    canvas.create_oval(
        cx - 16, cy + 3,
        cx + 17, cy + 38,
        fill=SKIN,
        outline="#E6AE83"
    )

    # Ear
    canvas.create_oval(
        cx - 19, cy + 17,
        cx - 13, cy + 26,
        fill=SKIN,
        outline=SKIN
    )

    # Hair
    canvas.create_polygon(
        cx - 16, cy + 18,
        cx - 16, cy + 9,
        cx - 11, cy + 1,
        cx - 2, cy - 2,
        cx + 8, cy + 1,
        cx + 15, cy + 8,
        cx + 18, cy + 16,
        cx + 11, cy + 12,
        cx + 5, cy + 16,
        cx - 2, cy + 13,
        cx - 10, cy + 17,
        cx - 13, cy + 24,
        fill="#3D302C",
        outline="#3D302C"
    )

    # Eyes
    for ex in (cx - 9, cx + 5):
        canvas.create_oval(
            ex, cy + 16,
            ex + 6, cy + 23,
            fill=WHITE,
            outline=WHITE
        )

    canvas.create_oval(
        cx - 6, cy + 18,
        cx - 3, cy + 22,
        fill=BLACK,
        outline=BLACK
    )
    canvas.create_oval(
        cx + 7, cy + 18,
        cx + 10, cy + 22,
        fill=BLACK,
        outline=BLACK
    )

    # Eyebrows
    canvas.create_line(
        cx - 10, cy + 14,
        cx - 3, cy + 13,
        fill="#49342E",
        width=2
    )
    canvas.create_line(
        cx + 4, cy + 13,
        cx + 11, cy + 14,
        fill="#49342E",
        width=2
    )

    # Nose
    canvas.create_line(
        cx + 1, cy + 21,
        cx + 2, cy + 26,
        fill="#D99B76"
    )

    # Smile
    canvas.create_arc(
        cx - 3, cy + 25,
        cx + 9, cy + 32,
        start=190,
        extent=150,
        style=tk.ARC,
        outline="#9D4D3F"
    )


# ==========================================
# RESET CAR TO THE DISTANCE
# ==========================================

def reset_car():
    global car_x, car_y, car_scale

    car_y = 276
    car_scale = 0.35
    car_x = ROAD_CENTER - 80 * car_scale


# ==========================================
# MAIN ANIMATION
# ==========================================

def animate():
    global car_x, car_y, car_scale
    global boy_x, boy_visible
    global car_stopped, state, transition_frames

    if not animation_running:
        return

    canvas.delete("all")
    draw_background()

    # STATE 1: CAR APPROACHES ON THE ROAD
    if state == "APPROACH":
        car_y += CAR_SPEED
        car_scale += CAR_SCALE_SPEED
        car_x = ROAD_CENTER - 80 * car_scale

        # Stop the car before the zebra crossing
        if car_y >= STOP_Y:
            car_y = STOP_Y
            car_scale = STOP_SCALE
            car_x = ROAD_CENTER - 80 * car_scale

            car_stopped = True
            boy_visible = True
            boy_x = -45
            state = "CROSSING"

    # STATE 2: BOY CROSSES FROM LEFT TO RIGHT
    elif state == "CROSSING":
        car_stopped = True
        boy_x += BOY_SPEED

        # Wait until the whole boy leaves the canvas
        if boy_x - 40 > WIDTH:
            boy_visible = False
            transition_frames = 0
            state = "YELLOW_BEFORE_GO"

    # STATE 3: RED CHANGES TO YELLOW
    elif state == "YELLOW_BEFORE_GO":
        car_stopped = True
        transition_frames += 1

        if transition_frames >= YELLOW_TRANSITION_FRAMES:
            transition_frames = 0
            state = "GREEN_BEFORE_DRIVE"

    # STATE 4: GREEN LIGHT, CAR WAITS BRIEFLY
    elif state == "GREEN_BEFORE_DRIVE":
        car_stopped = True
        transition_frames += 1

        if transition_frames >= GREEN_WAIT_FRAMES:
            car_stopped = False
            transition_frames = 0
            state = "DRIVE_AWAY"

    # STATE 5: CAR MOVES FORWARD AGAIN
    elif state == "DRIVE_AWAY":
        car_y += CAR_SPEED
        car_scale += CAR_SCALE_SPEED
        car_x = ROAD_CENTER - 80 * car_scale

        # Reset after the car moves out of view
        if car_y + 119 * car_scale >= HEIGHT:
            reset_car()
            car_stopped = False
            boy_visible = False
            transition_frames = 0
            state = "APPROACH"

    # Draw the car above the road
    draw_yellow_car(car_x, car_y, car_scale)

    # Draw the boy only during crossing
    if boy_visible:
        draw_boy(boy_x, boy_y)

    # Traffic-light signal for each state
    if state == "APPROACH":
        signal = "GREEN"
    elif state == "CROSSING":
        signal = "RED"
    elif state == "YELLOW_BEFORE_GO":
        signal = "YELLOW"
    elif state in ("GREEN_BEFORE_DRIVE", "DRIVE_AWAY"):
        signal = "GREEN"
    else:
        signal = "RED"

    draw_traffic_light(8, 175, signal)
    draw_traffic_light(449, 175, signal)

    root.after(FRAME_DELAY, animate)


# ==========================================
# PAUSE / RESUME
# ==========================================

def toggle_animation(event=None):
    global animation_running

    animation_running = not animation_running

    if animation_running:
        animate()


# ==========================================
# RESTART SIMULATION
# ==========================================

def reset_simulation(event=None):
    global boy_x, boy_visible
    global car_stopped, state, animation_running
    global transition_frames

    reset_car()
    boy_x = -45
    boy_visible = False
    car_stopped = False
    transition_frames = 0
    state = "APPROACH"
    animation_running = True

    animate()


# Keyboard controls:
# Space = Pause / Resume
# R = Restart
root.bind("<space>", toggle_animation)
root.bind("r", reset_simulation)
root.bind("R", reset_simulation)

# Start simulator
animate()
root.mainloop()
