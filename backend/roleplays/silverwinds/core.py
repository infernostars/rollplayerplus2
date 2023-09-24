import random


class Resource:
    def __init__(self, name: str, count: int, harvest_level: int, durability: int):
        self.name = name
        self.count = count


class Ore:
    def __init__(self, name: str, resource: Resource, depth_min: int, depth_max: int, rarity: int, pick_level: int,
                 no_ore: bool = False):
        if no_ore:
            self.name = resource.name
        else:
            self.name = name
        self.resource = resource
        self.depth_min = depth_min
        self.depth_max = depth_max
        self.rarity = rarity
        self.pick_level = pick_level

    def __str__(self):
        if self.name == self.resource.name:
            return f"x{self.resource.count} - {self.name}"
        else:
            return f"x{self.resource.count} - {self.name} ({self.resource.name})"

    def mine(self, depth, pick_level):
        if self.depth_min >= depth >= self.depth_max and self.pick_level <= pick_level:
            if random.randint(1, self.rarity) == 1:
                return self
            else:
                return 0
        else:
            return 0


ore_list = [
    Ore('Clay Ore', Resource('Clay', 1, 0, 0), 5, -20, 4, 0, True),
    Ore('Stone Ore', Resource('Stone', 1, 2, 100), 256, -512, 1, 1, True),
    Ore('Coal Ore', Resource('Coal', 1, 0, 0), 256, -120, 1, 1, True),
    Ore('Tin Ore', Resource('Tin', 1, 3, 100), 256, -512, 3, 2),
    Ore('Copper Ore', Resource('Copper', 1, 4, 200), 200, -100, 3, 3),
    Ore('Iron Ore', Resource('Iron', 1, 5, 250), 120, -120, 6, 3),
    Ore('Gold Ore', Resource('Gold', 1, 5, 80), -150, -300, 10, 3),
    Ore('Sapphire Ore', Resource('Sapphire', 1, 3, 1150), -145, -190, 30, 4, True),
    Ore('Limonite', Resource('Nickel', 1, 0, 0), -225, -240, 75, 4),
    Ore('Lead Ore', Resource('Lead', 1, 0, 0), -225, -315, 5, 4),
    Ore('Ruby Ore', Resource('Ruby', 1, 4, 900), -120, -140, 40, 5, True),
    Ore('Titanium Ore', Resource('Titanium ', 1, 7, 775), -50, -150, 45, 6),
    Ore('Platinum Ore', Resource('Platinum', 1, 5, 12500), -300, -512, 55, 6),
    Ore('Quartz Ore', Resource('Quartz', 1, 8, 50), -120, -150, 35, 7),
    Ore('Silver Ore', Resource('Silver', 1, 6, 750), -250, -512, 15, 7),
    Ore('Obsidian Ore', Resource('Obsidian', 1, 9, 25), -200, -512, 40, 8, True),
    Ore('Tungsten Ore', Resource('Tungsten', 1, 10, 1235), -300, -355, 35, 9),
    Ore('Uranium Ore', Resource('Uranium', 1, 0, 0), -480, -512, 50, 10, True),
]


class MineEvent:
    def __init__(self, depth, pick_level, times):
        self.depth = depth
        self.pick_level = pick_level
        self.times = times

    def mine(self):
        ore_mined_list = []
        for ore in ore_list:
            ore = ore.mine(self.depth, self.pick_level)
            if ore != 0:
                ore_mined_list.append(ore)
                print(ore)
        return ore_mined_list
