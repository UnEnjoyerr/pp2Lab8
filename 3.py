import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    points = []
    eraser_points = []
    mode = 'blue'
    drawing_shape = 'line'
    eraser_mode = False
    drawing_shape_active = False  # For circle and square
    shape_start_pos = None
    shapes = []  # Store all drawn shapes
    
    while True:
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
                # Color selection
                if event.key == pygame.K_r:
                    mode = 'red'
                    eraser_mode = False
                elif event.key == pygame.K_g:
                    mode = 'green'
                    eraser_mode = False
                elif event.key == pygame.K_b:
                    mode = 'blue'
                    eraser_mode = False
                elif event.key == pygame.K_e:  # Toggle eraser mode
                    eraser_mode = not eraser_mode
                elif event.key == pygame.K_c:  # Draw circle
                    drawing_shape = 'circle'
                elif event.key == pygame.K_x:  # Draw square
                    drawing_shape = 'square'
                elif event.key == pygame.K_l:  # Draw line
                    drawing_shape = 'line'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if eraser_mode:
                        eraser_points.append(event.pos)
                    else:
                        if drawing_shape == 'line':
                            points.append(event.pos)
                        elif drawing_shape in ['circle', 'square']:
                            drawing_shape_active = True
                            shape_start_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing_shape_active:
                    if drawing_shape == 'circle' and not eraser_mode:
                        end_pos = event.pos
                        radius = int(math.hypot(end_pos[0] - shape_start_pos[0], 
                                             end_pos[1] - shape_start_pos[1]))
                        shapes.append(('circle', shape_start_pos, radius, get_color(mode)))
                    elif drawing_shape == 'square' and not eraser_mode:
                        end_pos = event.pos
                        width = end_pos[0] - shape_start_pos[0]
                        height = end_pos[1] - shape_start_pos[1]
                        shapes.append(('square', shape_start_pos, width, height, get_color(mode)))
                    drawing_shape_active = False
            
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button pressed
                    if eraser_mode:
                        eraser_points.append(event.pos)
                        eraser_points = eraser_points[-256:]
                    else:
                        if drawing_shape == 'line':
                            points.append(event.pos)
                            points = points[-256:]

        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw all persistent shapes
        for shape in shapes:
            if shape[0] == 'circle':
                pygame.draw.circle(screen, shape[3], shape[1], shape[2])
            elif shape[0] == 'square':
                rect = pygame.Rect(shape[1][0], shape[1][1], shape[2], shape[3])
                pygame.draw.rect(screen, shape[4], rect)
        
        # Draw current line (normal drawing)
        if drawing_shape == 'line':
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
                i += 1
        
        # Draw eraser lines (black)
        i = 0
        while i < len(eraser_points) - 1:
            drawLineBetween(screen, i, eraser_points[i], eraser_points[i + 1], radius, 'black')
            i += 1
        
        # Draw preview of current shape being drawn
        if drawing_shape_active and shape_start_pos:
            current_pos = pygame.mouse.get_pos()
            if drawing_shape == 'circle' and not eraser_mode:
                radius_preview = int(math.hypot(current_pos[0] - shape_start_pos[0], 
                                             current_pos[1] - shape_start_pos[1]))
                pygame.draw.circle(screen, get_color(mode), shape_start_pos, radius_preview)
            elif drawing_shape == 'square' and not eraser_mode:
                width = current_pos[0] - shape_start_pos[0]
                height = current_pos[1] - shape_start_pos[1]
                rect = pygame.Rect(shape_start_pos[0], shape_start_pos[1], width, height)
                pygame.draw.rect(screen, get_color(mode), rect)

        pygame.display.flip()
        clock.tick(60)

def get_color(color_mode):
    if color_mode == 'blue':
        return (0, 0, 255)
    elif color_mode == 'red':
        return (255, 0, 0)
    elif color_mode == 'green':
        return (0, 255, 0)
    elif color_mode == 'black':
        return (0, 0, 0)
    return (255, 255, 255)

def drawLineBetween(screen, index, start, end, width, color_mode):
    color = get_color(color_mode)
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()