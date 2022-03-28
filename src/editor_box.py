import pygame
import json
from engine import entity, filehandler, window, statehandler, user_input, draw, chunk, maths, eventhandler
from src import art_tool


class Editor_Box(entity.Entity):
    def __init__(self, parent, left, top, right, bottom, item_columns=1, back=True):
        """Constructor for an edtiro box"""
        super().__init__()
        if parent != None:
            xpos = parent.area[0] * left + parent.pos[0]
            ypos = parent.area[1] * top + parent.pos[1]
            width = parent.area[0] * (right - left)
            height = parent.area[1] * (bottom - top)
            self.rel_pos = [parent.area[0] * left, parent.area[1] * top, self.area[0], self.area[1]]
            entity.set_entity_properties(xpos, ypos, width, height, None, self)
        else:
            entity.set_entity_properties(window.WIDTH * left, window.HEIGHT * top, window.WIDTH * (right - left), window.HEIGHT * (bottom - top), None, self)
            self.rel_pos = [self.pos[0], self.pos[1], self.area[0], self.area[1]]
        if back:
            self.background = filehandler.create_surface(self.area[0], self.area[1]).convert()
        else:
            self.background = None

        self.z = 0
        
        # in selection items stuff
        self.item_columns = item_columns
        self.item_width = self.area[0] // 2

        self.column = item_columns
        self.grid_pos = 0

        # editor box default
        self.dirty = True
        if parent:
            self.parent_id = parent.id
        else:
            self.parent_id = 0
        self.children = []
        self.padding = 0

        # stats
        self.hovering = False
        self.back_fill_color = (0, 0, 0)
    
    def fill_color(self, color):
        """Fill the color of our surface"""
        self.back_fill_color = color
        self.background.fill(color)
    
    def render(self, window, offset):
        """Render entity"""
        if self.dirty:
            # print("rednering", self.id)
            self.image = self.background
            self.dirty = False
            window.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))
            statehandler.CURRENT.handler.changed = True

    def update(self, dt):
        """Default update """
        pass

    def create_child(self, item_type, left, top, right, bottom):
        """Add a child to this editor"""
        child = item_type(self, left, top, right, bottom)
        statehandler.CURRENT.handler.add_entity(child)
        self.children.append(child.id)
        return child
    
    def scale_image_percent(self, img, size: tuple):
        """Scale using percent"""
        n = int(size * self.area[0])
        return filehandler.scale(img, (n, n))

    def scale_image_int(self, img, size):
        return filehandler.scale(img, size)
    
    def scale_image_to_item_size(self, img):
        """Image scale to item width"""
        return filehandler.scale(img, (self.item_width, self.item_width))

    def apply_all_transformations(self, child):
        """Apply all padding, scaling, etc"""
        # transform the image
        self.column
        n = child.grid_pos % self.column
        child.pos[0] = self.pos[0] + self.item_width * n
        n = child.grid_pos // self.column
        child.pos[1] = self.pos[1] + self.item_width * n
        child.area[0] = self.item_width
        child.area[1] = self.item_width
        # scale image
        child.background = filehandler.scale(filehandler.get_image(child.sprite_path), 
                    (self.item_width, self.item_width))

    @property
    def hover(self):
        """Check if mouse is hovering"""
        self.hovering = False
        mpos = user_input.get_mouse_pos()
        if self.pos[0] > mpos[0]:
            return False
        if self.pos[0] + self.area[0] < mpos[0]:
            return False
        if self.pos[1] > mpos[1]:
            return False
        if self.pos[1] + self.area[1] < mpos[1]:
            return False
        self.hovering = True
        return True

    @property
    def z_index(self):
        """Get z index"""
        return self.z
    
    @z_index.setter
    def z_index(self, other):
        """Set the z index"""
        self.z = other

    @property
    def column(self):
        """Returns the item width when items are contained within this container"""
        return self.item_columns

    @column.setter
    def column(self, cols):
        """Sets the item width"""
        self.item_columns = cols
        self.item_width = int(self.area[0] / self.item_columns)

    @property
    def grid_position(self):
        """Return the grid pos"""
        return self.grid_pos
    
    @grid_position.setter
    def grid_position(self, pos):
        """Set the grid pos"""
        self.grid_pos = pos

    @property
    def clicked(self):
        return self.hover and user_input.mouse[1]


