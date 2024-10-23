import pygame
import time
from ntcore import NetworkTableInstance
import sys
import pygame.mixer
import os
import math

# Initialize Pygame and Pygame mixer for sound
pygame.init()
pygame.mixer.init()

# Function to safely load a sound file with error handling
def load_sound(file_path):
    if os.path.exists(file_path):
        try:
            return pygame.mixer.Sound(file_path)
        except pygame.error as e:
            print(f"Error loading sound file {file_path}: {e}")
            return None
    else:
        print(f"Sound file {file_path} not found.")
        return None

# Load chime sounds with error handling for missing files
chime1 = load_sound('chime1.mp3')
chime2 = load_sound('chime2.mp3')
chime3 = load_sound('chime3.mp3')

# Get display size
display_info = pygame.display.Info()
screen_width = display_info.current_w - 100
screen_height = display_info.current_h // 2

# Set up the window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame FRC Dashboard")  # Updated window title

# Set up NetworkTables using the publish-subscribe model
ntinst = NetworkTableInstance.getDefault()
ntinst.setServer("127.0.0.1")  # Initial server IP
ntinst.startClient4("Pygame_Dashboard")  # Updated client name

# Get the telemetry table
telemetry_table = ntinst.getTable("telemetry")
fms_info_table = ntinst.getTable("FMSInfo")  # For FMSControlData
# Subscribe telemetry data
ds_r_entry = telemetry_table.getIntegerTopic("DS_R").subscribe(0)
ds_g_entry = telemetry_table.getIntegerTopic("DS_G").subscribe(0)
ds_b_entry = telemetry_table.getIntegerTopic("DS_B").subscribe(0)
ds_largetext_entry = telemetry_table.getStringTopic("DS_largetext").subscribe("")
ds_smalltext_entry = telemetry_table.getStringTopic("DS_smalltext").subscribe("")
ds_largetext_flash_entry = telemetry_table.getBooleanTopic("DS_largetext_flash").subscribe(False)
ds_smalltext_flash_entry = telemetry_table.getBooleanTopic("DS_smalltext_flash").subscribe(False)
ds_terminal_text_entry = telemetry_table.getStringTopic("DS_terminal_text").subscribe("")
ds_toptext_entry = telemetry_table.getStringTopic("DS_toptext").subscribe("")
fms_control_data_entry = fms_info_table.getIntegerTopic("FMSControlData").subscribe(0)
ds_terminal_text_r_entry = telemetry_table.getIntegerTopic("DS_terminal_text_R").subscribe(255)
ds_terminal_text_g_entry = telemetry_table.getIntegerTopic("DS_terminal_text_G").subscribe(255)
ds_terminal_text_b_entry = telemetry_table.getIntegerTopic("DS_terminal_text_B").subscribe(255)
ds_terminal_force_entry = telemetry_table.getBooleanTopic("DS_terminal_force").subscribe(False)
ds_chime_1_entry = telemetry_table.getBooleanTopic("DS_chime_1").subscribe(False)
ds_chime_2_entry = telemetry_table.getBooleanTopic("DS_chime_2").subscribe(False)
ds_chime_3_entry = telemetry_table.getBooleanTopic("DS_chime_3").subscribe(False)

# Read the current values
current_values = {
    "ds_r": ds_r_entry.get(),
    "ds_g": ds_g_entry.get(),
    "ds_b": ds_b_entry.get(),
    "ds_largetext": ds_largetext_entry.get(),
    "ds_smalltext": ds_smalltext_entry.get(),
    "ds_largetext_flash": ds_largetext_flash_entry.get(),
    "ds_smalltext_flash": ds_smalltext_flash_entry.get(),
    "ds_terminal_text": ds_terminal_text_entry.get(),
    "ds_toptext": ds_toptext_entry.get(),
    "fms_control_data": fms_control_data_entry.get(),
    "ds_terminal_text_r": ds_terminal_text_r_entry.get(),
    "ds_terminal_text_g": ds_terminal_text_g_entry.get(),
    "ds_terminal_text_b": ds_terminal_text_b_entry.get(),
    "ds_terminal_force": ds_terminal_force_entry.get(),
    "ds_chime_1": ds_chime_1_entry.get(),
    "ds_chime_2": ds_chime_2_entry.get(),
    "ds_chime_3": ds_chime_3_entry.get()
}

