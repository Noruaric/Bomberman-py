import sys
import random
import os
from time import time

import pygame

if os.getcwd()[:2] != "c:":  # C: étant la lettre de mon disque [SSD] sur mon pc perso
    try:
        sys.path.insert(0, f"{os.getcwd()[:2]}\\projet Bomberman\\module")
    except FileNotFoundError:
        pass
import pygame_menu  # pylint: disable=import-error, wrong-import-position
import bomber_constant as bc  # pylint: disable=wrong-import-position


class Player:
    """represent a bomber aka player"""

    def __init__(self, start_cord_x: int, start_cord_y: int) -> None:
        self.blast = 1  # aka explosion radius
        self.speed = 1  # aka player walk speed
        self.bomb = 1  # aka nomber of bomb
        self.heart = 1  # heart of player
        self.special_item = [False, False, False, False]
        self.placed_bombs = 0
        # ╚> aka the number of bomb the player have placed AND that did'nt explode
        self.power_up_colected = []
        # ╚> aka all the power colected even if max of the type is pass
        self.state = []
        # ╚> represent all state that are applied to the player
        self.coordinate = [start_cord_x, start_cord_y]
        self.graphic_coords = [start_cord_x-0.5, start_cord_y-0.5]
        self.p_frame = 0
        self.frame = 0
        self.animating_state = 'Walk_down'
        #                       ╚> animation name
        self.animation_dict = {
            "K.O.": [
                pygame.transform.scale(
                    pygame.image.load(i),
                    (
                        32 * RESCAL_COEF // 1.5,
                        32 * RESCAL_COEF // 1.5,
                    ),
                )
                for i in (bc.BOMBERS_ANIMATION_SPRITE["WHITE"]["K.O."])
            ],
            "Walk_up": [
                pygame.transform.scale(
                    pygame.image.load(i),
                    (
                        32 * RESCAL_COEF // 1.5,
                        32 * RESCAL_COEF // 1.5,
                    ),
                )
                for i in (bc.BOMBERS_ANIMATION_SPRITE["WHITE"]["Walk_up"])
            ],
            "Walk_down": [
                pygame.transform.scale(
                    pygame.image.load(i),
                    (
                        32 * RESCAL_COEF // 1.5,
                        32 * RESCAL_COEF // 1.5,
                    ),
                )
                for i in (bc.BOMBERS_ANIMATION_SPRITE["WHITE"]["Walk_down"])
            ],
            "Walk_left": [
                pygame.transform.scale(
                    pygame.image.load(i),
                    (
                        32 * RESCAL_COEF // 1.5,
                        32 * RESCAL_COEF // 1.5,
                    ),
                )
                for i in (bc.BOMBERS_ANIMATION_SPRITE["WHITE"]["Walk_left"])
            ],
            "Walk_right": [
                pygame.transform.scale(
                    pygame.image.load(i),
                    (
                        32 * RESCAL_COEF // 1.5,
                        32 * RESCAL_COEF // 1.5,
                    ),
                )
                for i in (bc.BOMBERS_ANIMATION_SPRITE["WHITE"]["Walk_right"])
            ],
        }
        self.image = self.animation_dict["Walk_down"][0]
        self.holding = (False, None)

    def power_collected(self, power_type: str) -> None:
        """todo"""
        if power_type == bc.BOMB_PLUS and self.bomb < 8:
            self.bomb += 1
        if power_type == bc.SPEED_PLUS and self.speed < 8:
            self.speed += 1
        if power_type == bc.BLAST_PLUS and self.blast < 8:
            self.blast += 1
        if power_type == bc.POWER_GLOVE_ITEM:
            self.special_item[bc.POWER_GLOVE_INDEX] = power_type
        if power_type == bc.KICK_ITEM:
            self.special_item[bc.FOOTKICK_INDEX] = power_type
        if power_type == bc.FOOTKICK_ITEM:
            self.special_item[bc.KICK_INDEX] = power_type
        if power_type == bc.SPIKE_BOMB_ITEM:
            self.special_item[bc.SPIKE_BOMB_INDEX] = power_type
        if power_type == bc.BOMB_MINUS and self.bomb > 1:
            self.bomb -= 1
            self.power_up_colected.remove(bc.BOMB_PLUS)
        if power_type == bc.SPEED_MINUS and self.speed > 1:
            self.speed -= 1
            self.power_up_colected.remove(bc.SPEED_PLUS)
        if power_type == bc.BLAST_MINUS and self.blast > 1:
            self.blast -= 1
            self.power_up_colected.remove(bc.BLAST_PLUS)
        self.power_up_colected.append(power_type)

    def place_bomb(self, date: int, bombs: list["bomb"]) -> "bomb":
        """to do"""
        for b in bombs:
            if [b.coordinates[0], b.coordinates[1]] == self.coordinate:
                if self.special_item[bc.POWER_GLOVE_INDEX]:
                    pass
                else:
                    return
        if self.placed_bombs != self.bomb:
            self.placed_bombs += 1
            return bomb(
                self.blast,
                self.special_item[bc.SPIKE_BOMB_INDEX],
                [int(self.coordinate[0]), int(self.coordinate[1])],
                date,
                self,
            )

    def walk_up(self, arena: list[str], bombs: list["bomb"], date: int) -> None:
        if self.animating_state == 'Walk_up':
            self.frame +=0.1
        self.p_frame = date
        self.animating_state = "Walk_up"
        for b in bombs:
            if b is None: continue
            if b.coordinates == (
                int(self.coordinate[0]),
                int(self.coordinate[1] - (1/135 + 1/135 * self.speed)),
            ) or b.coordinates == (
                int(self.coordinate[0]),
                int(self.coordinate[1] - 0.5),
            ):
                return
        if int(self.coordinate[1]) > 0.5:
            if (
                arena[int(self.coordinate[1]-(1/135 + 1/135 * self.speed))][
                    int(self.coordinate[0])
                ]
                not in bc.ALL_BLOCK
            ) and (
                arena[int(self.coordinate[1]-0.5)][
                    int(self.coordinate[0])
                ]
                not in bc.ALL_BLOCK
            ):
                self.coordinate[1] -= 1/135 + 1/135 * self.speed
                if self.coordinate[1] <= 0.5:
                    self.coordinate[1] = 0.5
            else:
                int(self.coordinate[1])+0.5
        else:
            self.coordinate[1] -= 1/135 + 1/135 * self.speed
            if self.coordinate[1] <= 0.5:
                self.coordinate[1] = 0.5

    def walk_down(self, arena: list[str], bombs: list["bomb"], date: int) -> None:
        if self.animating_state == 'Walk_down':
            self.frame +=0.1
        self.p_frame = date
        self.animating_state = "Walk_down"
        for b in bombs:
            if b is None: continue
            if b.coordinates == (
                int(self.coordinate[0]),
                int(self.coordinate[1] + (1/135 + 1/135 * self.speed)),
            ) or b.coordinates == (
                int(self.coordinate[0]),
                int(self.coordinate[1] + 0.5),
            ):
                return
        if int(self.coordinate[1]) < 8.5:
            if (
                arena[int(self.coordinate[1]+(1/135 + 1/135 * self.speed))][
                    int(self.coordinate[0])
                ]
                not in bc.ALL_BLOCK
            ) and (
                arena[int(self.coordinate[1]+0.5)][
                    int(self.coordinate[0])
                ]
                not in bc.ALL_BLOCK
            ):
                self.coordinate[1] += 1/135 + 1/135 * self.speed
                if self.coordinate[1] >= 8.5:
                    self.coordinate[1] = 8.4999
            else:
                int(self.coordinate[1])-0.5
        else:
            self.coordinate[1] += 1/135 + 1/135 * self.speed
            if self.coordinate[1] >= 8.5:
                self.coordinate[1] = 8.4999

    def walk_left(self, arena: list[str], bombs: list["bomb"], date: int) -> None:
        if self.animating_state == 'Walk_left':
            self.frame +=0.1
        self.p_frame = date
        self.animating_state = "Walk_left"
        for b in bombs:
            if b is None: continue
            if b.coordinates == (
                int(self.coordinate[0]- (1/135 + 1/135 * self.speed)),
                int(self.coordinate[1]),
            ) or b.coordinates == (
                int(self.coordinate[0] - 0.5),
                int(self.coordinate[1]),
            ):
                return
        if int(self.coordinate[1]) > 0.5:
            if (
                arena[int(self.coordinate[1])][
                    int(self.coordinate[0]-(1/135 + 1/135 * self.speed))
                ]
                not in bc.ALL_BLOCK
            ) and (
                arena[int(self.coordinate[1])][
                    int(self.coordinate[0]-0.5)
                ]
                not in bc.ALL_BLOCK
            ):
                self.coordinate[0] -= 1/135 + 1/135 * self.speed
                if self.coordinate[0] <= 0.5:
                    self.coordinate[0] = 0.5
            else:
                int(self.coordinate[0])+0.5
        else:
            self.coordinate[0] -= 1/135 + 1/135 * self.speed
            if self.coordinate[0] <= 0.5:
                self.coordinate[0] = 0.5

    def walk_right(self, arena: list[str], bombs: list["bomb"], date: int) -> None:
        if self.animating_state == 'Walk_right':
            self.frame +=0.1
        self.p_frame = date
        self.animating_state = "Walk_right"
        for b in bombs:
            if b is None: continue
            if b.coordinates == (
                int(self.coordinate[0]+ (1/135 + 1/135 * self.speed)),
                int(self.coordinate[1] ),
            ) or b.coordinates == (
                int(self.coordinate[0]+ 0.5),
                int(self.coordinate[1] ),
            ):
                return
        if int(self.coordinate[1]) < 12.5:
            if (
                arena[int(self.coordinate[1])][
                    int(self.coordinate[0]+(1/135 + 1/135 * self.speed))
                ]
                not in bc.ALL_BLOCK
            ) and (
                arena[int(self.coordinate[1])][
                    int(self.coordinate[0]+0.5)
                ]
                not in bc.ALL_BLOCK
            ):
                self.coordinate[0] += 1/135 + 1/135 * self.speed
                if self.coordinate[0] >= 12.5:
                    self.coordinate[0] = 12.4999
            else:
                int(self.coordinate[0])-0.5
        else:
            self.coordinate[0] += 1/135 + 1/135 * self.speed
            if self.coordinate[0] >= 12.5:
                self.coordinate[0] = 12.4999

    def show_hitbox(
        self,
        MARGE_UP: int,
        MARGE_LEFT: int,
        RESCAL_COEF: int,
        screen: pygame.Surface,
        color: str,
    ) -> None:
        if self.heart <= 0:
            return
        pygame.draw.polygon(
            screen,
            color,
            (
                (
                    int(self.coordinate[0]) * RESCAL_COEF * 16 + MARGE_LEFT,
                    int(self.coordinate[1]) * RESCAL_COEF * 16 + MARGE_UP,
                ),
                (
                    int(self.coordinate[0]) * RESCAL_COEF * 16
                    + MARGE_LEFT
                    + 16 * RESCAL_COEF,
                    int(self.coordinate[1]) * RESCAL_COEF * 16 + MARGE_UP,
                ),
                (
                    int(self.coordinate[0]) * RESCAL_COEF * 16
                    + MARGE_LEFT
                    + 16 * RESCAL_COEF,
                    int(self.coordinate[1]) * RESCAL_COEF * 16
                    + MARGE_UP
                    + 16 * RESCAL_COEF,
                ),
                (
                    int(self.coordinate[0]) * RESCAL_COEF * 16 + MARGE_LEFT,
                    int(self.coordinate[1]) * RESCAL_COEF * 16
                    + MARGE_UP
                    + 16 * RESCAL_COEF,
                ),
            ),
            1,
        )

    def process(self, arena: list[str], date : int) -> list[str]:
        self.graphic_coords = [self.coordinate[0]-0.5, self.coordinate[1]-0.5]
        if self.heart <= 0:
            if self.frame == -1: return arena
            self.frame+=0.1
            self.animating_state = "K.O."
            self.animation()
        else:
            if self.p_frame == self.frame:
                self.frame = 0
            self.p_frame = self.frame
            self.animation()
            if self.holding[0]:
                self.holding[1].explotion_date += 1
                self.holding[1].coordinates = (self.coordinate[0], self.coordinate[1])
            if (
                arena[int(self.coordinate[1])][int(self.coordinate[0])]
                == bc.LETHAL_BLOCK
            ):
                self.heart = 0
                if self.heart <= 0:
                    self.frame = 0
            if (
                arena[int(self.coordinate[1])][int(self.coordinate[0])][0]
                in bc.EVRY_EXPLOSION_TYPE
            ):
                self.heart -= 1
                if self.heart <= 0:
                    self.frame = 0
            if (
                arena[int(self.coordinate[1])][int(self.coordinate[0])]
                in bc.ALL_ITEM_POWER_UP
            ):
                self.power_collected(
                    arena[int(self.coordinate[1])][int(self.coordinate[0])]
                )
                arena[int(self.coordinate[1])][int(self.coordinate[0])] = bc.EMPTY_CASE
        return arena

    def animation(self) -> None:
        if (
            self.frame > len(self.animation_dict[self.animating_state]) - 0.1
            and self.heart == 0
        ):
            self.frame = -1
        if self.frame > len(self.animation_dict[self.animating_state]) - 0.1:
            self.frame = 0
        self.image = self.animation_dict[self.animating_state][int(self.frame)]

    def show_player(self, MARGE_UP: int, MARGE_LEFT: int) -> None:
        if self.frame == -1:
            return
        screen.blit(
            self.image,
            (
                self.graphic_coords[0] * RESCAL_COEF * 16 + MARGE_LEFT,
                self.graphic_coords[1] * RESCAL_COEF * 16 + MARGE_UP
            ),
        )


