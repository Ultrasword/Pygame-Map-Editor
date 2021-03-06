import pygame
import pyperclip


from engine import window, user_input, clock, statehandler, state, filehandler, eventhandler
from src import editor_box, art_tool

FPS = 30


window.create_instance("Level Editor", 1280, 720)
window.create_clock(FPS)

BACK_COLOR = (0, 19, 35)
CONTAINER_COLOR = (0, 8, 14)

global_state = state.State()
statehandler.push_state(global_state)


# sidebar
hovering_items = []


back = editor_box.Editor_Box(None, 0.005, 0.01, 0.3, 0.99)
back.fill_color(CONTAINER_COLOR)
global_state.handler.add_entity(back)

container = back.create_child(editor_box.SideBarSelection, 0.01, 0.01, 0.99, 0.99)
container.column = 3
container.padding = 2

# hovering_items.append(container)

container.load_spritesheet("assets/spritesheets/grass.json")

# editor box
editor = editor_box.Editor_Box(None, 0.305, 0.01, 0.995, 0.99)
editor.fill_color(CONTAINER_COLOR)
global_state.handler.add_entity(editor)

# add actual editing area
editor_area = editor.create_child(editor_box.LevelEditor, 0.01, 0.01, 0.99, 0.99)
editor_area.fill_color((255,255,255))
editor_area.z_index = 2

# tile map
tilemap = editor_area.create_child(editor_box.TileMap, 0.05, 0.05, 0.95, 0.95)
tilemap.fill_color((255, 255, 255))
tilemap.z_index = 3

editor_area.set_tile_map(tilemap)

editor_area.save_tile_map_to_file("test.json", container)

# set art tool


# ---------------- test

test_event = eventhandler.Event({"1": "TESTING!!!"})
eventhandler.register_event(test_event.eid)

def func(data):
    print("AWDAWd")
eventhandler.register_func_to_event(test_event.eid, func)



changed = True
running = True
clock.start(FPS)
while running:
    # update the background if changed
    if statehandler.CURRENT.handler.changed:
        window.FRAMEBUFFER.fill(BACK_COLOR)

    # statehandler.CURRENT.handler.render_chunks(window.FRAMEBUFFER, (0,0))
    statehandler.CURRENT.handler.update_and_render_entities(window.FRAMEBUFFER, clock.delta_time, (0,0))
    # print(item.sprite.get_size())
    # window.FRAMEBUFFER.blit(test, (0,0))

    if statehandler.CURRENT.handler.changed:
        window.INSTANCE.blit(window.FRAMEBUFFER, (0,0))
        statehandler.CURRENT.handler.changed = False
    pygame.display.update()

    # user input update
    user_input.update()
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
    eventhandler.update_events()

    clock.update()
    window.GLOBAL_CLOCK.tick(clock.FPS)

pygame.quit()
