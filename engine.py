import tcod as libtcod
import tcod.event as event

from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    # 画面サイズの変数
    screen_width = 80
    screen_height = 70
    map_width = 80
    map_height = 45

    # 壁とタイルの色を初期化
    colors = {
        "dark_wall": libtcod.Color(0, 0, 100),
        "dark_ground": libtcod.Color(50, 50, 150)
    }

    # デモ用にプレイヤーとNPCをEntityから生成する、位置と＠とその色を決定しentitiesに入れる
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", libtcod.green)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", libtcod.yellow)
    entities = [npc, player]
    # フォントの指定と(libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD）でどのタイプのファイルを読み取るのかを伝える
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # ここで実際に画面を作成する、画面サイズとタイトルとフルスクリーンにするかの真偽値の3つを指定している
    libtcod.console_init_root(screen_width, screen_height, "libtcod チュートリアル改訂", False)

    # デフォルトのコンソールを指定する
    con = libtcod.console.Console(screen_width, screen_height)

    # ゲームマップの初期化
    game_map = GameMap(map_width, map_height)
    game_map.make_map()

    # ゲームループと呼ばれるもの、ウィンドウを閉じるまでループする
    while True:
        # entityをここから呼び出す
        render_all(con, entities, game_map, screen_width, screen_height, colors)

        # 画面上に描画する機能
        libtcod.console_flush()

        # 移動後のentitiesをスペース（" "）で上書きして消す
        clear_all(con, entities)

        # event.get()イテレータをループで回し各キーの押下判定を行う
        for events in libtcod.event.get():
            if events.type == "QUIT":
                raise SystemExit()

            if events.type == "KEYDOWN":

                # handle_keysから各種変数を作っていく
                action = handle_keys(events)

                move = action.get("move")
                exit = action.get("exit")
                fullscreen = action.get("fullscreen")
                
                if move:
                    dx, dy = move  # action.get("move")で取得した値がdx, dyに代入される
                    if not game_map.is_blocked(player.x + dx, player.y + dy):
                        player.move(dx, dy)

                if exit:
                    raise SystemExit()

                if fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

# 明示的に実行された時のみmain()関数を実行する
if __name__ == "__main__":
    main()