class bomb:
    def __init__(
        self,
        radius: int,
        spike: bool,
        cord: tuple[int, int],
        born_date: int,
        owner: Player,
    ) -> None:
        self.coordinates = cord
        self.explotion_date = born_date + 60 * 5
        self.spikes = spike
        self.blast = radius
        self.owner = owner
        if self.spikes:
            self.image = SPIKEBOMB_SPRITE[0]
        else:
            self.image = BOMB_SPRITE[0]
        self.fired = False
        self.frame = 0

    def anim(self) -> None:
        self.frame += 0.1
        if self.frame > 2:
            self.frame = 0
        if self.spikes:
            self.image = SPIKEBOMB_SPRITE[int(self.frame)]
        else:
            self.image = BOMB_SPRITE[int(self.frame)]

    def verif(self, arena: list[str]) -> None:
        if self.fired:
            return
        if arena[self.coordinates[1]][self.coordinates[0]] in bc.EVRY_EXPLOSION_TYPE:
            self.fired = True

    def explose(
        self, arena: list[str], current_date: int, bombs: list["bomb"]
    ) -> tuple[list[str], bool]:
        self.verif(arena)
        if current_date < self.explotion_date and not self.fired:
            self.anim()
            return arena, False
        for b in bombs:
            if b is None:
                bombs.remove(None)
        self.coordinates = (int(self.coordinates[0]), int(self.coordinates[1]))
        if self.spikes:
            arena[self.coordinates[1]][self.coordinates[0]] = (
                bc.BLAST_CENTER_SPIKEBOMB,
                current_date,
            )
        else:
            arena[self.coordinates[1]][self.coordinates[0]] = (
                bc.BLAST_CENTER,
                current_date,
            )
        y = self.coordinates[1]
        if self.coordinates[0] != 0:
            range_left = self.coordinates[0] - self.blast
            if range_left < 0:
                range_left == 0
            max_left = None
            bomb_fired = False
            explosions = []
            for x in range(self.coordinates[0] - 1, range_left - 1, -1):
                if x <= -1:
                    break
                if arena[y][x] in (
                    bc.INDESTRUCTIBLE_BLOCK,
                    bc.LETHAL_BLOCK,
                    bc.EVRY_EXPLOSION_TYPE,
                ):
                    max_left = None
                    break
                elif arena[y][x] in bc.ALL_DESTRUCTIBLE_BLOCK:
                    if self.spikes:
                        arena[y][x] = (
                            bc.EXPLOSED_BLOCK_BY_SPIKEBOMB,
                            current_date,
                            arena[y][x],
                        )
                    else:
                        arena[y][x] = (bc.EXPLOSED_BLOCK, current_date, arena[y][x])
                        max_left = None
                elif arena[y][x] in bc.ALL_ITEM_POWER_UP:
                    max_left = None
                    explosions.append((x, y))
                    break
                else:
                    for b in bombs:
                        if b.coordinates == (x, y):
                            b.fired = True
                            max_left = None
                            bomb_fired = True
                            break
                    if bomb_fired:
                        break
                    else:
                        max_left = (x, y)
                        explosions.append((x, y))
            for e in explosions:
                if e == max_left:
                    continue
                elif self.spikes:
                    arena[e[1]][e[0]] = (bc.BLAST_LEFT_SPIKEBOMB, current_date)
                else:
                    arena[e[1]][e[0]] = (bc.BLAST_LEFT, current_date)

            if max_left != None:
                if self.spikes:
                    arena[max_left[1]][max_left[0]] = (
                        bc.BLAST_LEFTMAX_SPIKEBOMB,
                        current_date,
                    )
                else:
                    arena[max_left[1]][max_left[0]] = (bc.BLAST_LEFTMAX, current_date)

        if self.coordinates[0] != 12:
            range_right = self.blast + self.coordinates[0]
            if range_right > 12:
                range_right == 12
            max_right = None
            bomb_fired = False
            explosions = []
            for x in range(self.coordinates[0] + 1, range_right + 1):
                if arena[y][x] in (
                    bc.INDESTRUCTIBLE_BLOCK,
                    bc.LETHAL_BLOCK,
                    bc.EVRY_EXPLOSION_TYPE,
                ):
                    max_right = None
                    break
                elif arena[y][x] in bc.ALL_DESTRUCTIBLE_BLOCK:
                    if self.spikes:
                        arena[y][x] = (
                            bc.EXPLOSED_BLOCK_BY_SPIKEBOMB,
                            current_date,
                            arena[y][x],
                        )
                    else:
                        arena[y][x] = (bc.EXPLOSED_BLOCK, current_date, arena[y][x])
                        max_right = None
                elif arena[y][x] in bc.ALL_ITEM_POWER_UP:
                    max_right = None
                    explosions.append((x, y))
                    break
                else:
                    for b in bombs:
                        if b.coordinates == (x, y):
                            b.fired = True
                            max_right = None
                            bomb_fired = True
                            break
                    if bomb_fired:
                        break
                    else:
                        max_right = (x, y)
                        explosions.append((x, y))
            for e in explosions:
                if e == max_right:
                    continue
                elif self.spikes:
                    arena[e[1]][e[0]] = (bc.BLAST_RIGHT_SPIKEBOMB, current_date)
                else:
                    arena[e[1]][e[0]] = (bc.BLAST_RIGHT, current_date)

            if max_right != None:
                if self.spikes:
                    arena[max_right[1]][max_right[0]] = (
                        bc.BLAST_RIGHTMAX_SPIKEBOMB,
                        current_date,
                    )
                else:
                    arena[max_right[1]][max_right[0]] = (
                        bc.BLAST_RIGHTMAX,
                        current_date,
                    )

        x = self.coordinates[0]
        if self.coordinates[1] != 0:
            range_up = self.coordinates[1] - self.blast
            if range_up < 0:
                range_up == 0
            max_up = None
            bomb_fired = False
            explosions = []
            for y in range(self.coordinates[1] - 1, range_up - 1, -1):
                if y <= -1:
                    break
                if arena[y][x] in (
                    bc.INDESTRUCTIBLE_BLOCK,
                    bc.LETHAL_BLOCK,
                    bc.EVRY_EXPLOSION_TYPE,
                ):
                    max_up = None
                    break
                elif arena[y][x] in bc.ALL_DESTRUCTIBLE_BLOCK:
                    if self.spikes:
                        arena[y][x] = (
                            bc.EXPLOSED_BLOCK_BY_SPIKEBOMB,
                            current_date,
                            arena[y][x],
                        )
                    else:
                        arena[y][x] = (bc.EXPLOSED_BLOCK, current_date, arena[y][x])
                        max_up = None
                elif arena[y][x] in bc.ALL_ITEM_POWER_UP:
                    max_up = None
                    explosions.append((x, y))
                    break
                else:
                    for b in bombs:
                        if b.coordinates == (x, y):
                            b.fired = True
                            max_up = None
                            bomb_fired = True
                            break
                    if bomb_fired:
                        break
                    else:
                        max_up = (x, y)
                        explosions.append((x, y))
            for e in explosions:
                if e == max_up:
                    continue
                elif self.spikes:
                    arena[e[1]][e[0]] = (bc.BLAST_UP_SPIKEBOMB, current_date)
                else:
                    arena[e[1]][e[0]] = (bc.BLAST_UP, current_date)

            if max_up != None:
                if self.spikes:
                    arena[max_up[1]][max_up[0]] = (
                        bc.BLAST_UPMAX_SPIKEBOMB,
                        current_date,
                    )
                else:
                    arena[max_up[1]][max_up[0]] = (bc.BLAST_UPMAX, current_date)

        if self.coordinates[1] != 8:
            range_down = self.blast + self.coordinates[1]
            if range_down > 8:
                range_down == 8
            max_down = None
            bomb_fired = False
            explosions = []
            for y in range(self.coordinates[1] + 1, range_down + 1):
                try:
                    if arena[y][x] in (
                        bc.INDESTRUCTIBLE_BLOCK,
                        bc.LETHAL_BLOCK,
                        bc.EVRY_EXPLOSION_TYPE,
                    ):
                        max_down = None
                        break
                    elif arena[y][x] in bc.ALL_DESTRUCTIBLE_BLOCK:
                        if self.spikes:
                            arena[y][x] = (
                                bc.EXPLOSED_BLOCK_BY_SPIKEBOMB,
                                current_date,
                                arena[y][x],
                            )
                        else:
                            arena[y][x] = (bc.EXPLOSED_BLOCK, current_date, arena[y][x])
                            max_down = None
                    elif arena[y][x] in bc.ALL_ITEM_POWER_UP:
                        max_down = None
                        explosions.append((x, y))
                        break
                    else:
                        for b in bombs:
                            if b.coordinates == (x, y):
                                b.fired = True
                                max_down = None
                                bomb_fired = True
                                break
                        if bomb_fired:
                            break
                        else:
                            max_down = (x, y)
                            explosions.append((x, y))
                except IndexError:
                    break
            for e in explosions:
                if e == max_down:
                    continue
                elif self.spikes:
                    arena[e[1]][e[0]] = (bc.BLAST_DOWN_SPIKEBOMB, current_date)
                else:
                    arena[e[1]][e[0]] = (bc.BLAST_DOWN, current_date)

            if max_down != None:
                if self.spikes:
                    arena[max_down[1]][max_down[0]] = (
                        bc.BLAST_DOWNMAX_SPIKEBOMB,
                        current_date,
                    )
                else:
                    arena[max_down[1]][max_down[0]] = (bc.BLAST_DOWNMAX, current_date)

        self.owner.placed_bombs -= 1
        return arena, True


