import tcod as libtcod
import tcod.event as event

from game_states import GameStates

def handle_keys(events, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(events)

    elif game_state == GameStates.PLAYERS_DEAD:
        return handle_player_dead_keys(events)

    elif game_state == GameStates.SHOW_INVENTORY:
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

    # ALT + Enterでフルスクリーン
    if events.sym == event.K_RETURN and event.KMOD_LALT:
        return {"fullscreen": True}

    # Exitゲーム
    elif events.sym == event.K_ESCAPE:
        return {"exit": True}

    # キーが押されてない時は空の辞書を返す
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