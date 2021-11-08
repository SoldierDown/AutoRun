cur_yellows = 9
cur_purples = 4
cur_blues = 11



yellow_per_gold = 2
purple_per_gold = 5
per_gold = 41

yellow2blue = 3
purple2blue = 2



cur_total = cur_yellows * yellow2blue + cur_purples * purple2blue + cur_blues
can_afford = cur_total // per_gold

n_y2b = cur_yellows - can_afford * yellow_per_gold
n_p2b = cur_purples - can_afford * purple_per_gold

print('can afford: {}'.format(can_afford))
print('yellow to blue: {}'.format(n_y2b))
print('purple to blue: {}'.format(n_p2b))