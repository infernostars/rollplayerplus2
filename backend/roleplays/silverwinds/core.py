import random


class Resource:
    def __init__(self, name: str, count: int, harvest_level: int, durability: int):
        self.name = name
        self.count = count
        self.harvest_level = harvest_level
        self.durability = durability


class Ore:
    def __init__(self, name: str, resource: Resource, depth_min: int, depth_max: int, rarity: int, pick_level: int,
                 no_ore: bool = True):
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

    def mine(self, depth, pick_level, use_triangular=False):
        if self.depth_min <= depth <= self.depth_max and self.pick_level <= pick_level:
            if self.triangular:
                # Calculate the adjusted rarity.
                midpoint = (self.depth_max + self.depth_min) / 2
                adjusted_rarity = (1 / self.rarity) * abs(depth - midpoint)

                # Use a triangular distribution for the success chance.
                success_chance = random.triangular(self.depth_min, self.depth_max, midpoint)

                # Test if mining is successful.
                success = success_chance <= adjusted_rarity
            else:
                # Use the default success condition.
                success = random.randint(1, self.rarity) == 1

            if success:
                mined_resource = Resource(
                    self.resource.name,
                    self.resource.count,  # use the original count value
                    self.resource.harvest_level,
                    self.resource.durability)

                mined_ore = Ore(
                    self.name,
                    mined_resource,
                    self.depth_min,
                    self.depth_max,
                    self.rarity,
                    self.pick_level,
                    self.name == self.resource.name)

                return mined_ore

        # Mining failed or conditions not right for mining.
        return 0


ore_list = [
    Ore('Clay Ore', Resource('Clay', 1, 0, 0), 5, -20, 4, 0, no_ore=True),

    Ore('Stone Ore', Resource('Stone', 1, 2, 100), 256, -512, 1, 1, no_ore=True),
    Ore('Coal Ore', Resource('Coal', 1, 0, 0), 256, -120, 12, 1, no_ore=True),
    Ore('Tin Ore', Resource('Tin', 1, 3, 100), 256, -512, 16, 2, no_ore=True),
    Ore('Copper Ore', Resource('Copper', 1, 4, 200), 200, -100, 20, 3),

    Ore('Iron Ore', Resource('Iron', 1, 5, 250), 120, -120, 50, 3),

    Ore('Gold Ore', Resource('Gold', 1, 5, 80), -150, -300, 200, 3),

    Ore('Sapphire Ore', Resource('Sapphire', 1, 3, 1150), -145, -190, 180, 4, no_ore=True),
    Ore('Limonite', Resource('Nickel', 1, 0, 0), -225, -240, 115, 4),
    Ore('Lead Ore', Resource('Lead', 1, 0, 0), -225, -315, 120, 4),

    Ore('Ruby Ore', Resource('Ruby', 1, 4, 900), -120, -140, 400, 5, no_ore=True),

    Ore('Titanium Ore', Resource('Titanium', 1, 7, 775), -50, -150, 450, 6),
    Ore('Platinum Ore', Resource('Platinum', 1, 5, 12500), -300, -512, 550, 6),
    Ore('Quartz Ore', Resource('Quartz', 1, 8, 50), -120, -150, 350, 7),
    Ore('Silver Ore', Resource('Silver', 1, 6, 750), -250, -512, 150, 7),
    Ore('Obsidian Ore', Resource('Obsidian', 1, 9, 25), -200, -512, 400, 8, no_ore=True),

    Ore('Tungsten Ore', Resource('Tungsten', 1, 10, 1235), -300, -355, 350, 9),
    Ore('Uranium Ore', Resource('Uranium', 1, 0, 0), -480, -512, 500, 10, no_ore=True),
]

class MineEvent:
    def __init__(self, depth, pick_level, times):
        self.depth = depth
        self.pick_level = pick_level
        self.times = times

    def mine(self):
        ore_mined_dict = {}
        for _ in range(self.times):
            for ore in ore_list:
                mined_ore = ore.mine(self.depth, self.pick_level)
                if mined_ore != 0:
                    # if the ore is already in the dict, increment count
                    if mined_ore.name in ore_mined_dict:
                        ore_mined_dict[mined_ore.name].resource.count += mined_ore.resource.count
                    else:  # Otherwise, add the ore to the dict
                        ore_mined_dict[mined_ore.name] = mined_ore
        # Print the harvested ores
        for ore in ore_mined_dict.values():
            print(ore)
        return list(ore_mined_dict.values())  # Return the list of unique mined ores