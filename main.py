from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Window size
WINDOW_W = 1000
WINDOW_H = 800

# Constants
SPHERE_RADIUS = 50
MOVE_ACCEL = 0.5
MAX_SPEED = 7.0
FRICTION = 0.95
GRAVITY = -0.2
JUMP_STRENGTH = 9
GROUND_Z = 0
STRIPE_WIDTH = 400       # Width of each ground stripe
RENDER_DISTANCE = 6000   # How far ahead/behind to draw the platform

# Global State Variables
# Position
sphere_x = 0
sphere_y = 0
sphere_z = 0

# Velocity
vel_x = 0.0
vel_y = 0.0
jump_velocity = 0

# Rotation
sphere_rot_x = 0
sphere_rot_y = 0

# Game State
platform_offset = 0
is_jumping = False

# Input Flags
move_forward = False
move_backward = False
move_left = False
move_right = False


def draw_platform():
    glPushMatrix()
    
    # We draw stripes instead of a solid block so movement is visible
    # Draw relative to the platform_offset which now follows the player
    start_y = platform_offset - RENDER_DISTANCE
    end_y = platform_offset + RENDER_DISTANCE
    
    # Loop to draw alternating colored stripes
    for y in range(int(start_y), int(end_y), STRIPE_WIDTH):
        if (y // STRIPE_WIDTH) % 2 == 0:
            glColor3f(0.3, 0.3, 0.3) # Dark Grey
        else:
            glColor3f(0.4, 0.4, 0.4) # Lighter Grey

        glBegin(GL_QUADS)
        glVertex3f(-200, y + STRIPE_WIDTH, 0)
        glVertex3f( 200, y + STRIPE_WIDTH, 0)
        glVertex3f( 200, y, 0)
        glVertex3f(-200, y, 0)
        glEnd()

    glPopMatrix()


def update_game():
    global platform_offset
    # Infinite runner logic: 
    # Instead of "jumping" the platform when we reach the end, we simply
    # keep the platform centered on the sphere.
    # We snap the offset to STRIPE_WIDTH to ensure the texture pattern 
    # doesn't slide/jitter visually as the platform moves.
    platform_offset = sphere_y - (sphere_y % STRIPE_WIDTH)


def draw_sphere():
    glPushMatrix()
    
    # Move sphere to its position
    glTranslatef(sphere_x, sphere_y, sphere_z)
    
    # Rotate sphere (Physics logic removed from here, only drawing happens here)
    glRotatef(sphere_rot_x, 1, 0, 0)  # Roll forward/back (around X axis)
    glRotatef(sphere_rot_y, 0, 1, 0)  # Roll left/right (around Y axis)
    
    glColor3f(0.5, 0.8, 0.2)
    glutWireSphere(SPHERE_RADIUS, 15, 15)

    glPopMatrix()


def update_jump():
    global sphere_z, jump_velocity, is_jumping
    
    if is_jumping:
        sphere_z += jump_velocity
        jump_velocity += GRAVITY

        # Landed on ground
        if sphere_z <= GROUND_Z:
            sphere_z = GROUND_Z
            jump_velocity = 0
            is_jumping = False


def apply_input_acceleration():
    global vel_x, vel_y

    # Modify velocity based on Input Flags
    if move_forward:
        vel_y -= MOVE_ACCEL # Forward is Negative Y
    if move_backward:
        vel_y += MOVE_ACCEL # Backward is Positive Y
    if move_left:
        vel_x += MOVE_ACCEL # Left is Positive X (Camera looks towards -Y)
    if move_right:
        vel_x -= MOVE_ACCEL # Right is Negative X (Camera looks towards -Y)


def apply_friction():
    global vel_x, vel_y

    vel_x *= FRICTION
    vel_y *= FRICTION

    # Stop micro-sliding
    if abs(vel_x) < 0.001: vel_x = 0
    if abs(vel_y) < 0.001: vel_y = 0

    # Clamp speed to MAX_SPEED
    vel_x = max(-MAX_SPEED, min(MAX_SPEED, vel_x))
    vel_y = max(-MAX_SPEED, min(MAX_SPEED, vel_y))


def update_position_from_velocity():
    global sphere_x, sphere_y
    sphere_x += vel_x
    sphere_y += vel_y


def update_rotation_from_velocity():
    global sphere_rot_x, sphere_rot_y

    # Calculate rotation angle based on distance moved
    # 57.3 is approx (180 / pi) to convert radians to degrees
    rot_x = (vel_y / SPHERE_RADIUS) * 57.3
    rot_y = (vel_x / SPHERE_RADIUS) * 57.3

    # Update global rotation angles
    # NOTE: Physics directions fixed here
    
    # Forward/Back: Moving Back (+Y) should rotate top of sphere Back (+Y -> +Z).
    # Rotation around +X moves Y->Z. So +vel_y means +rot_x.
    # Actually, visual check:
    # +X Rotation axis: Top moves towards -Y (Forward).
    # So if we move Back (+Y), we want -X Rotation.
    sphere_rot_x -= rot_x 

    # Left/Right: Moving Right (+X) should rotate top of sphere Right (+X).
    # Rotation around +Y moves Z->X. So +vel_x means +rot_y.
    sphere_rot_y += rot_y


def keyboardListener(key, x, y):
    global is_jumping, jump_velocity
    global move_forward, move_backward, move_left, move_right

    # JUMP
    if key == b' ' and not is_jumping:
        jump_velocity = JUMP_STRENGTH
        is_jumping = True
    
    # MOVEMENT FLAGS (Set to True when pressed)
    if key == b'w':
        move_forward = True
    elif key == b's':
        move_backward = True
    elif key == b'a':
        move_left = True
    elif key == b'd':
        move_right = True


def keyboardUpListener(key, x, y):
    global move_forward, move_backward, move_left, move_right

    # MOVEMENT FLAGS (Set to False when released)
    if key == b'w':
        move_forward = False
    elif key == b's':
        move_backward = False
    elif key == b'a':
        move_left = False
    elif key == b'd':
        move_right = False


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, WINDOW_W / WINDOW_H, 1, 15000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera looks at the sphere slightly from above/behind
    # We fix the camera X to 0 so it follows the sphere along Y but stays centered on track
    gluLookAt(
        0, sphere_y + 400, 200,   # Eye: Follows sphere Y
        0, sphere_y, 0,           # Center: Looks at sphere Y
        0, 0, 1                   # Up: Z is up
    )


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, WINDOW_W, WINDOW_H)

    setupCamera()

    draw_platform()
    draw_sphere()

    glutSwapBuffers()


def idle():
    apply_input_acceleration()
    apply_friction()
    update_position_from_velocity()
    update_rotation_from_velocity()
    update_jump()
    update_game()

    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"CG Project - Fixed")
    
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()