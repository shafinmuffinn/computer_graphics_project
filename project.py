from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window size (use constants, very important)
WINDOW_W = 1000
WINDOW_H = 800
def draw_platform():
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)

    glBegin(GL_QUADS)
    glVertex3f(-200,  platform_offset + 5000, 0)
    glVertex3f( 200,  platform_offset + 5000, 0)
    glVertex3f( 200,  platform_offset - 5000, 0)
    glVertex3f(-200,  platform_offset - 5000, 0)
    glEnd()

    glPopMatrix()
def update_game():
    global platform_offset

    # if sphere reaches near the end
    if sphere_y < platform_offset - 3000:
        platform_offset -= PLATFORM_LENGTH


def draw_sphere():
    glPushMatrix()
    # move sphere forward along platform
    glTranslatef(0, sphere_y, sphere_z)
    # rotate sphere to simulate rolling
    glRotatef(sphere_rot, 1, 0, 0)
    glColor3f(0.5, 0.8, 0.2)
    glutWireSphere(50, 10, 10)

    glPopMatrix()
sphere_y = 0        # position along the platform
sphere_rot = 0     # rotation angle for rolling
SPHERE_RADIUS = 50
ROLL_SPEED = 5

platform_offset = 0
PLATFORM_LENGTH = 10000

#after adding jump
sphere_z = 0          # current height of sphere
jump_velocity = 0    # how fast it goes up/down
is_jumping = False   # whether jump is active

GRAVITY = -0.2
JUMP_STRENGTH = 9
GROUND_Z = 0

# after jump/holding down 'w' issue
move_forward = False
jump_requested = False


def update_jump():
    global sphere_z, jump_velocity, is_jumping, sphere_y, velocity_z, jump_requested
    

    if is_jumping:
        sphere_z += jump_velocity
        jump_velocity += GRAVITY

        # landed back on platform
        if sphere_z <= GROUND_Z:
            sphere_z = GROUND_Z
            jump_velocity = 0
            is_jumping = False
def keyboardUpListener(key, x, y):
    global move_forward

    if key == b'w':
        move_forward = False
        
def keyboardListener(key, x, y):
    global sphere_y, sphere_rot, jump_velocity, is_jumping, move_forward, jump_requested
    if key == b' ' and not is_jumping:
        jump_requested = True ##might need to change
        jump_velocity = JUMP_STRENGTH
        is_jumping = True

    if key == b'w':
        move_forward = True
    
        #print(sphere_y)
        # rotation angle = distance / radius (simplified)
        sphere_rot += (ROLL_SPEED / SPHERE_RADIUS) * 57.3
        sphere_y -= ROLL_SPEED

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Perspective camera (standard lab-safe)
    gluPerspective(60, WINDOW_W / WINDOW_H, 1, 5000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera position
    gluLookAt(
        0, 400, 200,   # eye (camera position)
        0, 0, 0,       # center (look-at point)
        0, 0, 1        # up vector (z-up)
    )

def showScreen():
    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Viewport (maps OpenGL coordinates to window)
    glViewport(0, 0, WINDOW_W, WINDOW_H)

    # Setup camera
    setupCamera()

    # -------- DRAW HERE (later) -------- #
    draw_sphere()
    draw_platform()
    update_jump()

    # Swap buffers (double buffering)
    glutSwapBuffers()
def idle():
    global sphere_y, sphere_rot

    if move_forward:
        sphere_y -= ROLL_SPEED   # move forward continuously
        sphere_rot += (ROLL_SPEED / SPHERE_RADIUS) * 57.3
    update_jump()

    glutPostRedisplay()
    glutPostRedisplay()
    update_game()
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"CG Project - Starter")
    # Enable depth testing (VERY IMPORTANT for 3D)
    glEnable(GL_DEPTH_TEST)

    # Background color
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Register display callback
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)

    glutIdleFunc(idle)
    # Enter main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