class SideBarSelection(Editor_Box):
    def __init__(self, parent, left, top, right, bottom):
        """Constructor for side bar item selection"""
        super().__init__(parent, left, top, right, bottom)
        # selecion
        self.selected = []
        self.used_pos = set()
        # scrolling
        self.scrolly = 0
        self.lowest_bottom = 0
        # spritesheets
        self.sprite_sheets = {}
    
    @property
    def item_padding(self):
        """Return item padding"""
        return self.padding
    
    @item_padding.setter
    def item_padding(self, other):
        """Set item padding"""
        self.padding = other
        # resize everything
        for child in self.children:
            self.apply_all_transformations(child)

    def find_lowest_pos(self):
        """Find the lowest pos for an item part"""
        if not self.used_pos:
            return 0
        low = 0
        if low == min(self.used_pos):
            # then find the next lowest that is greater than 0
            while low in self.used_pos:
                low += 1
            self.used_pos.add(low)
            return low
        else:
            self.used_pos.add(0)
            return 0
    
    def apply_all_transformations(self, child):
        """Apply all padding, scaling, etc"""
        # transform the image
        self.column
        # calculate row and col
        x = child.grid_pos % self.column
        y = child.grid_pos // self.column
        # set values for position and apply padding
        child.pos[0] = int(self.pos[0] + self.item_width * x + self.padding * (x+1))
        child.pos[1] = int(self.pos[1] + self.item_width * y + self.padding * (y+1))
        child.area[0] = int(self.item_width - self.padding * 2)
        child.area[1] = child.area[0]
        # set rel pos
        child.rel_pos = [child.pos[0] - self.pos[0], child.pos[1] - self.pos[1], child.area[0], child.area[1]]
        # scale image
        child.background = filehandler.scale(filehandler.get_image(child.sprite_path), 
                    child.area)
        # add to the set
        self.used_pos.add(child.grid_pos)

    def load_spritesheet(self, file_path):
        """Load a spritesheet from json file"""
        with open(file_path, 'r') as file:
            data = json.load(file)
            file.close()
        # load the data
        image = data["file"]
        width = data["tile_width"]
        height = data["tile_height"]
        tile_pos = data["tiles"]
        sprite_sheet = filehandler.get_image(image)
        self.sprite_sheets[file_path] = sprite_sheet
        # add each child to the children
        for pos in tile_pos:
            if pos == None:
                # add an empty block
                grid_pos = self.find_lowest_pos()
                self.used_pos.add(grid_pos)
                continue
            # get x and y pos
            x, y = map(int, pos.split("."))
            # grab sprite from the image
            px = x * width
            py = y * height
            # grab image and paste onto new surface
            item = self.create_child(SideBarItem, 0.05, 0.05, 0.3, 0.3)
            item.sprite_path = image
            item.grid_pos = self.find_lowest_pos()
            self.apply_all_transformations(item)
            # set image
            item.background = filehandler.scale(filehandler.cut(px, py, width, height, sprite_sheet), (self.item_width, self.item_width))
            self.lowest_bottom = max(self.lowest_bottom, item.pos[1] + item.area[1])

    def update(self, dt):
        """update the objects inside and the side bar"""
        # get scrolling
        self.dirty = True
        self.scrolly -= user_input.y_scroll * 10
        # set a clamp onto the scrolling
        self.scrolly = maths.clamp(self.scrolly, 0, self.lowest_bottom)
        # render the items inside first
        self.background.fill(self.back_fill_color)
        for eid in self.children:
            child = statehandler.CURRENT.handler.entities[eid]
            child.update_mouse(self.scrolly)
            # render each child onto background with offset
            self.background.blit(child.background, (child.rel_pos[0], child.rel_pos[1] - self.scrolly))
            self.image = self.background


