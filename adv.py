from room import Room
from player import Player
from world import World

import random
from util import Graph, Queue, Stack
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# holds the vistied rooms
visited = {}
# create a list for path
master_path = []
# list of reverse commands to enable going backwards
reverse_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
# takes current room and appends to `visited` dictionary
# also gets exits so we can start traversal
visited[player.current_room.id] = player.current_room.get_exits()
# begin traversal, if length of vistied is less than length of room  graph
while len(visited) < len(room_graph) - 1:
    # check if current room if is `visited` dictionary
    if player.current_room.id not in visited:
        # add current_room to the `visited`
        visited[player.current_room.id] = player.current_room.get_exits()
        # grab previous direction
        previous_direction = master_path[-1]
        # remove the previous direction to avoid going that way
        visited[player.current_room.id].remove(previous_direction)
    # change traversal to look through all rooms, not just the shortest path
    while len(visited[player.current_room.id]) == 0:
        # remove previous exits set
        previous_direction = master_path.pop()
        # add last set of exits to traversal path
        traversal_path.append(previous_direction)
        # use travel funstion on player to move around to previous room
        # check if those rooms are visited
        player.travel(previous_direction)
    # check current_room's exits and find last room on list, go to that room.
    next_move = visited[player.current_room.id].pop(0)
    # append to path as this is the right directions
    traversal_path.append(next_move)
    # append it to record of going there
    master_path.append(reverse_direction[next_move])
    # use the directions dictionary to go backwards through rooms
    player.travel(next_move)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
