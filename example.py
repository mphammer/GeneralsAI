
import generals


# 1v1
#g = generals.Generals('ry0FVyx_g', 'frank', '1v1')

# ffa
# g = generals.Generals('your userid', 'your username', 'ffa')

# private game

room = input("Please enter the room id: ")

g = generals.Generals('ry0FVyx_g', 'frank', 'private', room)

# 2v2 game
# g = generals.Generals('your userid', 'your username', 'team')

for update in g.get_updates():

    # get position of your general
    pi = update['player_index']
    y, x = update['generals'][pi]

    # move units from general to arbitrary square
    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if (0 <= y+dy < update['rows'] and 0 <= x+dx < update['cols']
                and update['tile_grid'][y+dy][x+dx] != generals.MOUNTAIN):
            g.move(y, x, y+dy, x+dx)
            break