class SideBarItem(Editor_Box):
    def __init__(self, parent, left, top, right, bottom):
        """Constructor for a side bar item"""
        super().__init__(parent, left, top, right, bottom)
        self.image_path = None
        # image etc
        self.parent = parent

    @property
    def sprite(self):
        """Get the sprite path"""
        return self.background

    @sprite.setter
    def sprite(self, img):
        """Set image"""
        self.background = img

    @property
    def sprite_path(self):
        """Get the sprite path"""
        return self.image_path
    
    @sprite_path.setter
    def sprite_path(self, path):
        """Set the sprite path"""
        self.image_path = path

    def update_mouse(self, y_scroll):
        """update but better"""
        mpos = user_input.get_mouse_pos()
        self.hovering = False
        if self.pos[0] > mpos[0]:
            return
        if self.pos[0] + self.area[0] < mpos[0]:
            return
        if self.pos[1] > mpos[1] + y_scroll:
            return
        if self.pos[1] + self.area[1] < mpos[1] + y_scroll:
            return
        
        # is hovering - check if clicking
        if not user_input.mouse[1]:
            return
        
        # handle clicking stuff
        if art_tool.ACTIVE_EDITOR:
            art_tool.ACTIVE_EDITOR.user_brush.icon_image = self.sprite
        art_tool.ART_ITEM_SELECTION = self

    def update(self, dt):
        """Update function overload"""
        # check if mouse hovers and if click
        return
        if self.clicked:
            if art_tool.ACTIVE_EDITOR:
                art_tool.ACTIVE_EDITOR.user_brush.icon_image = self.sprite
            # print("CLICKED!!!")
            art_tool.ART_ITEM_SELECTION = self
    
    def render(self, window, offset):
        """Empty func"""
        pass