# Publish telemetry data
ds_r_entry_publisher = telemetry_table.getIntegerTopic("DS_R").publish()
ds_g_entry_publisher = telemetry_table.getIntegerTopic("DS_G").publish()
ds_b_entry_publisher = telemetry_table.getIntegerTopic("DS_B").publish()
ds_largetext_entry_publisher = telemetry_table.getStringTopic("DS_largetext").publish()
ds_smalltext_entry_publisher = telemetry_table.getStringTopic("DS_smalltext").publish()
ds_largetext_flash_entry_publisher = telemetry_table.getBooleanTopic("DS_largetext_flash").publish()
ds_smalltext_flash_entry_publisher = telemetry_table.getBooleanTopic("DS_smalltext_flash").publish()
ds_terminal_text_entry_publisher = telemetry_table.getStringTopic("DS_terminal_text").publish()
ds_toptext_entry_publisher = telemetry_table.getStringTopic("DS_toptext").publish()
fms_control_data_entry_publisher = fms_info_table.getIntegerTopic("FMSControlData").publish()
ds_terminal_text_r_entry_publisher = telemetry_table.getIntegerTopic("DS_terminal_text_R").publish()
ds_terminal_text_g_entry_publisher = telemetry_table.getIntegerTopic("DS_terminal_text_G").publish()
ds_terminal_text_b_entry_publisher = telemetry_table.getIntegerTopic("DS_terminal_text_B").publish()
ds_terminal_force_entry_publisher = telemetry_table.getBooleanTopic("DS_terminal_force").publish()
ds_chime_1_entry_publisher = telemetry_table.getBooleanTopic("DS_chime_1").publish()
ds_chime_2_entry_publisher = telemetry_table.getBooleanTopic("DS_chime_2").publish()
ds_chime_3_entry_publisher = telemetry_table.getBooleanTopic("DS_chime_3").publish()

# Set default values if current values do not match (to prevent overwriting preexisting values)
initial_values = {
    "ds_r": 255,
    "ds_g": 255,
    "ds_b": 255,
    "ds_largetext": "Welcome to pygame Dashboard",
    "ds_smalltext": "This is the default status.",
    "ds_largetext_flash": False,
    "ds_smalltext_flash": False,
    "ds_terminal_text": "",
    "ds_toptext": "",
    "fms_control_data": 0,
    "ds_terminal_text_r": 0,
    "ds_terminal_text_g": 0,
    "ds_terminal_text_b": 0,
    "ds_terminal_force": False,
    "ds_chime_1": False,
    "ds_chime_2": False,
    "ds_chime_3": False
}

for key, value in current_values.items():
    if value == initial_values[key]:
        globals()[f"{key}_entry_publisher"].set(initial_values[key])
    else:
        globals()[f"{key}_entry_publisher"].set(current_values[key])

# Edge settings
edge_width = 50

# Flash intervals
flash_interval = 0.25  # Seconds

# Terminal settings
terminal_lines = []  # List to store terminal lines (with color)
terminal_max_lines = 10  # Max number of lines visible in the terminal
last_terminal_text = ""  # Track last text to detect changes
terminal_force_triggered = False  # Latch for force print

# Function to clamp RGB values between 0 and 255
def clamp_rgb_value(value):
    return max(0, min(value, 255))

# Function to invert RGB color values
def invert_color(r, g, b):
    return (255 - r, 255 - g, 255 - b)

# Function to calculate Euclidean distance between two colors
def color_distance(color1, color2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))

