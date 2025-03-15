
extends Node

var rooms = {}

func _ready():
    var peer = ENetMultiplayerPeer.new()
    peer.create_server(7777, 10)
    multiplayer.multiplayer_peer = peer
    print("✅ Server is running!")

    multiplayer.peer_connected.connect(_on_player_connected)
    multiplayer.peer_disconnected.connect(_on_player_disconnected)

func _on_player_connected(player_id):
    join_or_create_room(player_id)

func _on_player_disconnected(player_id):
    for room_id in rooms.keys():
        if player_id in rooms[room_id]:
            rooms[room_id].erase(player_id)
            if rooms[room_id].size() == 0:
                rooms.erase(room_id)

func join_or_create_room(player_id):
    for room_id in rooms.keys():
        if rooms[room_id].size() < 6:
            rooms[room_id].append(player_id)
            check_and_start_race(room_id)
            return

    var new_room_id = str(rooms.size() + 1)
    rooms[new_room_id] = [player_id]

func check_and_start_race(room_id):
    if rooms[room_id].size() == 6:
        rpc("load_track", room_id)

@rpc("any_peer")
func load_track(room_id):
    var race_scene = load("res://scenes/track.tscn")
    get_tree().change_scene_to_packed(race_scene)
    var track = get_tree().get_first_node_in_group("Track")
    var start_positions = track.get_node("StartPositions").get_children()

    for i in range(rooms[room_id].size()):
        var player_id = rooms[room_id][i]
        var pos = start_positions[i].global_transform.origin
        rpc("spawn_player", player_id, pos)

@rpc("any_peer")
func spawn_player(peer_id, position):
    var player_scene = load("res://scenes/player.tscn")
    var player = player_scene.instantiate()
    player.name = str(peer_id)
    player.position = position
    add_child(player)
