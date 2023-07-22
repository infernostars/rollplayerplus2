import os
import random


def name_init() -> list[dict]:
    """Initializes the name generation chains."""
    out = dict()
    for namebase in os.listdir("data/name_generator"):
        def increment(lst, cur):
            if lst in list(chain.keys()):
                if cur in list(chain[lst].keys()):
                    chain[lst][cur] += 1
                else:
                    chain[lst][cur] = 1
            else:
                chain[lst] = dict()
                chain[lst][cur] = 1

        chain = dict()
        with open(os.path.join("data/name_generator", namebase), 'r', encoding='utf8') as f:  # open in readonly mode
            lines = f.read().splitlines()
            chain[0] = dict([tuple(i.split(':')) for i in lines[0].split('|')])
            lines = lines[1:]
        for line in lines:
            last = "#" * int(chain[0]['chainlength'])
            for i in line:
                increment(last, i)
                last = last[1:] + i
            increment(last, "#")
        out[os.path.splitext(namebase)[0]] = chain
    return out


namechains = name_init()


def name_generator(kind: str, amount: int = 10) -> list[str]:
    chain = namechains[kind]
    out = []
    chainlength = int(chain[0]['chainlength'])
    for _ in range(int(amount)):
        name = "#" * chainlength
        name += random.choices(list(chain[name].keys()),
                               weights=list(chain[name].values()))[0]
        # same thing as in the loop, done once, so it doesn't end with # immediately
        while True:
            while True:
                name += random.choices(list(chain[name[-chainlength:]].keys()),
                                       weights=list(chain[name[-chainlength:]].values()))[0]
                if name[-1] == "#":
                    if random.random() < len(name) / 24 - 1 / 24:  # end it
                        break
                    else:
                        name = name[:-1]  # try again
                else:
                    if random.random() < len(name) / 36 - 1 / 36:  # end it
                        name += "#"
                        break
                    else:
                        break
            if len(name) == 12 or name[-1] == "#":
                break
        out.append(''.join(name).replace('#', ''))
    return out
