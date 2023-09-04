import random

from bot import bot

def lerp(a, b, t): #woah!! an actual function defined without necessity!!
    return a*(1 - t) + b*t

def unlerp(a, b, t):
    return (t-a)/(b-a)

def english(numbers):
    if len(numbers) == 0:
        return ""
    elif len(numbers) == 1:
        return str(numbers[0])
    elif len(numbers) == 2:
        return str(numbers[0]) + " and " + str(numbers[1])
    else:
        formatted_numbers = [str(num) for num in numbers[:-1]]
        formatted_numbers.append("and " + str(numbers[-1]))
        return ", ".join(formatted_numbers)


async def roll(ctx, *, arguments: str = None):
    msg = []
    total = []
    clownAlert = bot.get_channel(987247910301364284)
    #splitting dice and bonus in two
    try: differentThings = arguments.split(" ")
    except: differentThings = ['d100']
    for index, e in enumerate(differentThings):
        msg.append({'args': e})
        #initialize these otherwise shit gets broken.
        bonus=None
        dice=None
        #since the first one is ALWAYS d, and d has to be there in order for everything to work..
        perish = e.replace('0', ' ').replace('1', ' ').replace('2', ' ').replace('3', ' ').replace('4', ' ').replace('5', ' ').replace('6', ' ').replace('7', ' ').replace('8', ' ').replace('9', ' ').replace(':', ' ').replace('i', ' ').replace(',', ' ').split()
        fiend = e.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('/', ' ').split()
        if len(perish) != len(fiend):
            await ctx.response.send_message("Errno 01.1: The modifiers are incomplete.");return
        else:
            x=0
            killurself = []
            for e in perish:
                killurself.append(perish[x]+fiend[x])
                x+=1
            del killurself[0]
            bonus="".join(killurself)
            if bonus == "":
                bonus=None
        dice = fiend[0]
        if bonus!=None and "*" in bonus:
            readableBonus = bonus.replace('*', '\*')
        else:
            readableBonus = bonus
        if len("".join(perish).replace('d', '')) != len(fiend)-1:# and bonus!=None:
            await ctx.response.send_message("Errno 01.2: The modifiers are incomplete.");return
        if dice == None: #this is understandable, but if you do "v!roll d" i hate you
            number = 1
            high = 100
            low = 1
        elif dice.count("d") != 1 and len(dice) != 0:
            await ctx.response.send_message("Errno 02.1: You did the dice command incorrectly.");return
        if dice != None:
            if dice == "d" and bonus is None:
                print(f"{ctx.user.id} is a fucking dumbass") #this is so i can SHAME YOU
            thanosnap = dice.split("d")
            number = thanosnap[0]
            purpose = None
            if dice.replace('i', '') != dice:
                identity = dice.split("i")
                if identity[1].replace(',', '') != identity[1]: #this is where it actually turns into brainfuck
                    ohNo = identity[1].split(",")
                    purpose = [] #I asked for the perfect rolling bot, but the cost of perfection is infinite.
                    for b in ohNo: purpose.append(int(b))
                else:
                    if identity[1] != "":
                        try: purpose = int(identity[1])
                        except: purpose = None
                    else:
                       await ctx.response.send_message("Errno 03.1: Specify which number you want to be modified when you use ``i``.");return
            if purpose != None:
                if int(number) <= 1:
                   await ctx.response.send_message("Errno 04.1: Only use the ``i`` when needed.");return
                else:
                    if bonus is None:
                        await ctx.response.send_message("Errno 04.2: Only use the ``i`` when needed.");return
                    else:
                        if purpose == 0:
                            await ctx.response.send_message("Errno 05.1: Invalid index for individual modifier.");return
            if thanosnap[1].count(":") != 0:
                andagain = thanosnap[1].split(":")
                try: low = int(andagain[0])
                except ValueError: await ctx.response.send_message("Errno 06.1: You used the ``i`` incorrectly.");return
                if dice.replace('i', '') != dice:
                    yes = andagain[1].split("i")
                    high = int(yes[0])
                else:
                    try: high = int(andagain[1])
                    except ValueError: await ctx.response.send_message("Errno 06.2: You used the ``i`` incorrectly.");return
            else:
                if thanosnap[1] == "" or thanosnap[0] == None:
                    high = 100
                    low = 1
                else:
                    ihatemylife = thanosnap[1].split("i")
                    try: high = int(ihatemylife[0])
                    except: high = 100
                    finally: low = 1
        if high <= 1:
            await ctx.response.send_message("Errno 07.1: You can't roll a d0 or d1.");return
        if number == None or number == "": number = 1 #failsafe
        if int(number) == 0:
            await ctx.response.send_message("Errno 08.1: You can't roll 0 times.");return
        if int(number) > 1:
            a=0
            constantinople=[]
            istanbul=[]
            while a != int(number):
                #yes i know this looks stupid but otherwise it links them together like a retard
                i = random.randint(low,high)
                constantinople.append(i)
                istanbul.append(i)
                a+=1
        else:
            i = random.randint(low,high)
        #NOTE: I fucking hate regex, why do you have to turn a simple task into brainfuck
        if bonus == None: #the killur and self variables are references to a quackity video
            killur = None
            self = None
        else:
            killur = bonus.replace('0', ' ').replace('1', ' ').replace('2', ' ').replace('3', ' ').replace('4', ' ').replace('5', ' ').replace('6', ' ').replace('7', ' ').replace('8', ' ').replace('9', ' ').split()
            self = bonus.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('/', ' ').split()
        if bonus is not None and (killur == None or self == None or bonus.replace('+', '').replace('-', '').replace('*', '').replace('/', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '') != ""): #uh oh, retard code alert
            await ctx.response.send_message("Errno 09.1: You did the modifiers incorrectly.");return
        if bonus is None:
            if int(number) > 1:
                total.append(sum(constantinople))
                msg[index]['out'] = f"{english(constantinople)}, [total **{sum(constantinople)}**]"
                msg[index]['level'] = unlerp(low * int(number), high * int(number), sum(constantinople))
            else:
                total.append(i)
                msg[index]['out'] = f"**{i}**"
                msg[index]['level'] = unlerp(low, high, i)
        else:
            if len(killur) != len(self):
                await ctx.response.send_message("Errno 01.3: The modifiers are incomplete.");return
            if purpose != None:
                if type(purpose) == int:
                    if int(number) < purpose-1:
                        await ctx.response.send_message("Errno 05.2: Invalid index for individual modifier.");return
                if type(purpose) == list:
                    for p in purpose:
                        if int(number) < p-1:
                            await ctx.response.send_message("Errno 05.3: Invalid index for individual modifier.");return
            if int(number) > 1:
                if purpose != None:
                    if type(purpose) == list:
                        for p in purpose:
                            x=0
                            for n in killur:
                                if killur[x] == "+":
                                    istanbul[p-1]+=int(self[x])
                                elif killur[x] == "-":
                                    istanbul[p-1]-=int(self[x])
                                elif killur[x] == "*":
                                    istanbul[p-1]*=int(self[x])
                                elif killur[x] == "/":
                                    try: istanbul[p-1]/=int(self[x])
                                    except ZeroDivisionError:
                                        await ctx.response.send_message("Errno 11.1: You attempted to divide by zero.");return
                                x+=1
                    else:
                        y=purpose-1
                        x=0
                        for n in killur:
                            if killur[x] == "+":
                                istanbul[y]+=int(self[x])
                            elif killur[x] == "-":
                                istanbul[y]-=int(self[x])
                            elif killur[x] == "*":
                                istanbul[y]*=int(self[x])
                            elif killur[x] == "/":
                                try: istanbul[y]/=int(self[x])
                                except ZeroDivisionError:
                                    await ctx.response.send_message("Errno 11.2: You attempted to divide by zero.");return
                            x+=1
                else:
                    y=0
                    for c in constantinople:
                        x=0
                        for n in killur:
                            if killur[x] == "+":
                                istanbul[y]+=int(self[x])
                            elif killur[x] == "-":
                                istanbul[y]-=int(self[x])
                            elif killur[x] == "*":
                                istanbul[y]*=int(self[x])
                            elif killur[x] == "/":
                                try: istanbul[y]/=int(self[x])
                                except ZeroDivisionError:
                                    await ctx.response.send_message("Errno 11.3: You attempted to divide by zero.");return
                            x+=1
                        y+=1
            else:
                e=i
                x=0
                for n in killur:
                    if killur[x] == "+":
                        e+=int(self[x])
                    elif killur[x] == "-":
                        e-=int(self[x])
                    elif killur[x] == "*":
                        e*=int(self[x])
                    elif killur[x] == "/":
                        try: e/=int(self[x])
                        except ZeroDivisionError:
                            await ctx.response.send_message("Errno 11.4: You attempted to divide by zero.");return
                    x+=1
            if int(number) > 1: #the clownAlerts are only if someone triggers the 4000+ character limit
                x=0
                tot = sum(constantinople)
                for n in killur:
                    if killur[x] == "+": tot+=int(self[x])
                    elif killur[x] == "-": tot-=int(self[x])
                    elif killur[x] == "*": tot*=int(self[x])
                    elif killur[x] == "/":
                        try: tot/=int(self[x])
                        except ZeroDivisionError:
                            await ctx.response.send_message("Errno 11.5: You attempted to divide by zero.");return
                    x+=1
                msg[index]['out'] = f"{english(istanbul)}. [total **{sum(istanbul)}**]"
                msg[index]['raw'] = f"{english(constantinople)}, [total **{sum(constantinople)}**]" #[modded total **{tot}**] (decided not to keep this)
                msg[index]['level'] = unlerp(low * int(number), high * int(number), sum(constantinople)) #trust me anything more complex would be programming purgatory
            else:
                x=0
                tot = i
                for n in killur:
                    if killur[x] == "+": tot+=int(self[x])
                    elif killur[x] == "-": tot-=int(self[x])
                    elif killur[x] == "*": tot*=int(self[x])
                    elif killur[x] == "/":
                        try: tot/=int(self[x])
                        except ZeroDivisionError:
                            await ctx.response.send_message("Errno 11.6: You attempted to divide by zero.");return
                    x+=1
                msg[index]['out'] = f"**{e}**"
                msg[index]['raw'] = f"**{i}**"
                msg[index]['level'] = unlerp(low,high,i)
    level = sum([i['level'] for i in msg])/len(msg) #this is how well you did and is used for color
    color = [255*(1-level),255*level,0]
    embed = discord.Embed(title="Here are your rolls!", color=round(color[0])*0x10000+round(color[1])*0x100+round(color[2])) #color wizardry dont worry about it
    for i in msg:
        if 'raw' in list(i.keys()):
            embed.add_field(name=f"You rolled [{i['args']}] and got...", value=f"{i['out']}, with raw {i['raw']}.", inline=False)
        else:
            embed.add_field(name=f"You rolled [{i['args']}] and got...", value=f"{i['out']}.", inline=False)

    try: await ctx.response.send_message(ctx.user.mention,embed=embed)
    except:
        await ctx.response.send_message(f"Errno 12.1: The maximum character limit was exceeded.")
        await clownAlert.send(f"-=- OFFICIAL WEE WOO POLICE NOTIFIER -=-\n\nThis is a notification to tell you that the 2000 character limit was exceeded in <#{ctx.channel.id}> by <@{ctx.user.id}>! Please add more details in the future.\n\n-=- FOR THE EYES OF <@184145857526890506> -=-")