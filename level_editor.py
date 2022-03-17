import pygame
import pyperclip


from engine import window, user_input, clock, statehandler, state
from src import editor_box


window.create_instance("Level Editor", 1280, 720)
window.create_clock(30)

BACK_COLOR = (0, 19, 35)
CONTAINER_COLOR = (0, 8, 14)

global_state = state.State()
statehandler.push_state(global_state)


# sidebar
back = editor_box.Editor_Box(None, 0.01, 0.01, 0.3, 0.99)
back.fill_color(CONTAINER_COLOR)
global_state.handler.add_entity(back)

back.create_child(0.01, 0.01, 0.99, 0.99)



# editor box
editor = editor_box.Editor_Box(None, 0.31, 0.01, 0.99, 0.99)
editor.fill_color(CONTAINER_COLOR)
global_state.handler.add_entity(editor)


changed = True
running = True
clock.start(30)
while running:

    if statehandler.CURRENT.handler.changed:
        window.FRAMEBUFFER.fill(BACK_COLOR)

    statehandler.CURRENT.handler.render_chunks(window.FRAMEBUFFER, (0,0))
    statehandler.CURRENT.handler.update_and_render_entities(window.FRAMEBUFFER, clock.delta_time, (0,0))

    if statehandler.CURRENT.handler.changed:
        window.INSTANCE.blit(window.FRAMEBUFFER, (0,0))
        statehandler.CURRENT.handler.changed = False
    pygame.display.update()


    # for loop through events
    for e in pygame.event.get():
        # handle different events
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            # keyboard press
            user_input.key_press(e)
        elif e.type == pygame.KEYUP:
            # keyboard release
            user_input.key_release(e)
        elif e.type == pygame.MOUSEMOTION:
            # mouse movement
            user_input.mouse_move_update(e)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            # mouse press
            user_input.mouse_button_press(e)
        elif e.type == pygame.MOUSEBUTTONUP:
            # mouse release
            user_input.mouse_button_release(e)
        elif e.type == pygame.WINDOWRESIZED:
            # window resized
            window.handle_resize(e)
            user_input.update_ratio(window.WIDTH, window.HEIGHT, window.ORIGINAL_WIDTH, window.ORIGINAL_HEIGHT)
    # update keyboard
    user_input.update()

    clock.update()
    window.GLOBAL_CLOCK.tick(clock.FPS)

pygame.quit()
