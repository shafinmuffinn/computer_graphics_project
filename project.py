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
    glTranslatef(0, sphere_y, SPHERE_RADIUS)

    # rotate sphere to simulate rolling
    glRotatef(sphere_rot, 1, 0, 0)

    glColor3f(0.5, 0.8, 0.2)
    glutSolidSphere(SPHERE_RADIUS, 5, 5)

    glPopMatrix()
sphere_y = 0        # position along the platform
sphere_rot = 0     # rotation angle for rolling
SPHERE_RADIUS = 50
ROLL_SPEED = 40

platform_offset = 0
PLATFORM_LENGTH = 10000

def keyboardListener(key, x, y):
    global sphere_y, sphere_rot

    if key == b'w':
        sphere_y -= ROLL_SPEED
        #print(sphere_y)
        # rotation angle = distance / radius (simplified)
        sphere_rot += (ROLL_SPEED / SPHERE_RADIUS) * 57.3

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
    # Swap buffers (double buffering)
    glutSwapBuffers()
def idle():
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
    glutIdleFunc(idle)
    # Enter main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