# FMSControlData color mappings and FMS attached logic
def get_fms_edge_color(fms_control_data):
    fms_attached_colors = {
        48: (255, 0, 0),   # Red for Disabled
        49: (0, 255, 0),   # Green for Teleop
        51: (0, 0, 255),   # Blue for Auto
        53: (255, 255, 0)  # Yellow for Test
    }
    fms_not_attached_colors = {
        32: (255, 0, 0),   # Red for Disabled
        33: (0, 255, 0),   # Green for Teleop
        35: (0, 0, 255),   # Blue for Auto
        37: (255, 255, 0)  # Yellow for Test
    }
    if fms_control_data in fms_attached_colors:
        return fms_attached_colors[fms_control_data], True  # True means FMS is attached
    elif fms_control_data in fms_not_attached_colors:
        return fms_not_attached_colors[fms_control_data], False  # False means FMS is not attached
    else:
        return (169, 169, 169), False  # Grey for disconnected or unknown

# Function to draw text with optional flashing
def draw_text(screen, text, font, color, center_position, flash, elapsed_time):
    if not flash or int(elapsed_time / flash_interval) % 2 == 0:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_position)
        screen.blit(text_surface, text_rect)

# Function to dynamically adjust font size based on text length and available space
def get_dynamic_font(text, max_width, max_height, base_font_size):
    font_size = base_font_size
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_width, text_height = text_surface.get_size()

    # Adjust font size based on width and height constraints
    while (text_width > max_width or text_height > max_height) and font_size > 10:
        font_size -= 1
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_width, text_height = text_surface.get_size()

    return font

# Function to handle terminal printing with background box if color is too close
def print_terminal(screen, font, terminal_lines, canvas_color, position, max_lines, color_threshold=100):
    for i, (line, color) in enumerate(terminal_lines[:max_lines]):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(topleft=(position[0], position[1] + i * 20))
        
        # Check if text color is too close to canvas color
        if color_distance(color, canvas_color) < color_threshold:
            # Draw a background box with the inverted color of the text
            box_color = invert_color(*color)
            pygame.draw.rect(screen, box_color, text_rect.inflate(10, 10))
        
        # Draw the text on top
        screen.blit(text_surface, text_rect)

