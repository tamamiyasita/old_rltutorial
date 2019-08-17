import tcod as libtcod
import tcod.event as event

from game_states import GameStates

def handle_keys(events, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(events)

    elif game_state == GameStates.PLAYERS_DEAD:
        return handle_player_dead_keys(events)

    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(events)

    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(events)

    return {}


def handle_player_turn_keys(events):
    # ＠の移動キー
    if events.sym == event.K_UP:
        return {"move": (0, -1)}

    elif events.sym == event.K_DOWN:
        return {"move": (0, 1)}

    elif events.sym == event.K_LEFT:
        return {"move": (-1, 0)}

    elif events.sym == event.K_RIGHT:
        return {"move": (1, 0)}
    
    elif events.sym == event.K_HOME:
        return {"move": (-1, -1)}

    elif events.sym == event.K_END:
        return {"move": (-1, 1)}

    elif events.sym == event.K_PAGEUP:
        return {"move": (1, -1)}

    elif events.sym == event.K_PAGEDOWN:
        return {"move": (1, 1)}

    if events.sym == event.K_g:
        return {"pickup": True}

    elif events.sym == event.K_i:
        return {"show_inventory": True}

    elif events.sym == event.K_d:
        return {"drop_inventory": True}

    # ALT + Enterでフルスクリーン
    if events.sym == event.K_RETURN:
        return {"fullscreen": True}

    # Exitゲーム
    elif events.sym == event.K_ESCAPE:
        return {"exit": True}

    # キーが押されてない時は空の辞書を返す
    return {}

def handle_targeting_keys(events):
    if events.sym == event.K_ESCAPE:
        return {"exit": True}

    return {}

def handle_player_dead_keys(events):
    if events.sym == event.K_i:
        return {"show_inventory": True}

    if events.sym == event.K_RETURN and event.K_LALT:
        return {"fullscreen": True}

    elif events.sym == event.K_ESCAPE:
        return {"exit": True}

    return {}

def handle_inventory_keys(events):
    index = events.sym - ord("a")

    if 0 <= index < 26:
        return {"inventory_index": index}

    if events.sym == event.K_RETURN and event.K_LALT:
        return {"fullscreen": True}

    elif events.sym == event.K_ESCAPE:
        return {"exit": True}

    return {}

def handle_main_menu(events):
    if events.sym == event.K_a:
        return {"new_game": True}
    elif events.sym == event.K_b:
        return {"load_game": True}
    elif events.sym == event.K_c:
        return {"exit": True}

    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.tile)

    if event.BUTTON_LEFT:
        return {"left_click": (x, y)}
    elif event.BUTTON_RIGHT:
        return {"right_click": (x, y)}

    return {}