# init
pygame.init()
pygame.joystick.init()
pygame.mixer.init()

# contollers setup
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
controls_maps = []
for i in joysticks:
    i.init()
    if i.get_name() == "PS4 Controller" or i.get_numhats() == 0:
        controls_maps.append(bc.CONTROL_MAP_PS)
    else:
        controls_maps.append(bc.CONTROL_MAP_XBX)

pygame.mixer.music.load(bc.MENU_MUSIC_START)
pygame.mixer.music.play()
pygame.mixer.music.queue(bc.MENU_MUSIC_LOOP, loops=-1)

# window config and other
if bc.DEBUG_FULLSCREEN:
    pgdi = pygame.display.Info()
    width = pgdi.current_w
    height = pgdi.current_h
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    width = 1000
    height = 650
    screen = pygame.display.set_mode((width, height))
# pour les pc du lycée
RESCAL_COEF = round(min(width / 239, height / 160))
if width == 1280 and height == 720:
    # pour les pc full HD
    RESCAL_COEF = min(width / 239, height / 160)
ARENA_MARGING = (width - 239 * RESCAL_COEF) / 2

# font
font2 = pygame.font.SysFont("Arial", 18)
myfont = pygame.font.SysFont("Arial", 28)
Hurryfont = pygame.font.SysFont("Arial Black", 48, True)

