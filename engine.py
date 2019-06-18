import tcod as libtcod

def main():
    # 画面サイズの変数
    screen_width = 15
    screen_height = 15

    # フォントの指定と(libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD）でどのタイプのファイルを読み取るのかを伝える
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # ここで実際に画面を作成する、画面サイズとタイトルとフルスクリーンにするかの真偽値の3つを指定している
    libtcod.console_init_root(screen_width, screen_height, "libtcod チュートリアル改訂", False)

    # ゲームループと呼ばれるもの、ウィンドウを閉じるまでループする
    while not libtcod.console_is_window_closed():

        # "@"シンボルの色を指定する, 0の値はその描画先のコンソールのこと
        libtcod.console_set_default_foreground(0, libtcod.green)

        # 最初の引数0は出力先のコンソール、ｘとｙ座標、"@"の記号を指定、背景をNONEにする
        libtcod.console_put_char(0, 7, 7, "@", libtcod.BKGND_NONE)

        # 画面上に描画する機能
        libtcod.console_flush()

        # キーボードの入力を取得し、key変数に入れる
        key = libtcod.console_check_for_keypress()

        # 押されたキーがESCならループにTrueを返しウィンドウを閉じる
        if key.vk == libtcod.KEY_ESCAPE:
            return True

# 明示的に実行された時のみmain()関数を実行する
if __name__ == "__main__":
    main()

