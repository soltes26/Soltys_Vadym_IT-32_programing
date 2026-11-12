import math

NAME = "Vadym Soltys"
GROUP = "IT-32"

# --- ЗАМІНІТЬ НА СВОЇ ВИМІРИ ---------------------------------------------
ROOM_L, ROOM_W, ROOM_H = 4.0, 3.2, 2.6   # довжина, ширина, висота кімнати, м
DOOR_W, DOOR_H = 0.9, 2.0                # двері, м
WINDOW_W, WINDOW_H = 1.3, 1.4            # вікно, м
TILE_SIDE = 0.40                         # плитка 40 x 40 см, у метрах
TILE_PRICE = 55.90                       # ціна однієї плитки, грн
# --------------------------------------------------------------------------

SPARE = 0.10          # запас 10 %
PAINT_PER_M2 = 0.1    # 1 л на 10 м2 за один шар
LAYERS = 2
CAN_VOLUME = 2.5      # банка, л


def main():
    print(f"{NAME}, {GROUP}")

    floor_area = ROOM_L * ROOM_W
    wall_area = (2 * (ROOM_L + ROOM_W) * ROOM_H
                 - DOOR_W * DOOR_H - WINDOW_W * WINDOW_H)
    floor_diag = math.hypot(ROOM_L, ROOM_W)
    room_diag = math.dist((0, 0, 0), (ROOM_L, ROOM_W, ROOM_H))

    tiles_exact = floor_area / (TILE_SIDE * TILE_SIDE)
    tiles_to_buy = math.ceil(tiles_exact * (1 + SPARE))

    paint = wall_area * PAINT_PER_M2 * LAYERS
    cans = math.ceil(paint / CAN_VOLUME)

    cost_mul = tiles_to_buy * TILE_PRICE
    cost_sum = 0.0
    for _ in range(tiles_to_buy):
        cost_sum += TILE_PRICE

    print(f"room:          {ROOM_L} x {ROOM_W} x {ROOM_H} m")
    print(f"floor area:    {floor_area:.2f} m2")
    print(f"wall area:     {wall_area:.2f} m2 (without door and window)")
    print(f"floor diag:    {floor_diag:.2f} m")
    print(f"room diag:     {room_diag:.2f} m")
    print()
    print(f"tiles exact:   {tiles_exact:.2f}")
    print(f"  round:       {round(tiles_exact)}")
    print(f"  floor:       {math.floor(tiles_exact)}")
    print(f"  ceil:        {math.ceil(tiles_exact)}")
    print(f"tiles to buy:  {tiles_to_buy} (+{SPARE:.0%} spare)")
    print(f"paint:         {paint:.2f} l -> {cans} cans of {CAN_VOLUME} l")
    print()
    print(f"tiles cost:    {cost_mul:.2f} UAH")
    print(f"sum == mul:    {cost_sum == cost_mul}")
    print(f"isclose:       {math.isclose(cost_sum, cost_mul)}")
    print(f"difference:    {abs(cost_sum - cost_mul)}")


if __name__ == "__main__":
    main()
