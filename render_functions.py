import tcod as libtcod


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
	# 視野内かどうかでタイルの明暗を変える
	if fov_recompute:
		for y in range(game_map.height):
			for x in range(game_map.width):
				visible = libtcod.map_is_in_fov(fov_map, x, y)
				wall = game_map.tiles[x][y].block_sight

				if visible:
					if wall:
						libtcod.console_set_char_background(con, x, y, colors.get("light_wall"), libtcod.BKGND_SET)
					else:
						libtcod.console_set_char_background(con, x, y, colors.get("light_ground"), libtcod.BKGND_SET)

					game_map.tiles[x][y].explored = True

				elif game_map.tiles[x][y].explored:
					if wall:
						libtcod.console_set_char_background(con, x, y, colors.get("dark_wall"), libtcod.BKGND_SET)
					else:
						libtcod.console_set_char_background(con, x, y, colors.get("dark_ground"), libtcod.BKGND_SET)

	# entitiesのリストをdraw_entityに渡して描画
	for entity in entities:
		draw_entity(con, entity, fov_map)

	# 実際に画面に描画するコマンド、コンソールを指定してx,yの0からscreenまでの描画範囲を指定、後ろの0は高さ幅などの設定(0で最大)
	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

def clear_all(con, entities):
	# 下記のclear_entityを使って描画された全てのentityをクリアするためのループ
	for entity in entities:
		clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
	# 視覚内のオブジェクトなら表示
	if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
		libtcod.console_set_default_foreground(con, entity.color)
		libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

	# 移動したentityを画面から消去する
def clear_entity(con, entity):
	libtcod.console_put_char(con, entity.x, entity.y, " ", libtcod.BKGND_NONE)