# icon and caption
ico = pygame.image.load("./graphisme/bomberman.png").convert_alpha()
pygame.display.set_icon(ico)
pygame.display.set_caption("Bomberman")

# IMG

BLAST_IMG_DIC: dict[str, list[pygame.Surface]]
BLAST_IMG_DIC = {
    bc.EXPLOSED_BLOCK: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSED_BLOCK_PATH
    ],
    bc.BLAST_CENTER: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_CENTER
    ],
    bc.BLAST_LEFT: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_LEFT
    ],
    bc.BLAST_RIGHT: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_RIGHT
    ],
    bc.BLAST_UP: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_UP
    ],
    bc.BLAST_DOWN: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_DOWN
    ],
    bc.BLAST_LEFTMAX: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_LEFT_MAX
    ],
    bc.BLAST_RIGHTMAX: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_RIGHT_MAX
    ],
    bc.BLAST_UPMAX: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_UP
    ],
    bc.BLAST_DOWNMAX: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_DOWN_MAX
    ],
    bc.EXPLOSED_BLOCK_BY_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSED_BLOCK_PATH_BLUE
    ],
    bc.BLAST_CENTER_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_CENTER_BLUE
    ],
    bc.BLAST_LEFT_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_LEFT_BLUE
    ],
    bc.BLAST_RIGHT_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_RIGHT_BLUE
    ],
    bc.BLAST_UP_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_UP_BLUE
    ],
    bc.BLAST_DOWN_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_DOWN_BLUE
    ],
    bc.BLAST_LEFTMAX_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_LEFT_MAX_BLUE
    ],
    bc.BLAST_RIGHTMAX_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_RIGHT_MAX_BLUE
    ],
    bc.BLAST_UPMAX_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_UP_MAX_BLUE
    ],
    bc.BLAST_DOWNMAX_SPIKEBOMB: [
        pygame.transform.scale(
            pygame.image.load(img),
            (
                16 * RESCAL_COEF,
                16 * RESCAL_COEF,
            ),
        )
        for img in bc.EXPLOSION_DOWN_MAX_BLUE
    ],
}
POWER_UP_DIC = {
    bc.BLAST_PLUS: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_BLAST_PLUS),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.BLAST_MINUS: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_BLAST_MINUS),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.BOMB_PLUS: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_BOMB_PLUS),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.BOMB_MINUS: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_BOMB_MINUS),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.SPEED_PLUS: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_SPEED_PLUS),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.SPEED_MINUS: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_SPEED_MINUS),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.POWER_GLOVE_ITEM: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_POWER_GLOVE),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.KICK_ITEM: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_KICK),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.FOOTKICK_ITEM: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_FOOTKICK),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.HEART_ITEM: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_HEART),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.SPIKE_BOMB_ITEM: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_SPIKE_BOMB),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.SKULL_DISEAS: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_SKULL_DISEAS),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
    bc.MAX_BOMB_POWER: pygame.transform.scale(
        pygame.image.load(bc.ONFLOOR_MAX_BOMB_POWER),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),
    ),
}

BOMB_SPRITE = [
    pygame.transform.scale(
        pygame.image.load(f'./graphisme/bomb & blast/bomb/sprite_{i}.png'),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),) for i in range(3)
]
SPIKEBOMB_SPRITE = [
    pygame.transform.scale(
        pygame.image.load(f'./graphisme/bomb & blast/bomb/sprite_{i}.png'),
        (
            14 * RESCAL_COEF,
            14 * RESCAL_COEF,
        ),) for i in range(3, 6)
]


spiral_number = 0
step = -1
side = "L"


