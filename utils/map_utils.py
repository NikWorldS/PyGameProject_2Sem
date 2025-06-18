def get_collision_grid(tmx_data, collision_layer_name):
    width = tmx_data.width
    height = tmx_data.height

    grid = [[0 for _ in range(width)] for _ in range(height)]

    layer = tmx_data.get_layer_by_name(collision_layer_name)

    for y in range(height):
        for x in range(width):
            tile = layer.data[y][x]
            if tile:
                grid[y][x] = 1  # препятствие

    return grid