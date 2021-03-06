from bearlibterminal import terminal

import sys

from player_systems.try_move_player import try_move_player, try_next_level, move_on_click_player, action_wait
from inventory_system.inventory_functions import get_available_item_actions
from state import States
from ui_system.ui_enums import NextLevelResult, ItemMenuResult, MainMenuSelection, OptionMenuSelection, YesNoResult
from ui_system.show_menus import show_main_options_menu, show_item_screen, show_character_menu, show_victory_menu, \
    show_quit_game_menu
from ui_system.interface import Interface, GraphicalModes
from world import World
from texts import Texts
from components.targeting_component import TargetingComponent
import config
from data.save_and_load import save_game
from ui_system.render_camera import get_map_coord_with_mouse_when_zooming


def player_input():
    if terminal.has_input():
        key = terminal.read()
        has_act = False

        if key == terminal.TK_MOUSE_LEFT:
            mouse_map_pos_x, mouse_map_pos_y = get_map_coord_with_mouse_when_zooming()
            # move_order_player(mouse_map_pos_x, mouse_map_pos_y)
            has_act = move_on_click_player(mouse_map_pos_x, mouse_map_pos_y)

        elif key == terminal.TK_LEFT or key == terminal.TK_KP_4 or key == terminal.TK_H:
            has_act = try_move_player(-1, 0)
        elif key == terminal.TK_RIGHT or key == terminal.TK_KP_6 or key == terminal.TK_L:
            has_act = try_move_player(1, 0)
        elif key == terminal.TK_UP or key == terminal.TK_KP_8 or key == terminal.TK_K:
            has_act = try_move_player(0, -1)
        elif key == terminal.TK_DOWN or key == terminal.TK_KP_2 or key == terminal.TK_J:
            has_act = try_move_player(0, 1)
        #diagonal
        elif key == terminal.TK_KP_9 or key == terminal.TK_Y:
            has_act = try_move_player(1, -1)
        elif key == terminal.TK_KP_7 or key == terminal.TK_U:
            has_act = try_move_player(-1, -1)
        elif key == terminal.TK_KP_3 or key == terminal.TK_N:
            has_act = try_move_player(1, 1)
        elif key == terminal.TK_KP_1 or key == terminal.TK_B:
            has_act = try_move_player(-1, 1)

        # others
            '''
            elif key == terminal.TK_G:
                get_item(World.fetch('player'))
            '''
        elif key == terminal.TK_I:
            show_item_screen()
            return States.SHOW_INVENTORY
        elif key == terminal.TK_C:
            show_character_menu()
            return States.CHARACTER_SHEET
        elif key == terminal.TK_SPACE:
            next_lvl = try_next_level()
            if next_lvl == NextLevelResult.NEXT_FLOOR:
                return States.NEXT_LEVEL
            elif next_lvl == NextLevelResult.EXIT_DUNGEON:
                show_victory_menu()
                return States.VICTORY
        elif key == terminal.TK_KP_5 or key == terminal.TK_Z:
            action_wait(World.fetch('player'))
            return States.TICKING

        elif key == terminal.TK_PAGEUP:
            Interface.set_zoom(Interface.zoom + 1)
            return States.REFRESH
        elif key == terminal.TK_PAGEDOWN:
            Interface.set_zoom(Interface.zoom - 1)
            return States.REFRESH
        elif key == terminal.TK_ENTER:
            current_map = World.fetch('current_map')
            current_map.revealed_tiles = [True] * (current_map.height * current_map.width)
            return States.REFRESH

        elif key == terminal.TK_ESCAPE:
            show_quit_game_menu()
            return States.CONFIRM_QUIT

        elif key == terminal.TK_CLOSE:
            save_game(World)
            terminal.close()
            sys.exit()
        else:
            return States.AWAITING_INPUT

        # has not moved?
        if not has_act:
            return States.AWAITING_INPUT
        return States.TICKING
    return States.AWAITING_INPUT


def targeting_input(item, mouse_coords, valid_target=False):
    cancel = False
    if terminal.has_input():
        logs = World.fetch('logs')
        key = terminal.read()
        if key == terminal.TK_ESCAPE:
            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]{Texts.get_text("YOU_CHANGE_MIND")}[/color]')
            cancel = True
        elif key == terminal.TK_MOUSE_LEFT:
            print(f'targeting input: {item}, {mouse_coords}, {valid_target}')
            if valid_target and item:
                return ItemMenuResult.SELECTED, item, mouse_coords
            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]{Texts.get_text("NOTHING_TO_TARGET")}[/color]')
            cancel = True
        elif key == terminal.TK_CLOSE:
            save_game(World)
            terminal.close()
            sys.exit()

    if cancel:
        World.remove_component(TargetingComponent, World.fetch('player'))
        return ItemMenuResult.CANCEL, None, None
    return ItemMenuResult.NO_RESPONSE, None, None


def input_escape_to_quit():
    if terminal.has_input():
        key = terminal.read()
        if key == terminal.TK_ESCAPE:
            return ItemMenuResult.SELECTED
        elif key == terminal.TK_CLOSE:
            save_game(World)
            terminal.close()
    return ItemMenuResult.NO_RESPONSE