def lethal_block_fall(arena: list[str]) -> list[str]:
    global spiral_number, step, side
    step += 1
    if side == "L":
        arena[8 - (step + spiral_number)][0 + spiral_number] = bc.LETHAL_BLOCK
        if step == 8 - spiral_number * 2:
            step = -1
            side = "U"
    elif side == "U":
        arena[0 + spiral_number][1 + spiral_number + step] = bc.LETHAL_BLOCK
        if step == 11 - spiral_number * 2:
            step = -1
            side = "R"
    elif side == "R":
        arena[1 + spiral_number + step][12 - spiral_number] = bc.LETHAL_BLOCK
        if step == 7 - spiral_number * 2:
            step = -1
            side = "D"
    elif side == "D":
        arena[8 - spiral_number][11 - (step + spiral_number)] = bc.LETHAL_BLOCK
        if step == 10 - spiral_number * 2:
            step = -1
            spiral_number += 1
            side = "L"
    return arena


def arena_build() -> list[str]:
    arena = bc.arena_temp()
    for i in range(9):
        for y in range(13):
            if arena[i][y] == bc.EMPTY_DESTRUCTIBLE:
                if random.uniform(0.00, 1.00) < 1 / 3:
                    if random.uniform(0.00, 1.00) < 0.075:
                        a = bc.BLOCK_HEART
                    else:
                        a = random.choice(bc.POWER_UP_BLOCKS)
                    arena[i][y] = a
    return arena


def controller_refresh(useless) -> None:
    global joysticks
    global controls_maps
    joysticks = [
        pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
    ]
    temp = [controls_maps, -1]
    controls_maps = []
    for i in joysticks:
        temp[1] += 1
        i.init()
        if len(temp[0]) >= temp[1] + 1:
            controls_maps.append(temp[0][temp[1]])
        elif i.get_name() == "PS4 Controller" or i.get_numhats() == 0:
            controls_maps.append(bc.CONTROL_MAP_PS)
        else:
            controls_maps.append(bc.CONTROL_MAP_XBX)
    M = 20
    for i in joysticks:
        f = pygame.image.load(f"./graphisme/controller_battery/{i.get_power_level()} battery.png")
        screen.blit(f, (0, M))
        M += 20