class LevelEditor(Editor_Box):
    def __init__(self, parent, left, top, right, bottom):
        """Constructor for the level editor box"""
        super().__init__(parent, left, top, right, bottom)
        # level editor stuffs
        self.brush = None
        self.block_width = int(self.area[0] // 16)
        # acts as a camera
        self.c_offset = [0, 0]
        self.grid_color = (0,0,0)

        # set to default brush
        self.brush = art_tool.Brush(None, 1, self.block_width)

        # movespeed
        self.move_speed = 240

        # sprites that can be used
        self.spritesheets = {}

        # custom click event for drawing onto map
        self.tilemap = None
        self.event = eventhandler.Event({'x':0, 'y':0, 'img':0})

        # register the event function
        eventhandler.register_event(self.event.eid)
        self.func_eid = eventhandler.register_func_to_event(self.event.eid, lambda data: print(data))
    
    @property
    def camera_move_speed(self):
        """Returns camera move speed"""
        return self.move_speed
    
    @camera_move_speed.setter
    def camera_move_speed(self, new):
        """Set new camera move speed"""
        self.move_speed = new

    @property
    def grid_outline_color(self):
        """Return the grid color"""
        return self.grid_color
    
    @grid_outline_color.setter
    def grid_outline_color(self, col):
        """Set grid outline color"""
        self.grid_color = col

    @property
    def user_brush(self):
        """Return the current brush"""
        return self.brush

    @user_brush.setter
    def user_brush(self, new):
        """Set the current brush"""
        self.brush = new
    
    def set_brush_icon(self, icon):
        """Set the brush icon"""
        self.brush.icon_path = icon
        self.brush.icon_image = filehandler.scale(filehandler.get_image(icon), (self.block_width, self.block_width))

    def set_tile_map(self, tile_map):
        """set the tile map"""
        self.tilemap = tile_map
        # remove function from event handler
        eventhandler.remove_func_id(self.func_eid)
        # make new func
        self.func_eid = eventhandler.register_func_to_event(self.event.eid, self.tilemap.set_tile_at_event)

    def update(self, dt):
        """Updates editor area"""
        # get mouse and make it relative
        # offset stuff
        if user_input.is_key_pressed(pygame.K_LEFT):
            self.c_offset[0] -= self.move_speed * dt
            self.dirty = True
        if user_input.is_key_pressed(pygame.K_RIGHT):
            self.c_offset[0] += self.move_speed * dt
            self.dirty = True
        if user_input.is_key_pressed(pygame.K_UP):
            self.c_offset[1] -= self.move_speed * dt
            self.dirty = True
        if user_input.is_key_pressed(pygame.K_DOWN):
            self.c_offset[1] += self.move_speed * dt
            self.dirty = True

        # if mouse hovering or if something was changed in the editor
        if self.hover or self.dirty:

            # therefore the active editor is self
            art_tool.ACTIVE_EDITOR = self
            self.dirty = True

            # mouse position
            mpos = user_input.get_mouse_pos()
            rpos = [mpos[0] - self.pos[0] + self.c_offset[0], mpos[1] - self.pos[1] + self.c_offset[1]]

            # some click events
            if user_input.mouse[1]:
                # set event data
                self.event.data['x'] = int(rpos[0]) // self.block_width
                self.event.data['y'] = int(rpos[1]) // self.block_width
                self.event.data['img'] = self.brush.icon_image
                eventhandler.add_event(self.event)
            # print(user_input.mouse_pressed_this)

            # fill back and then paint with brush
            self.background.fill((255,255,255))
            # draw tilemap onto image
            if self.tilemap:
                self.tilemap.render_grid(self.background, self.c_offset)
                # self.background.blit(self.tilemap.image, (self.tilemap.rel_pos[0] - self.c_offset[0],
                #                 self.tilemap.rel_pos[1] - self.c_offset[1]))
            art_tool.paint_with_brush(self.background, rpos, self.brush, self)
            art_tool.brush_hover_outline(self.background, rpos, self.brush, self)

            # draw to image
            self.image = self.background

    def render(self, window, offset):
        """Render the art system with grids"""
        if self.dirty:
            # print("rednering", self.id)
            self.image = self.background
            self.dirty = False
            
            # draw grids
            left = 0
            top = 0
            right = int(self.area[0] // self.block_width)
            bottom = int(self.area[1] // self.block_width)
            # draw vertical lines
            xoff, yoff = self.c_offset[0] % self.block_width, self.c_offset[1] % self.block_width
            extend = self.block_width
            for x in range(left, right+1):
                draw.DEBUG_DRAW_LINE(self.background, self.grid_color,
                    (x * self.block_width + offset[0] - xoff, offset[1]), 
                    (x * self.block_width + offset[0] - xoff, self.area[1] + offset[1] + extend))
            # draw horizontal lines
            for y in range(top, bottom+2):
                draw.DEBUG_DRAW_LINE(self.background, self.grid_color,
                    (offset[0], y * self.block_width + offset[1] - yoff),
                    (self.area[0] + offset[0], y * self.block_width + offset[1] - yoff))

            # draw onto window
            window.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))
            statehandler.CURRENT.handler.changed = True

    def save_tile_map_to_file(self, file_path, sidebar_object):
        """Save the tilemap to a file"""
        # make a save buffer
        buffer = {}
        # store data into buffer
        buffer["level_name"] = None
        # get blocks and texture data
        buffer["spritesheets"] = {}
        # just save another copy of all the level sprites
        for cid in sidebar_object.children:
            child = statehandler.CURRENT.handler.entities[cid]
            # check if they are sidebar item object type
            if type(child) == SideBarItem:
                print("yes")

        return

        # open file path object
        with open(file_path, "w") as file:
            # write data into file
            

            # close file
            file.close()


class TileMap(Editor_Box):
    def __init__(self, parent, l, t, r, b):
        """Constructor for a tilemap - fills 100% of parent object"""
        super().__init__(parent, 0, 0, 1, 1)
        self.parent = parent

        # chunks dict
        self.chunks = {}

        # dirty?
        self.dirty = True
    
    def set_tile_at_event(self, data: dict):
        """set tile using given dict event"""
        # print("TileMap: ", data)
        self.dirty = True
        self.set_tile_at(data['x'], data['y'], data['img'])

    def set_tile_at(self, x, y, img: str):
        """Sets a tile at a given position"""
        # find the chunk it is located in
        cx = x // chunk.CHUNK_WIDTH
        cy = y // chunk.CHUNK_HEIGHT
        # create chunk if not exist
        h = maths.two_hash(cx, cy)
        crx = int(x - cx * chunk.CHUNK_WIDTH)
        cry = int(y - cy * chunk.CHUNK_HEIGHT)
        # TODO - create new chunk object
        if self.chunks.get(h):
            # set pos
            self.chunks.get(h).set_tile_at([crx, cry, img, 0])
        else:
            # make a chunk
            new_chunk = chunk.Chunk(cx, cy)
            new_chunk.set_tile_at([crx, cry, img, 0])
            self.chunks[h] = new_chunk

    def render_grid(self, window, offset):
        """Render grid whenever"""
        # check if dirty
        bw = self.parent.block_width
        cw = bw * chunk.CHUNK_WIDTH
        ch = bw * chunk.CHUNK_HEIGHT
        for h, cc in self.chunks.items():
            # render the blocks into the grid
            # check if chunk is on screen first
            for tile in cc.grid:
                # if image
                if tile[chunk.TILE_I]:
                    # render
                    x = tile[chunk.TILE_X] * bw + cw * cc.pos[0]
                    y = tile[chunk.TILE_Y] * bw + ch * cc.pos[1]
                    tile[chunk.TILE_I].set_alpha(255)
                    window.blit(tile[chunk.TILE_I], (x - offset[0], y - offset[1]))
                    tile[chunk.TILE_I].set_alpha(128)
