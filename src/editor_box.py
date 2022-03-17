from engine import entity, filehandler, window, statehandler


class Editor_Box(entity.Entity):
    def __init__(self, parent, left, top, right, bottom):
        """Constructor for an edtiro box"""
        super().__init__()
        if parent != None:
            entity.set_entity_properties(parent.area[0] * left + parent.pos[0], parent.area[1] * top + parent.pos[1], parent.area[0] * (right - left), parent.area[1] * (bottom - top), None, self)
        else:
            entity.set_entity_properties(window.WIDTH * left, window.HEIGHT * top, window.WIDTH * (right - left), window.HEIGHT * (bottom - top), None, self)
        self.background = filehandler.create_surface(self.area[0], self.area[1], flags=filehandler.SRCALPHA).convert()

        # editor box default
        self.dirty = True
        if parent:
            self.parent_id = parent.id
        else:
            self.parent_id = 0
        self.children = []
    
    def fill_color(self, color):
        """Fill the color of our surface"""
        self.background.fill(color)
    
    def render(self, window, offset):
        """Render entity"""
        if self.dirty:
            print("rednering", self.id)
            self.image = self.background
            self.dirty = False
            window.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))
            statehandler.CURRENT.handler.changed = True

    def update(self, dt):
        """Default update """
        pass

    def create_child(self, left, top, right, bottom):
        """Add a child to this editor"""
        child = Editor_Box(self, left, top, right, bottom)
        statehandler.CURRENT.handler.add_entity(child)
        self.children.append(child.id)


class SideBarSelection(Editor_Box):
    def __init__(self, parent, left, top, right, bottom):
        """Constructor for """
        super().__init__(parent, left, top, right, bottom)
        # selecion
        self.items = []
        self.selected = []