def start_the_game() -> None:
    pygame.mixer.music.pause()
    pygame.mixer.music.unload()
    global controls_maps
    menu.close()
    pygame.key.set_repeat(16)
    wait_screen = pygame.image.load("./graphisme/waiting_screen.png")
    wait_screen = pygame.transform.scale(wait_screen, (width, height))
    J_index = 0
    tempT = 0
    label = myfont.render("Aucune manette connecté !", 1, (255, 0, 0))
    Stime = time()
    joysticks = [
        pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
    ]
    temp = [controls_maps, -1]
    controls_maps = []
    for i in joysticks:
        temp[1] += 1
        i.init()
        if len(temp[0]) >= temp[1] + 1:
            controls_maps.append(temp[0][temp[1]])
        elif i.get_name() == "PS4 Controller" or i.get_numhats() == 0:
            controls_maps.append(bc.CONTROL_MAP_PS)
        else:
            controls_maps.append(bc.CONTROL_MAP_XBX)
    for i in joysticks:
        i.init()
    while time() <= Stime + 10:
        screen.blit(wait_screen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if len(joysticks) >= J_index + 1 and 5 != J_index + 1 and time() >= tempT + 2.5:
            tempT = time()
            joystick = joysticks[J_index]
            joystick.rumble(0.25, 0.25, 250)
            label = myfont.render(
                f"Player {J_index+1} your controller should be rumbeling",
                1,
                (255, 0, 0),
            )
            J_index += 1
        elif time() >= tempT + 2.5:
            label = myfont.render("pas d'autre manette connecté", 1, (255, 0, 0))
        screen.blit(label, (width / 2 - label.get_size()[0] / 2, height / 2))
        pygame.display.flip()

    player1 = Player(0.5, 0.5)
    # player2 = Player(0, 0)
    player2 = Player(12.4999, 0.5)
    player3 = Player(0.5, 8.4999)
    player4 = Player(12.4999, 8.4999)
    bombs: list[bomb]
    bombs = []
    IMAGE_DESTRUCTIBLE_BLOCKS = pygame.image.load(bc.PATH_DESTRUCTIBLE_BLOCKS)
    IMAGE_DESTRUCTIBLE_BLOCKS = pygame.transform.scale(
        IMAGE_DESTRUCTIBLE_BLOCKS,
        (
            16 * RESCAL_COEF,
            16 * RESCAL_COEF,
        ),
    )
    IMAGE_LETHAL_BLOCKS = pygame.image.load(bc.PATH_LETHAL_BLOCKS)
    IMAGE_LETHAL_BLOCKS = pygame.transform.scale(
        IMAGE_LETHAL_BLOCKS,
        (
            16 * RESCAL_COEF,
            16 * RESCAL_COEF,
        ),
    )
    MARGE_UP = RESCAL_COEF * 8
    MARGE_LEFT = RESCAL_COEF * 16 + ARENA_MARGING
    ingame = True
    arena = arena_build()
    ARENA_BG = pygame.image.load(bc.PATH_ARENA_BG)
    ARENA_BG = pygame.transform.scale(
        ARENA_BG,
        (ARENA_BG.get_width() * RESCAL_COEF, ARENA_BG.get_height() * RESCAL_COEF),
    )

    clock = pygame.time.Clock()
    TickTime = 0
    pygame.draw.polygon(
        screen, "darkgray", ((0, 0), (width, 0), (width, height), (0, height))
    )
    show_order = 0
    alive_players = 4
    p1dead = False
    p2dead = False
    p3dead = False
    p4dead = False
    anti_hold_k_A = (False, 0)
    anti_hold_k_I = (False, 0)
    anti_hold_k_H = (False, 0)
    anti_hold_k_PAGEDOWN = (False, 0)
    pygame.mixer.Sound.play(bc.VOICE_READY)
    screen.blit(ARENA_BG, (ARENA_MARGING, 0))

    for y in range(9):
        for x in range(13):
            if arena[y][x] in bc.ALL_DESTRUCTIBLE_BLOCK:
                screen.blit(
                    IMAGE_DESTRUCTIBLE_BLOCKS,
                    (
                        x * 16 * RESCAL_COEF + MARGE_LEFT,
                        y * 16 * RESCAL_COEF + MARGE_UP,
                    ),
                )
            elif arena[y][x] in (bc.INDESTRUCTIBLE_BLOCK, bc.EMPTY_CASE):
                pass
            elif arena[y][x] == bc.LETHAL_BLOCK:
                screen.blit(
                    IMAGE_LETHAL_BLOCKS,
                    (
                        x * 16 * RESCAL_COEF + MARGE_LEFT,
                        y * 16 * RESCAL_COEF + MARGE_UP,
                    ),
                )
            elif arena[y][x] in bc.ALL_ITEM_POWER_UP:
                screen.blit(
                    POWER_UP_DIC[arena[y][x]],
                    (
                        x * 16 * RESCAL_COEF + MARGE_LEFT,
                        y * 16 * RESCAL_COEF + MARGE_UP,
                    ),
                )
            elif arena[y][x][0] in bc.EVRY_EXPLOSION_TYPE:
                if arena[y][x][1] + 60 == TickTime:
                    try:
                        arena[y][x] = bc.BLOCK_TO_POWER_UP[arena[y][x][2]]
                    except KeyError:
                        arena[y][x] = bc.EMPTY_CASE
                    except IndexError:
                        arena[y][x] = bc.EMPTY_CASE
                else:
                    screen.blit(
                        BLAST_IMG_DIC[arena[y][x][0]][
                            (arena[y][x][1] - TickTime) // 15
                        ],
                        (
                            x * 16 * RESCAL_COEF + MARGE_LEFT,
                            y * 16 * RESCAL_COEF + MARGE_UP,
                        ),
                    )

    # "hitbox"
    if bc.DEBUG_SHOW_BOMBER_PLACEMENT:
        show_order += 1
        if show_order <= 10:
            player1.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "white")
            player2.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "black")
            player3.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "red")
            player4.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "blue")
        if show_order <= 20 and show_order > 10:
            player2.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "black")
            player3.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "red")
            player4.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "blue")
            player1.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "white")
        if show_order <= 30 and show_order > 20:
            player3.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "red")
            player4.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "blue")
            player1.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "white")
            player2.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "black")
        if show_order <= 40 and show_order > 30:
            player4.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "blue")
            player1.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "white")
            player2.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "black")
            player3.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "red")
        if show_order == 40:
            show_order = 0

    player1.show_player(MARGE_UP, MARGE_LEFT)
    player2.show_player(MARGE_UP, MARGE_LEFT)
    player3.show_player(MARGE_UP, MARGE_LEFT)
    player4.show_player(MARGE_UP, MARGE_LEFT)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.mixer.Sound.play(bc.VOICE_GO)
    pygame.mixer.music.load(bc.BATTLE_MUSIC[music_selected])
    pygame.mixer.music.play()
    while ingame:
        clock.tick(60)
        TickTime += 1
        screen.blit(ARENA_BG, (ARENA_MARGING, 0))
        arena = player1.process(arena, TickTime)
        arena = player2.process(arena, TickTime)
        arena = player3.process(arena, TickTime)
        arena = player4.process(arena, TickTime)
        if player1.heart == 0 and not p1dead:
            alive_players -= 1
            p1dead = True
        if player2.heart == 0 and not p2dead:
            alive_players -= 1
            p2dead = True
        if player3.heart == 0 and not p3dead:
            alive_players -= 1
            p3dead = True
        if player4.heart == 0 and not p4dead:
            alive_players -= 1
            p4dead = True
        if alive_players <= 1:
            if p1dead and player1.frame != -1:
                pass
            elif p2dead and player2.frame != -1:
                pass
            elif p3dead and player3.frame != -1:
                pass
            elif p4dead and player4.frame != -1:
                pass
            else:
                ingame = False
        M = 30
        for event in pygame.event.get():
            if event.type not in (
                pygame.QUIT,
                pygame.KEYDOWN,
                pygame.JOYBUTTONDOWN,
            ):
                continue
            # aucun événement devrait (théoriquement) se retrouver ici sauf les événement lié au JOY
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                try:
                    if (
                        event.button == controls_maps[0]["B"]
                        and event.instance_id == 0
                        and player1.heart > 0
                    ):
                        bombs.append(player1.place_bomb(TickTime, bombs))
                    elif (
                        event.button == controls_maps[1]["B"]
                        and event.instance_id == 1
                        and player2.heart > 0
                    ):
                        bombs.append(player2.place_bomb(TickTime, bombs))
                    elif (
                        event.button == controls_maps[2]["B"]
                        and event.instance_id == 2
                        and player3.heart > 0
                    ):
                        bombs.append(player3.place_bomb(TickTime, bombs))
                    elif (
                        event.button == controls_maps[3]["B"]
                        and event.instance_id == 3
                        and player4.heart > 0
                    ):
                        bombs.append(player4.place_bomb(TickTime, bombs))
                except IndexError:
                    pass
            if event.type == pygame.KEYDOWN:
                if pygame.joystick.get_count() <= 0 and player1.heart > 0:
                    if event.key == pygame.K_z:
                        player1.walk_up(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_s:
                        player1.walk_down(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_q:
                        player1.walk_left(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_d:
                        player1.walk_right(arena, bombs, TickTime)
                        continue

                    if event.key == pygame.K_a and not anti_hold_k_A[0]:
                        bombs.append(player1.place_bomb(TickTime, bombs))
                    if event.key == pygame.K_a:
                        anti_hold_k_A = (True, TickTime)

                if pygame.joystick.get_count() <= 1 and player2.heart > 0:
                    if event.key == pygame.K_o:
                        player2.walk_up(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_l:
                        player2.walk_down(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_k:
                        player2.walk_left(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_m:
                        player2.walk_right(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_i and not anti_hold_k_I[0]:
                        bombs.append(player2.place_bomb(TickTime, bombs))
                    if event.key == pygame.K_i:
                        anti_hold_k_I = (True, TickTime)

                if pygame.joystick.get_count() <= 2 and player3.heart > 0:
                    if event.key == pygame.K_g:
                        player3.walk_up(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_b:
                        player3.walk_down(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_v:
                        player3.walk_left(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_n:
                        player3.walk_right(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_h and not anti_hold_k_H[0]:
                        bombs.append(player3.place_bomb(TickTime, bombs))
                    if event.key == pygame.K_h:
                        anti_hold_k_H = (True, TickTime)

                if pygame.joystick.get_count() <= 3 and player4.heart > 0:
                    if event.key == pygame.K_UP:
                        player4.walk_up(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_DOWN:
                        player4.walk_down(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_LEFT:
                        player4.walk_left(arena, bombs, TickTime)
                        continue
                    if event.key == pygame.K_RIGHT:
                        player4.walk_right(arena, bombs, TickTime)
                    if event.key == pygame.K_PAGEDOWN and not anti_hold_k_PAGEDOWN[0]:
                        bombs.append(player4.place_bomb(TickTime, bombs))
                    if event.key == pygame.K_PAGEDOWN:
                        anti_hold_k_PAGEDOWN = (True, TickTime)

        if pygame.joystick.get_count() >= 1 and player1.heart > 0:
            if controls_maps[0]["HAT"]:
                if joysticks[0].get_hat(0)[1] == 1:
                    player1.walk_up(arena, bombs, TickTime)
                if joysticks[0].get_hat(0)[1] == -1:
                    player1.walk_down(arena, bombs, TickTime)
                if joysticks[0].get_hat(0)[0] == -1:
                    player1.walk_left(arena, bombs, TickTime)
                if joysticks[0].get_hat(0)[0] == 1:
                    player1.walk_right(arena, bombs, TickTime)

            if not controls_maps[0]["HAT"]:
                if joysticks[0].get_button(controls_maps[0]["D-PAD UP"]):
                    player1.walk_up(arena, bombs, TickTime)
                if joysticks[0].get_button(controls_maps[0]["D-PAD DOWN"]):
                    player1.walk_down(arena, bombs, TickTime)
                if joysticks[0].get_button(controls_maps[0]["D-PAD LEFT"]):
                    player1.walk_left(arena, bombs, TickTime)
                if joysticks[0].get_button(controls_maps[0]["D-PAD RIGHT"]):
                    player1.walk_right(arena, bombs, TickTime)

        if pygame.joystick.get_count() >= 2 and player2.heart > 0:
            if controls_maps[1]["HAT"]:
                if joysticks[1].get_hat(0)[1] == 1:
                    player2.walk_up(arena, bombs, TickTime)
                if joysticks[1].get_hat(0)[1] == -1:
                    player2.walk_down(arena, bombs, TickTime)
                if joysticks[1].get_hat(0)[0] == -1:
                    player2.walk_left(arena, bombs, TickTime)
                if joysticks[1].get_hat(0)[0] == 1:
                    player2.walk_right(arena, bombs, TickTime)

            if not controls_maps[1]["HAT"]:
                if joysticks[1].get_button(controls_maps[1]["D-PAD UP"]):
                    player2.walk_up(arena, bombs, TickTime)
                if joysticks[1].get_button(controls_maps[1]["D-PAD DOWN"]):
                    player2.walk_down(arena, bombs, TickTime)
                if joysticks[1].get_button(controls_maps[1]["D-PAD LEFT"]):
                    player2.walk_left(arena, bombs, TickTime)
                if joysticks[1].get_button(controls_maps[1]["D-PAD RIGHT"]):
                    player2.walk_right(arena, bombs, TickTime)

        if pygame.joystick.get_count() >= 3 and player3.heart > 0:
            if controls_maps[2]["HAT"]:
                if joysticks[2].get_hat(0)[1] == 1:
                    player3.walk_up(arena, bombs, TickTime)
                if joysticks[2].get_hat(0)[1] == -1:
                    player3.walk_down(arena, bombs, TickTime)
                if joysticks[2].get_hat(0)[0] == -1:
                    player3.walk_left(arena, bombs, TickTime)
                if joysticks[2].get_hat(0)[0] == 1:
                    player3.walk_right(arena, bombs, TickTime)

            if not controls_maps[2]["HAT"]:
                if joysticks[2].get_button(controls_maps[2]["D-PAD UP"]):
                    player3.walk_up(arena, bombs, TickTime)
                if joysticks[2].get_button(controls_maps[2]["D-PAD DOWN"]):
                    player3.walk_down(arena, bombs, TickTime)
                if joysticks[2].get_button(controls_maps[2]["D-PAD LEFT"]):
                    player3.walk_left(arena, bombs, TickTime)
                if joysticks[2].get_button(controls_maps[2]["D-PAD RIGHT"]):
                    player3.walk_right(arena, bombs, TickTime)

        if pygame.joystick.get_count() >= 4 and player4.heart > 0:
            if controls_maps[3]["HAT"]:
                if joysticks[3].get_hat(0)[1] == 1:
                    player4.walk_up(arena, bombs, TickTime)
                if joysticks[3].get_hat(0)[1] == -1:
                    player4.walk_down(arena, bombs, TickTime)
                if joysticks[3].get_hat(0)[0] == -1:
                    player4.walk_left(arena, bombs, TickTime)
                if joysticks[3].get_hat(0)[0] == 1:
                    player4.walk_right(arena, bombs, TickTime)

            if not controls_maps[3]["HAT"]:
                if joysticks[3].get_button(controls_maps[3]["D-PAD UP"]):
                    player4.walk_up(arena, bombs, TickTime)
                if joysticks[3].get_button(controls_maps[3]["D-PAD DOWN"]):
                    player4.walk_down(arena, bombs, TickTime)
                if joysticks[3].get_button(controls_maps[3]["D-PAD LEFT"]):
                    player4.walk_left(arena, bombs, TickTime)
                if joysticks[3].get_button(controls_maps[3]["D-PAD RIGHT"]):
                    player4.walk_right(arena, bombs, TickTime)
        if anti_hold_k_A[1] != TickTime:
            anti_hold_k_A = (False, 0)
        if anti_hold_k_H[1] != TickTime:
            anti_hold_k_H = (False, 0)
        if anti_hold_k_I[1] != TickTime:
            anti_hold_k_I = (False, 0)
        if anti_hold_k_PAGEDOWN[1] != TickTime:
            anti_hold_k_PAGEDOWN = (False, 0)

        index_to_remove = []
        for b in range(len(bombs)):
            if bombs[b] is None:
                index_to_remove.append(b)
                continue
            if arena[bombs[b].coordinates[1]][bombs[b].coordinates[0]] == bc.LETHAL_BLOCK:
                bombs[b].owner.placed_bombs -= 1
                index_to_remove.append(b)
                continue
            arena, resu = bombs[b].explose(arena, TickTime, bombs)
            if resu:
                index_to_remove.append(b)
                continue
            else:
                screen.blit(
                    bombs[b].image,
                    (
                        (bombs[b].coordinates[0] * 16 +1)* RESCAL_COEF + MARGE_LEFT,
                        (bombs[b].coordinates[1] * 16 +1)* RESCAL_COEF + MARGE_UP,
                    ),
                )
        for b in index_to_remove:
            bombs.pop(b)

        for y in range(9):
            for x in range(13):
                if arena[y][x] in bc.ALL_DESTRUCTIBLE_BLOCK:
                    screen.blit(
                        IMAGE_DESTRUCTIBLE_BLOCKS,
                        (
                            x * 16 * RESCAL_COEF + MARGE_LEFT,
                            y * 16 * RESCAL_COEF + MARGE_UP,
                        ),
                    )
                elif arena[y][x] in (bc.INDESTRUCTIBLE_BLOCK, bc.EMPTY_CASE):
                    pass
                elif arena[y][x] == bc.LETHAL_BLOCK:
                    screen.blit(
                        IMAGE_LETHAL_BLOCKS,
                        (
                            x * 16 * RESCAL_COEF + MARGE_LEFT,
                            y * 16 * RESCAL_COEF + MARGE_UP,
                        ),
                    )
                elif arena[y][x] in bc.ALL_ITEM_POWER_UP:
                    screen.blit(
                        POWER_UP_DIC[arena[y][x]],
                        (
                            (x * 16 +1)* RESCAL_COEF + MARGE_LEFT,
                            (y * 16 +1)* RESCAL_COEF + MARGE_UP,
                        ),
                    )
                elif arena[y][x][0] in bc.EVRY_EXPLOSION_TYPE:
                    if arena[y][x][1] + 60 == TickTime:
                        try:
                            arena[y][x] = bc.BLOCK_TO_POWER_UP[arena[y][x][2]]
                        except KeyError:
                            arena[y][x] = bc.EMPTY_CASE
                        except IndexError:
                            arena[y][x] = bc.EMPTY_CASE
                    else:
                        screen.blit(
                            BLAST_IMG_DIC[arena[y][x][0]][
                                (arena[y][x][1] - TickTime) // 15
                            ],
                            (
                                x * 16 * RESCAL_COEF + MARGE_LEFT,
                                y * 16 * RESCAL_COEF + MARGE_UP,
                            ),
                        )

        # "hitbox"
        if bc.DEBUG_SHOW_BOMBER_PLACEMENT:
            show_order += 1
            if show_order <= 10:
                player1.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "white")
                player2.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "black")
                player3.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "red")
                player4.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "blue")
            if show_order <= 20 and show_order > 10:
                player2.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "black")
                player3.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "red")
                player4.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "blue")
                player1.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "white")
            if show_order <= 30 and show_order > 20:
                player3.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "red")
                player4.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "blue")
                player1.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "white")
                player2.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "black")
            if show_order <= 40 and show_order > 30:
                player4.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "blue")
                player1.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "white")
                player2.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "black")
                player3.show_hitbox(MARGE_UP, MARGE_LEFT, RESCAL_COEF, screen, "red")
            if show_order == 40:
                show_order = 0

        player1.show_player(MARGE_UP, MARGE_LEFT)
        player2.show_player(MARGE_UP, MARGE_LEFT)
        player3.show_player(MARGE_UP, MARGE_LEFT)
        player4.show_player(MARGE_UP, MARGE_LEFT)

        if TickTime == 7200 and not bc.DEBUG_FAST_HURRY:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            HurryUp_str = Hurryfont.render("Hurry Up !", 1, (255, 0, 0))
            pygame.mixer.Sound.play(bc.VOICE_HURRY_UP)

        if TickTime >= 7200 and TickTime <= 7250 and not bc.DEBUG_FAST_HURRY:
            screen.blit(
                HurryUp_str,
                (
                    width / 2 - HurryUp_str.get_size()[0] / 2,
                    height / 2 - HurryUp_str.get_size()[1] / 2,
                ),
            )

        if TickTime == 7250 and not bc.DEBUG_FAST_HURRY:
            pygame.mixer.music.load(bc.BATTLE_MUSIC_HURY_UP[music_selected])
            pygame.mixer.music.play()

        if TickTime >= 7290 and not bc.DEBUG_FAST_HURRY:
            if TickTime % 30 == 0:
                arena = lethal_block_fall(arena)

        if TickTime == 300 and bc.DEBUG_FAST_HURRY:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            HurryUp_str = Hurryfont.render("Hurry Up !", 1, (255, 0, 0))
            pygame.mixer.Sound.play(bc.VOICE_HURRY_UP)

        if TickTime >= 300 and TickTime <= 350 and bc.DEBUG_FAST_HURRY:
            screen.blit(
                HurryUp_str,
                (
                    width / 2 - HurryUp_str.get_size()[0] / 2,
                    height / 2 - HurryUp_str.get_size()[1] / 2,
                ),
            )

        if TickTime == 350 and bc.DEBUG_FAST_HURRY:
            pygame.mixer.music.load(bc.BATTLE_MUSIC_HURY_UP[music_selected])
            pygame.mixer.music.play()

        if TickTime >= 390 and bc.DEBUG_FAST_HURRY:
            if TickTime % 30 == 0:
                arena = lethal_block_fall(arena)

        pygame.display.flip()
    pygame.time.delay(500)
    if alive_players == 0:
        End_str = Hurryfont.render("DRAW !", 1, (255, 0, 0))
        pygame.mixer.Sound.play(bc.VOICE_DRAW)
    else:
        if not p1dead:
            End_str = Hurryfont.render("Player 1 WIN !", 1, (0, 0, 0))
        if not p2dead:
            End_str = Hurryfont.render("Player 2 WIN !", 1, (0, 0, 0))
        if not p3dead:
            End_str = Hurryfont.render("Player 3 WIN !", 1, (0, 0, 0))
        if not p4dead:
            End_str = Hurryfont.render("Player 4 WIN !", 1, (0, 0, 0))

    screen.blit(
        End_str,
        (
            width / 2 - End_str.get_size()[0] / 2,
            height / 2 - End_str.get_size()[1] / 2,
        ),
    )
    T = 0
    global spiral_number, step, side
    spiral_number = 0
    step = -1
    side = "L"
    while True:
        T += 1
        pygame.display.flip()
        if T == 600:
            break
    pygame.mixer.music.stop()
    pygame.mixer.music.load(bc.MENU_MUSIC_START)
    pygame.mixer.music.play()
    pygame.mixer.music.queue(bc.MENU_MUSIC_LOOP, loops=-1)
    menu.enable()