def yes_no_input():
    if terminal.has_input():
        key = terminal.read()
        if key != terminal.TK_MOUSE_MOVE:
            if key == terminal.TK_ESCAPE:
                return YesNoResult.NO
            elif key == terminal.TK_CLOSE:
                save_game(World)
                terminal.close()
                sys.exit()
            else:
                index = terminal.state(terminal.TK_CHAR) - ord('a')
                if index == 0:
                    return YesNoResult.NO
                elif index == 1:
                    return YesNoResult.YES
    return YesNoResult.NO_RESPONSE


def identify_menu_input(item_list):
    # return ItemMenuResult, new_state, item selected
    if terminal.has_input():
        key = terminal.read()
        if key != terminal.TK_MOUSE_MOVE:
            if key == terminal.TK_ESCAPE:
                return ItemMenuResult.CANCEL, None, None
            elif key == terminal.TK_CLOSE:
                save_game(World)
                terminal.close()
                sys.exit()
            else:
                index = terminal.state(terminal.TK_CHAR) - ord('a')
                if 0 <= index < len(item_list):
                    print(f'identify item input: item {index} has been chosen.')
                    return ItemMenuResult.SELECTED, States.TICKING, item_list[index]
    return ItemMenuResult.NO_RESPONSE, None, None


def known_cursed_inventory_input(item_list):
    # return ItemMenuResult, new_state, item selected
    if terminal.has_input():
        key = terminal.read()
        if key != terminal.TK_MOUSE_MOVE:
            if key == terminal.TK_ESCAPE:
                return ItemMenuResult.CANCEL, None, None
            elif key == terminal.TK_CLOSE:
                save_game(World)
                terminal.close()
                sys.exit()
            else:
                index = terminal.state(terminal.TK_CHAR) - ord('a')
                if 0 <= index < len(item_list):
                    print(f'curse removal input: item {index} has been chosen.')
                    return ItemMenuResult.SELECTED, States.TICKING, item_list[index]
    return ItemMenuResult.NO_RESPONSE, None, None


def inventory_input(item_list):
    # return ItemMenuResult, new_state, item selected
    if terminal.has_input():
        key = terminal.read()
        if key != terminal.TK_MOUSE_MOVE:
            if key == terminal.TK_ESCAPE:
                return ItemMenuResult.CANCEL, None, None
            elif key == terminal.TK_CLOSE:
                save_game(World)
                terminal.close()
                sys.exit()
            else:
                index = terminal.state(terminal.TK_CHAR) - ord('a')
                if 0 <= index < len(item_list):
                    print(f'inventory input: item {index} has been chosen.')
                    # show_selected_item_screen(f'{Texts.get_text("INVENTORY")}', item_list[index])

                    return ItemMenuResult.SELECTED, States.SHOW_SELECTED_ITEM_MENU, item_list[index]
    return ItemMenuResult.NO_RESPONSE, None, None


def inventory_selected_item_input(chosen_item):
    if terminal.has_input():
        key = terminal.read()
        if key != terminal.TK_MOUSE_MOVE:
            if key == terminal.TK_ESCAPE:
                return ItemMenuResult.DESELECT, None
            elif key == terminal.TK_CLOSE:
                save_game(World)
                terminal.close()
                sys.exit()
            else:
                index = terminal.state(terminal.TK_CHAR) - ord('a')
                action_list = get_available_item_actions(chosen_item)
                if 0 <= index < len(action_list):
                    return ItemMenuResult.ACTION, action_list[index]
    return ItemMenuResult.NO_RESPONSE, None


def main_menu_input():
    if terminal.has_input():
        key = terminal.read()
        index = terminal.state(terminal.TK_CHAR) - ord('a')
        if key == terminal.TK_ESCAPE or index == 3:
            return MainMenuSelection.QUIT
        elif index == 0:
            return MainMenuSelection.NEWGAME
        elif index == 1:
            return MainMenuSelection.LOAD_GAME
        elif index == 2:
            return MainMenuSelection.OPTION
        elif key == terminal.TK_CLOSE:
            save_game(World)
            terminal.close()
            sys.exit()
    return MainMenuSelection.NO_RESPONSE


def option_menu_input():
    if terminal.has_input():
        key = terminal.read()
        index = terminal.state(terminal.TK_CHAR) - ord('a')
        if key == terminal.TK_ESCAPE or index == 2:
            return OptionMenuSelection.BACK_TO_MAIN_MENU
        elif key == terminal.TK_CLOSE:
            save_game(World)
            terminal.close()
            sys.exit()
        elif index == 0:
            # change language
            if Texts.get_current_language() == 'fr':
                Texts.set_language('en')
            else:
                Texts.set_language('fr')
            show_main_options_menu()
        elif index == 1:
            # graphical mode
            if Interface.mode == GraphicalModes.ASCII:
                terminal.clear()
                Interface.change_graphical_mode(GraphicalModes.TILES)
            elif Interface.mode == GraphicalModes.TILES:
                terminal.clear()
                Interface.change_graphical_mode(GraphicalModes.ASCII)
            show_main_options_menu()
    return MainMenuSelection.NO_RESPONSE


def character_sheet_input():
    if terminal.has_input():
        key = terminal.read()
        if key == terminal.TK_ESCAPE:
            terminal.clear_area(0, 0, Interface.screen_width, Interface.screen_height)
            terminal.refresh()
        elif key == terminal.TK_CLOSE:
            save_game(World)
            terminal.close()
            sys.exit()
