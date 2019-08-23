import tcod as libtcod
import tcod.event as event


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError("Cannot have a menu with more than 26 options.")

    # ヘッダーの高さと行の計算
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # メニューのコンソールを作る
    window = libtcod.console.Console(width, height)

    # 自動折り返しでヘッダをprintする
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # すべてのオプションをprintする
    y = header_height
    letter_index = ord("a")
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # ウィンドウの内容をルートコンソールにblitする
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
    # インベントリメニューの表示
    if len(inventory.items) == 0:
        options = ["Inventory is empty."]
    else:
        options = [item.name for item in inventory.items]

    menu(con, header, options, inventory_width, screen_width, screen_height)

def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, (screen_width // 2), (screen_height // 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             "Tombs of Eternia")
    libtcod.console_print_ex(0, screen_width // 2, int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             "By (Your name here)")
    menu(con, "", ["play a new game", "Continue last game", "Quit"], 24, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ["Constitution (+20 HP, from {0})".format(player.fighter.max_hp),
               "Strength (+1 attack, from {0})".format(player.fighter.power),
               "Agility (+1 defense, from {0})".format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "Character_Information")
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "Level: {0}".format(player.level.cureent_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "Experience: {0}".format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "Experience to Level: {0}".format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "Maximum HP: {0}".format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "Attack: {0}".format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, "Defense: {0}".format(player.fighter.defense))

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)