music_selected = 0


def dbg() -> None:
    dddd = True
    pygame.draw.polygon(
        screen, (128, 128, 128), ((0, 0), (width, 0), (width, height), (0, height))
    )
    while dddd:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dddd = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(BLAST_IMG_DIC[bc.BLAST_LEFT][0], (width / 2, height / 2))
        pygame.display.flip()


def change_music(Music: tuple[str, int], *args) -> None:
    global music_selected
    Music_display_name._title = bc.MUSIC_NAME_LIST[Music[1]]
    music_selected = Music[1]


def controller_config_screen(text: str) -> None:
    pygame.draw.polygon(
        screen, (128, 128, 128), ((0, 0), (width, 0), (width, height), (0, height))
    )
    label2 = myfont.render(text, 1, (255, 255, 255))
    screen.blit(label2, (width / 2 - label2.get_size()[0] / 2, height / 2))
    pygame.display.flip()


def controller_config() -> None:
    global controls_maps
    controller_config_screen("press any button of the controller to remap it")
    cust_map = {}
    list_btn = [
        "A",
        "B",
        "X",
        "Y",
        "LB",
        "RB",
        "Start",
        "D-PAD UP",
        "D-PAD DOWN",
        "D-PAD LEFT",
        "D-PAD RIGHT",
    ]
    t = 0
    remaping = True
    while remaping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION:
                remap_joy = event.joy
                remaping = False
                joysticks[remap_joy].rumble(0.25, 0.25, 250)
    if joysticks[remap_joy].get_numhats() == 0:
        cust_map.update({"HAT", False})
    remaping = True
    while remaping:
        if list_btn[t] == "D-PAD UP" and joysticks[remap_joy].get_numhats() >= 1:
            cust_map.update({"HAT": True})
            break
        if t >= len(list_btn):
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION:
                if remap_joy == event.joy:
                    t += 1
                    cust_map.update({list_btn[t]: event.button})
        controller_config_screen(f"press {list_btn[t]}")
    controls_maps[remap_joy] = cust_map


menu = pygame_menu.Menu(
    "Bomberman", width, height, theme=pygame_menu.themes.THEME_BLUE, columns=2, rows=7
)

menu.add.button("Play", start_the_game)

Music_display_name = menu.add.label("Music :")
selct_music = menu.add.selector(
    title="",
    items=[" "] * len(bc.MUSIC_NAME_LIST),
    onchange=change_music,
)
Music_display_name = menu.add.label(bc.MUSIC_NAME_LIST[0])
img = menu.add.image("./jacket/Bomberman (DS) [JP_cover].jpg")
menu.add.button("control mapping", controller_config)
menu.add.button("Quit", pygame_menu.events.EXIT)
# menu.add.button("dbg", dbg)

menu.mainloop(screen, controller_refresh)
