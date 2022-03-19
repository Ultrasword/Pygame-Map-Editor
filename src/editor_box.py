from engine import entity, filehandler, window, statehandler, user_input
from src import art_tool


class Editor_Box(entity.Entity):
    def __init__(self, parent, left, top, right, bottom, item_columns=1, back=True):
        """Constructor for an edtiro box"""
        super().__init__()
        if parent != None:
            entity.set_entity_properties(parent.area[0] * left + parent.pos[0], parent.area[1] * top + parent.pos[1], 
                            parent.area[0] * (right - left) + parent.pos[0], parent.area[1] * (bottom - top) + parent.pos[1], None, self)
        else:
            entity.set_entity_properties(window.WIDTH * left, window.HEIGHT * top, window.WIDTH * (right - left), window.HEIGHT * (bottom - top), None, self)
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

        # stats
        self.hovering = False
    
    def fill_color(self, color):
        """Fill the color of our surface"""
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


class SideBarSelection(Editor_Box):
    def __init__(self, parent, left, top, right, bottom):
        """Constructor for side bar item selection"""
        super().__init__(parent, left, top, right, bottom)
        # selecion
        self.items = []
        self.selected = []


class SideBarItem(Editor_Box):
    def __init__(self, parent, left, top, right, bottom):
        """Constructor for a side bar item"""
        super().__init__(parent, left, top, right, bottom)
        self.image_path = None
        # image etc
        # print(self.pos, self.area)
        self.clicked = False

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

    def update(self, dt):
        # check if mouse hovers and if click
        if self.hover and user_input.mouse[1]:
            print("CLICKED!!!")
            art_tool.ART_ITEM_SELECTION = self


class LevelEditor(Editor_Box):
    def __init__(self, parent, left, top, right, bottom):
        """Constructor for the level editor box"""
        super().__init__(parent, left, top, right, bottom)
        # level editor stuffs
        self.brush = None
        self.block_width = int(self.area[0] // 16)
        # acts as a camera
        self.offset = [0, 0]

        # set to default brush
        self.brush = art_tool.Brush(None, 1)

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
        self.brush.icon = filehandler.scale(icon, (self.block_width, self.block_width))

    def update(self, dt):
        """Updates editor area"""
        # get mouse and make it relative
        if self.hover:
            self.dirty = True
            mpos = user_input.get_mouse_pos()
            rpos = [mpos[0] - self.pos[0], mpos[1] - self.pos[1]]
            # 
            self.background.fill((255,255,255))
            art_tool.paint_with_brush(self.background, rpos, self.brush, self)

            # draw to image
            self.image = self.background
