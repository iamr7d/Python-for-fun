import pygame
import cv2
import mediapipe as mp

# Initialize Pygame
pygame.init()

# Set up window dimensions and display
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw with Your Hand")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
drawing_color = (0, 255, 0)
button_color = (255, 0, 0)
button_hover_color = (200, 0, 0)

# Set up Pygame drawing surface
drawing_surface = pygame.Surface((width, height))
drawing_surface.fill(white)

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Setup webcam for hand tracking
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Variables to track drawing state
drawing = False
last_x, last_y = None, None
prev_x, prev_y = None, None

# Clear button dimensions and position
clear_button_rect = pygame.Rect(10, 10, 150, 50)

# Smooth hand tracking (Moving average method)
smooth_factor = 0.8
smoothed_x, smoothed_y = None, None

def smooth_hand_position(x, y):
    global smoothed_x, smoothed_y
    if smoothed_x is None or smoothed_y is None:
        smoothed_x, smoothed_y = x, y
    smoothed_x = smooth_factor * smoothed_x + (1 - smooth_factor) * x
    smoothed_y = smooth_factor * smoothed_y + (1 - smooth_factor) * y
    return int(smoothed_x), int(smoothed_y)

def draw_line(x, y):
    global last_x, last_y
    if last_x is not None and last_y is not None:
        pygame.draw.line(drawing_surface, drawing_color, (last_x, last_y), (x, y), 5)
    last_x, last_y = x, y

def draw_clear_button():
    # Draw clear button with hover effect
    if clear_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, button_hover_color, clear_button_rect)
    else:
        pygame.draw.rect(window, button_color, clear_button_rect)
    
    # Add text on the button
    font = pygame.font.Font(None, 36)
    text = font.render("Clear", True, white)
    window.blit(text, (clear_button_rect.x + 50, clear_button_rect.y + 10))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for mouse click on the clear button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if clear_button_rect.collidepoint(event.pos):
                drawing_surface.fill(white)  # Clear the drawing surface
                last_x, last_y = None, None  # Reset the drawing coordinates

    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)
    
    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the index finger tip coordinates
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)
            
            # Smooth the hand movement
            index_x, index_y = smooth_hand_position(index_x, index_y)
            
            # Draw landmarks and connections (optional)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Only draw if the hand is in a stable position (to avoid jitter)
            if prev_x is None or prev_y is None or abs(index_x - prev_x) > 5 or abs(index_y - prev_y) > 5:
                draw_line(index_x, index_y)
                prev_x, prev_y = index_x, index_y
    
    # Display the drawing surface
    window.fill(white)
    window.blit(drawing_surface, (0, 0))

    # Draw the clear button
    draw_clear_button()
    
    # Show webcam feed in a separate window (optional)
    cv2.imshow("Hand Tracking", frame)
    
    # Update the Pygame window
    pygame.display.update()

    # Close the webcam feed window if escape key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and quit
cap.release()
cv2.destroyAllWindows()
pygame.quit()
