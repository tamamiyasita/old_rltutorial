import tcod as libtcod
import itertools


def initialize_fov(game_map):
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    for x, y in itertools.product(range(game_map.width), range(game_map.height)):
        libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                    not game_map.tiles[x][y].blocked)

    return fov_map

def recompute_fov(fov_map, x, y, radius, light_wall=True, algorithm=0):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_wall, algorithm)
