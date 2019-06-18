import tcod as libtcod
from input_handlers import handle_keys


def main():
    # 画面サイズの変数
    screen_width = 30
    screen_height = 20

    # 画面の中央を整数(int())にして取得し、player_x,y変数に入れる
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # フォントの指定と(libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD）でどのタイプのファイルを読み取るのかを伝える
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # ここで実際に画面を作成する、画面サイズとタイトルとフルスクリーンにするかの真偽値の3つを指定している
    libtcod.console_init_root(screen_width, screen_height, "libtcod チュートリアル改訂", False)

    # デフォルトのコンソールを指定する
    con = libtcod.console_new(screen_width, screen_height)

    # キーボードとマウスの入力を表す変数
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # ゲームループと呼ばれるもの、ウィンドウを閉じるまでループする
    while not libtcod.console_is_window_closed():

        # ユーザー入力をキャプチャする関数、入力した内容で変数を更新する
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # "@"シンボルの色を指定する, conの値は描画先のコンソール
        libtcod.console_set_default_foreground(con, libtcod.green)

        # 最初の引数conは出力先のコンソール、ｘとｙ座標、"@"の記号を指定、背景をNONEにする
        libtcod.console_put_char(con, player_x, player_y, "@", libtcod.BKGND_NONE)

        # コンソールを指定してx,yの0からscreenまでの範囲を指定、後ろの0は高さ幅などの設定(0で最大)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        # 画面上に描画する機能
        libtcod.console_flush()

        # 移動後の＠をスペース（" "）で上書きして消す
        libtcod.console_put_char(con, player_x, player_y, " ", libtcod.BKGND_NONE)

        # handle_keysから各種変数を作っていく
        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move:
            dx, dy = move  # action.get("move")で取得した値がdx, dyに代入される
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

# 明示的に実行された時のみmain()関数を実行する
if __name__ == "__main__":
    main()

