field_rows = int(input())
ships = []
ships_health = []
destroyed_ships = 0
missed = 0

for x in range(field_rows):
    row = list(map(int, input().split()))
    for y in range(len(row)):
        if row[y] > 0:
            ship_health = row[y]
            ships.append([x, y, ship_health])

attacks = list(input().split())

for attack in range(len(attacks)):
    destroyed = False
    attack_x = int(attacks[attack][0])
    attack_y = int(attacks[attack][2])
    for ship in range(len(ships)):
        if ships[ship] is not None:
            if attack_x == ships[ship][0] and attack_y == ships[ship][1]:
                if ships[ship][2] - 1 > 0:
                    ships[ship][2] -= 1
                else:
                    destroyed_ships += 1
                    destroyed = True
                    ships[ship] = None
                    break
        else:
            continue
    if not destroyed:
        missed += 1

print(f"Destroyed ships: {destroyed_ships}")
print(f"Missed shots: {missed}")