# Function to render buttons
def render_button(screen, rect, text, font, color=(200, 200, 200), text_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Border
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Latch state for chime playback
chime1_played = False
chime2_played = False
chime3_playing = False  # State for looping chime 3

# Config Panel Variables
config_panel_active = False
ip_input_active = False
ip_input_text = ""
ip_input_rect = pygame.Rect(screen_width//2 - 150, screen_height//2 - 100, 300, 40)
clear_terminal_button_rect = pygame.Rect(screen_width//2 - 100, screen_height//2, 200, 50)
submit_ip_button_rect = pygame.Rect(screen_width//2 - 100, screen_height//2 + 60, 200, 50)
close_config_button_rect = pygame.Rect(screen_width//2 + 160, screen_height//2 - 100, 30, 30)

# Config Button in Bottom-Right Corner
config_button_rect = pygame.Rect(screen_width - 110, screen_height - 60, 100, 50)

# Font for buttons and input
button_font = pygame.font.Font(None, 24)
config_font = pygame.font.Font(None, 32)

# Main loop
running = True
clock = pygame.time.Clock()
start_time = time.time()

while running:
    elapsed_time = time.time() - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                config_panel_active = not config_panel_active
                ip_input_active = False  # Reset input field when toggling panel

            if config_panel_active and ip_input_active:
                if event.key == pygame.K_RETURN:
                    # Submit IP Address
                    new_ip = ip_input_text.strip()
                    if new_ip:
                        ntinst.setServer(new_ip)
                        print(f"Server IP set to {new_ip}")
                        # Restart NetworkTables client with new IP
                        try:
                            ntinst.stopClient()
                        except:
                            pass  # If client was not running
                        ntinst.startClient4("Pygame_Dashboard")
                        ip_input_text = ""
                        ip_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    ip_input_text = ip_input_text[:-1]
                else:
                    ip_input_text += event.unicode

        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if config_panel_active:
                # Check if click is inside IP input field
                if ip_input_rect.collidepoint(mouse_pos):
                    ip_input_active = True
                else:
                    ip_input_active = False

                # Check if Clear Terminal button is clicked
                if clear_terminal_button_rect.collidepoint(mouse_pos):
                    terminal_lines.clear()
                    ds_terminal_text_entry_publisher.set("")  # Use publisher to clear terminal text
                    print("Terminal cleared.")

                # Check if Submit IP button is clicked
                if submit_ip_button_rect.collidepoint(mouse_pos):
                    new_ip = ip_input_text.strip()
                    if new_ip:
                        ntinst.setServer(new_ip)
                        print(f"Server IP set to {new_ip}")
                        # Restart NetworkTables client with new IP
                        try:
                            ntinst.stopClient()
                        except:
                            pass  # If client was not running
                        ntinst.startClient4("Pygame_Dashboard")
                        ip_input_text = ""
                        ip_input_active = False

                # Check if Close Config button is clicked
                if close_config_button_rect.collidepoint(mouse_pos):
                    config_panel_active = False
                    ip_input_active = False

            else:
                # Check if Config button is clicked
                if config_button_rect.collidepoint(mouse_pos):
                    config_panel_active = True

    # Get canvas color from NetworkTables and clamp RGB values
    ds_r = clamp_rgb_value(ds_r_entry.get())
    ds_g = clamp_rgb_value(ds_g_entry.get())
    ds_b = clamp_rgb_value(ds_b_entry.get())
    canvas_color = (ds_r, ds_g, ds_b)
    text_color = invert_color(ds_r, ds_g, ds_b)

    # Get FMSControlData
    fms_control_data = fms_control_data_entry.get()

    # Determine the edge color and if FMS is attached
    edge_color, fms_attached = get_fms_edge_color(fms_control_data)

    # Get text data
    ds_largetext = ds_largetext_entry.get()
    ds_smalltext = ds_smalltext_entry.get()

    # Get flash data
    largetext_flash = ds_largetext_flash_entry.get()
    smalltext_flash = ds_smalltext_flash_entry.get()

    # Get terminal text data and clamp the RGB values
    terminal_text = ds_terminal_text_entry.get()
    terminal_text_r = clamp_rgb_value(ds_terminal_text_r_entry.get())
    terminal_text_g = clamp_rgb_value(ds_terminal_text_g_entry.get())
    terminal_text_b = clamp_rgb_value(ds_terminal_text_b_entry.get())
    terminal_force = ds_terminal_force_entry.get()

    # Handle terminal text updates
    if terminal_text != last_terminal_text or (terminal_force and not terminal_force_triggered):
        terminal_color = (terminal_text_r, terminal_text_g, terminal_text_b)  # Color only affects new lines
        terminal_lines.insert(0, (terminal_text, terminal_color))  # Insert new text and color at the top
        terminal_lines = terminal_lines[:terminal_max_lines]  # Keep only max lines
        last_terminal_text = terminal_text
        terminal_force_triggered = True if terminal_force else False

        # Reset ds_terminal_force_entry to False
        if terminal_force:
            ds_terminal_force_entry_publisher.set(False)
    elif not terminal_force:
        terminal_force_triggered = False  # Reset latch

    # Get chime states
    chime1_trigger = ds_chime_1_entry.get()
    chime2_trigger = ds_chime_2_entry.get()
    chime3_trigger = ds_chime_3_entry.get()

    # Handle chime playback with latching (Chime 1 and 2) and looping (Chime 3)
    
    # Chime 1 (Latched)
    if chime1_trigger and not chime1_played and chime1:
        chime1.play()
        chime1_played = True
        ds_chime_1_entry_publisher.set(False)  # Reset in NetworkTables
    elif not chime1_trigger:
        chime1_played = False  # Reset latch

    # Chime 2 (Latched)
    if chime2_trigger and not chime2_played and chime2:
        chime2.play()
        chime2_played = True
        ds_chime_2_entry_publisher.set(False)  # Reset in NetworkTables
    elif not chime2_trigger:
        chime2_played = False  # Reset latch

    # Chime 3 (Looping)
    if chime3_trigger and chime3 and not chime3_playing:
        chime3.play(loops=-1)  # Start looping Chime 3
        chime3_playing = True
        #ds_chime_3_entry_publisher.set(False)  # Reset in NetworkTables
    elif not chime3_trigger and chime3_playing:
        chime3.stop()  # Stop Chime 3 immediately
        chime3_playing = False

    # Fill the screen with the canvas color
    screen.fill(canvas_color)

    # Dynamically determine font size based on available canvas space
    available_width = screen_width - 2 * edge_width
    available_height = screen_height - 2 * edge_width

    # Get dynamic font for large and small text
    large_font = get_dynamic_font(ds_largetext, available_width, available_height // 2, 200)
    small_font = get_dynamic_font(ds_smalltext, available_width, available_height // 4, 100)

    # Render large text in the center of the screen
    draw_text(screen, ds_largetext, large_font, text_color, (screen_width // 2, screen_height // 2 - 50), largetext_flash, elapsed_time)
    
    # Render small text just below the large text
    draw_text(screen, ds_smalltext, small_font, text_color, (screen_width // 2, screen_height // 2 + 50), smalltext_flash, elapsed_time)

    # Draw the colored edge based on FMSControlData (top, bottom, left, right edges)
    pygame.draw.rect(screen, edge_color, (0, 0, screen_width, edge_width))  # Top edge
    pygame.draw.rect(screen, edge_color, (0, screen_height - edge_width, screen_width, edge_width))  # Bottom edge
    pygame.draw.rect(screen, edge_color, (0, 0, edge_width, screen_height))  # Left edge
    pygame.draw.rect(screen, edge_color, (screen_width - edge_width, 0, edge_width, screen_height))  # Right edge

    # Render the DS_toptext on the top edge
    ds_toptext = ds_toptext_entry.get()
    top_edge_font = get_dynamic_font(ds_toptext, screen_width - 2 * edge_width, edge_width, edge_width)
    top_text_color = invert_color(*edge_color)
    draw_text(screen, ds_toptext, top_edge_font, top_text_color, (screen_width // 2, edge_width // 2), False, elapsed_time)

    # Print terminal-like text in the bottom-left (inside the canvas, avoiding the edge)
    terminal_font = pygame.font.Font(None, 24)
    print_terminal(screen, terminal_font, terminal_lines, canvas_color, (10 + edge_width, screen_height - edge_width - terminal_max_lines * 20 - 10), terminal_max_lines)

    # If FMS is attached, display "FMS Connected" on the bottom edge
    if fms_attached:
        font = pygame.font.Font(None, 36)
        text_surface = font.render("FMS Connected", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - edge_width // 2))
        screen.blit(text_surface, text_rect)

    # Render Config Button if config panel is not active
    if not config_panel_active:
        render_button(screen, config_button_rect, "Config", button_font)

    # Render Config Panel if active
    if config_panel_active:
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(200)  # Transparency
        overlay.fill((50, 50, 50))  # Dark grey
        screen.blit(overlay, (0, 0))

        # Draw Config Panel Background
        panel_rect = pygame.Rect(screen_width//2 - 200, screen_height//2 - 150, 400, 300)
        pygame.draw.rect(screen, (100, 100, 100), panel_rect)
        pygame.draw.rect(screen, (0, 0, 0), panel_rect, 2)  # Border

        # Render IP Address Label
        ip_label = config_font.render("RoboRIO IP Address:", True, (255, 255, 255))
        screen.blit(ip_label, (screen_width//2 - 180, screen_height//2 - 130))

        # Render IP Input Field
        pygame.draw.rect(screen, (255, 255, 255), ip_input_rect, 2)
        ip_text_surface = config_font.render(ip_input_text, True, (0, 0, 0))
        screen.blit(ip_text_surface, (ip_input_rect.x + 5, ip_input_rect.y + 5))

        # Render Submit IP Button
        render_button(screen, submit_ip_button_rect, "Set IP", button_font)

        # Render Clear Terminal Button
        render_button(screen, clear_terminal_button_rect, "Clear Terminal", button_font)

        # Render Close Config Button (X)
        render_button(screen, close_config_button_rect, "X", button_font, color=(200, 0, 0), text_color=(255, 255, 255))

    # Update the display
    pygame.display.flip()

    # Flush NetworkTables to ensure data is sent/received
    ntinst.flush()

    # Limit the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
