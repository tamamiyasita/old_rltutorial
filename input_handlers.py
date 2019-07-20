import tcod as libtcod
import tcod.event as event


def handle_keys(events):
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
        