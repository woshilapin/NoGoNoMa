from bearlibterminal import terminal

from world import World
from ui_system.ui_enums import Layers
from ui_system.render_functions import get_item_display_name
from ui_system.render_camera import get_screen_bounds
from components.position_component import PositionComponent
from components.name_component import NameComponent
from components.hidden_component import HiddenComponent
from components.attributes_component import AttributesComponent
from components.pools_component import Pools
from ui_system.interface import Interface


class Tooltip:
    def __init__(self):
        self.lines = list()

    def add(self, string):
        self.lines.append(string)

    @property
    def width(self):
        best = 0
        for line in self.lines:
            if len(line) > best:
                best = len(line)
        return best

    @property
    def height(self):
        return len(self.lines)

    def render(self, x, y):
        terminal.layer(Layers.TOOLTIP.value)
        for i, line in enumerate(self.lines):
            terminal.printf(x, y + i, line)


def draw_tooltip():
    min_x, max_x, min_y, max_y = get_screen_bounds()
    current_map = World.fetch('current_map')

    mouse_pos_x = terminal.state(terminal.TK_MOUSE_X)
    mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y)
    mouse_map_pos_x = mouse_pos_x + min_x
    mouse_map_pos_y = mouse_pos_y + min_y

    if mouse_map_pos_x > Interface.map_screen_width - 1 or mouse_map_pos_y > Interface.map_screen_height - 1:
        return

    # On ne regarde que ce qui est visible.
    if current_map.visible_tiles[current_map.xy_idx(mouse_map_pos_x, mouse_map_pos_y)]:

        # est ce qu'on doit bien reconstruire le tooltip?
        old_tooltip, old_mouse_x, old_mouse_y = World.fetch('tooltip')
        tooltip = list()
        subjects = World.get_components(NameComponent, PositionComponent)
        for entity, (name, position) in subjects:
            if World.get_entity_component(entity, HiddenComponent):
                continue
            if mouse_map_pos_x == position.x and mouse_map_pos_y == position.y:
                tooltip.append(entity)

        # identique, on ne change rien.
        if tooltip == old_tooltip and mouse_map_pos_x == old_mouse_x and mouse_map_pos_y == old_mouse_y:
            return

        # nouveaux tooltips!
        World.insert('tooltip', (tooltip, mouse_map_pos_x, mouse_map_pos_y))
        terminal.layer(Layers.TOOLTIP.value)
        terminal.clear_area(0, 0, Interface.screen_width, Interface.screen_height)

        if not tooltip:
            return

        tip_boxes = list()
        for entity in tooltip:
            tip = Tooltip()
            tip.add(get_item_display_name(entity))
            # level
            level = World.get_entity_component(entity, Pools)
            if level:
                tip.add(f'Level : {level.level}')
            # attributes
            attributes = World.get_entity_component(entity, AttributesComponent)
            if attributes:
                description = ''
                if attributes.might > 3:
                    description += "Strong. "
                if attributes.might < 3:
                    description += "Weak. "
                if attributes.body > 3:
                    description += "Healthy. "
                if attributes.body < 3:
                    description += "Unhealthy. "
                if attributes.quickness > 3:
                    description += "Agile. "
                if attributes.quickness < 3:
                    description += "Clumsy. "
                if attributes.wits > 3:
                    description += "Smart. "
                if attributes.wits < 3:
                    description += "Stupid. "
                if not description:
                    description = "Quite average."
                tip.add(description)
            tip_boxes.append(tip)

        # render left or right of mouse
        arrow_y = mouse_pos_y
        if mouse_pos_x < Interface.screen_width // 2:
            # Left
            arrow = '←'
            arrow_x = mouse_pos_x + 1
        else:
            # right
            arrow = '→'
            arrow_x = mouse_pos_x - 1
        terminal.layer(Layers.TOOLTIP.value)
        terminal.color('white')
        terminal.printf(arrow_x, arrow_y, arrow)

        total_tip_height = 0
        for tooltip in tip_boxes:
            total_tip_height += tooltip.height

        y = mouse_pos_y - (total_tip_height // 2)
        while y + (total_tip_height // 2) > Interface.screen_height:
            y -= 1

        for tooltip in tip_boxes:
            if mouse_pos_x < Interface.screen_width // 2:
                print(f'right tooltip')
                x = mouse_pos_x + 1 #+ tooltip.width)
            else:
                print(f'left tooltip')
                x = mouse_pos_x - (1 + tooltip.width)
            tooltip.render(x, y)
            y += tooltip.height
        terminal.refresh()


def odraw_tooltip():
    # render camera
    min_x, max_x, min_y, max_y = get_screen_bounds()

    # mouse & tooltip
    mouse_pos_x = terminal.state(terminal.TK_MOUSE_X) + min_x
    mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y) + min_y

    current_map = World.fetch('current_map')
    subjects = World.get_components(PositionComponent, NameComponent)

    if mouse_pos_x > Interface.map_screen_width - 1 or mouse_pos_y > Interface.map_screen_height - 1:
        return

    if current_map.visible_tiles[current_map.xy_idx(mouse_pos_x, mouse_pos_y)]:
        old_tooltip, old_mouse_x, old_mouse_y = World.fetch('tooltip')

        tooltip = []
        for entity, (position, name) in subjects:
            if World.get_entity_component(entity, HiddenComponent):
                continue
            if position.x == mouse_pos_x and position.y == mouse_pos_y:
                tooltip.append(get_item_display_name(entity))

        # identique, on ne change rien.
        if tooltip == old_tooltip and mouse_pos_x == old_mouse_x and mouse_pos_y == old_mouse_y:
            return

        terminal.layer(Layers.TOOLTIP.value)
        terminal.clear_area(0, 0, current_map.width, current_map.height)

        if tooltip:
            terminal.color('white')
            width = 0
            for string in tooltip:
                if width < len(string):
                    width = len(string)
                width += 3

            if mouse_pos_x > 40:
                arrow_pos = (mouse_pos_x - 2 - min_x, mouse_pos_y - min_y)
                left_x = mouse_pos_x - width - min_x
                y = mouse_pos_y - min_y
                for string in tooltip:
                    terminal.printf(left_x, y, f'[bkcolor=gray]{string}[/color]')
                    padding = (width - len(string) - 1)
                    for i in range(0, padding):
                        terminal.printf(arrow_pos[0] - i, y, f'[bkcolor=gray] [/color]')
                    y += 1
                terminal.printf(arrow_pos[0], arrow_pos[1], f'[bkcolor=gray]->[/color]')
            else:
                arrow_pos = (mouse_pos_x + 1 - min_x, mouse_pos_y - min_y)
                left_x = mouse_pos_x + 3 - min_x
                y = mouse_pos_y - min_y
                for string in tooltip:
                    terminal.printf(left_x, y, f'[bkcolor=gray]{string}[/color]')
                    padding = width - len(string) - 1
                    for i in range(0, padding):
                        terminal.printf(arrow_pos[0] + i, y, f'[bkcolor=gray] [/color]')
                        y += 1
                terminal.printf(arrow_pos[0], arrow_pos[1], f'[bkcolor=gray]<-[/color]')
        World.insert('tooltip', (tooltip, mouse_pos_x, mouse_pos_y))
        terminal.refresh()
