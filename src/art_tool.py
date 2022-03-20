from engine import filehandler


ACTIVE_EDITOR = None


def paint_with_brush(window, rel_pos_to_container, brush, editor_box):
    """Paint with brush"""
    # get the position
    width = editor_box.block_width
    relx = rel_pos_to_container[0] // editor_box.block_width
    rely = rel_pos_to_container[1] // editor_box.block_width
    # draw the brush onto the window
    brush.draw(window, (relx, rely), editor_box.block_width, editor_box.c_offset)


def brush_hover_outline(window, rel_pos_to_container, brush, editor_box):
    """Hover effect for the brush"""
    # get the position
    width = editor_box.block_width
    relx = (rel_pos_to_container[0] - editor_box.c_offset[0]) // editor_box.block_width
    rely = (rel_pos_to_container[1] - editor_box.c_offset[1]) // editor_box.block_width
    # draw the outline to the window
    brush.draw(window, (relx, rely), editor_box.block_width, editor_box.c_offset)


class Brush:
    def __init__(self, icon, size, width):
        """Brush constructor"""
        self.icon = icon
        self.size = size
        self.block_width = width

    @property
    def icon_image(self):
        """Get icon"""
        return self.icon
    
    @icon_image.setter
    def icon_image(self, new):
        """Set icon image"""
        self.icon = filehandler.scale(new.copy(), (self.block_width, self.block_width))
        self.icon.set_alpha(128)

    @property
    def brush_size(self):
        """Get the brush size"""
        return self.size
    
    @brush_size.setter
    def brush_size(self, size):
        """Set brush size"""
        self.size = size

    def draw(self, window, rel_pos, block_width, c_offset):
        """Draw function"""
        # the standard brush
        # usually drawn using smaller brush sizes
        # print(rel_pos[0] * block_width, rel_pos[1] * block_width)
        window.blit(self.icon, (rel_pos[0] * block_width + c_offset[0], rel_pos[1] * block_width + c_offset[1]))
        
        # left = rel_pos[0] * block_width
        # top = rel_pos[1] * block_width
        # for x in range(self.size):
        #     # draw the selected item onto the window
        #     for i in range(2 * x + 1):
        #         window.blit(self.icon, (0, 0)) # change this
        # for x in range(self.size - 2, -1, -1):
        #     # draw selected items
        #     for i in range(2 * x + 1):
        #         window.blit(self.icon, (self.size-x))

