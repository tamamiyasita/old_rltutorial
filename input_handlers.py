import tcod as libtcod

# libtcod.sys_check_for_eventに送る引数keyを辞書で定義する関数
# keyから参照されるvalueの値を使ってゲームをコントロールする
def handle_keys(key):
    # ＠の移動キー

    if key.vk == libtcod.KEY_UP:
        return {"move": (0, -1)}

    elif key.vk == libtcod.KEY_DOWN:
        return {"move": (0, 1)}

    elif key.vk == libtcod.KEY_LEFT:
        return {"move": (-1, 0)}

    elif key.vk == libtcod.KEY_RIGHT:
        return {"move": (1, 0)}

    # ALT + Enterでフルスクリーン
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {"fullscreen": True}

    # Exitゲーム
    elif key.vk == libtcod.KEY_ESCAPE:
        return {"exit": True}

    # 空の辞書を返す
    return {}
        