from numpy.polynomial.polynomial import Polynomial as poly
from datetime import datetime as dt
import settings

### PROCESS DATA

# create gears
# sources:
# legendary gear: https://gyazo.com/88629460c091fcf444dbc1e20d06021f
# rare gear: https://gyazo.com/18b5c3dcd905cff7d8300917e9a53b2e
# shop and event gear: https://docs.google.com/document/d/1h3K3prLtUAKS0EYf8pcuvQsw6Ky33T9FjDbW7Bgzni4
# thanks to thestaticbro, vkess, samkoopayyy, 789legendary987 and robeatsgearmaster for these
gear_input = open("rodata/gears.txt", "r").read().split("\n")[1:]
gears = {}
for gear_set in gear_input:
    lines = gear_set.split("\t")
    name = lines[0] if lines[0][:2] in ["r-", "l-", "b-", "g-"] else lines[0][2:]
    geartype = lines[0][:2]
    if (((geartype == "r-" and settings.use_rare_color_gear)
    or (geartype == "l-" and settings.use_legendary_color_gear)
    or (geartype == "x-" and settings.use_legendary_gear)
    or (geartype == "b-" and settings.use_tutorial_gear)
    or (geartype == "s-" and settings.use_shop_gear)
    or (geartype == "g-" and settings.use_shop_gear) # guitars
    or (geartype == "e-" and settings.use_event_gear))
    and (name not in settings.unobtainable_sets or settings.use_unobtainable_gear))\
    or settings.use_owned_gear:
        gears[name] = []
        for gear in lines[1:]:
            if gear: # can be empty line
                if gear != "-":
                    x = []
                    for stat in gear.split(" "):
                        stat = stat.split(",")
                        x.append((stat[0], int(stat[1])))
                    gears[name].append(x)
                else:
                    gears[name].append(None)

# create gear material costs
cost_input = open("rodata/costs.txt", "r").read().split("\n")[1:]
material_costs = {}
for gear_set in cost_input:
    lines = gear_set.split("\t")
    name = lines[0]
    material_costs[name] = []
    for gear in lines[1:]:
        if gear:
            x = []
            for material in gear.split(" "):
                material = material.split(",")
                x.append((material[0], int(material[1])))
            material_costs[name].append(x)

# create material price in coins
# from https://docs.google.com/document/d/1AvRHLc-zukyuA0fnEKWvkDz5_PVG3Ci_NScnh2SZJiI
# thanks to tishi for organizing that
price_input = open("rodata/prices.txt", "r").read().split("\n")[1:]
material_price = {}
for line in price_input:
    line = line.split("\t")
    material_price[line[0]] = int(line[-1])

# create minis. all stats are for max level but since they scale slowly and linearly (?) it should hold for lower levels
mini_input = open("rodata/minis.txt", "r").read().split("\n")[1:]
minis = {}
mini_level = 0 if settings.mini_level < 0 else settings.mini_level
mini_level = 50 if mini_level > 50 else int(mini_level)
for line in mini_input:
    line = [c for c in line.split("\t") if c]
    output = []
    cmult = 1 + 1.5 * mini_level / 20 if mini_level < 20 else 2.5 + 2.5 * (mini_level - 20) / 30
    smult = 1 if mini_level < 20 else int(mini_level / 10 - 0.6)
    for y in line[1].split(" "):
        y = y.split(",")
        output.append((y[0], int(int(y[1]) * cmult)))
    for y in line[2].split(" "):
        y = y.split(",")
        output.append((y[0], int(int(y[1]) * smult)))
    minis[line[0]] = output
mini_list = list(minis.keys())

# create upgrades
upgrade_input = open("rodata/upgrades.txt", "r").read().split("\n")[1:]
upgrades = {}
for line in upgrade_input:
    line = line.split("\t")
    upgrades[line[0]] = [(y.split(",")[0], int(y.split(",")[1])) for y in line[-1].split(" ")]
upgrade_list = list(upgrades.keys())

# create owned gear
if settings.use_owned_gear:
    owned_gears = {}
    for gear_set in gears:
        owned_gears[gear_set] = [None, None, None, None, None, None]
    owned_input = open("rodata/owned.txt", "r").read().split("\n")[1:]
    for line in owned_input:
        line = [i for i in line.split("\t") if i]
        slot = {"hat": 0, "neck": 1, "face": 2, "shirt": 3, "back": 4, "pants": 5}[line[0]]
        gear_set = line[1]
        if len(line) > 2:
            gear_upgrades = line[2].split(",")
        else:
            gear_upgrades = []
        gear_stats = {}
        for stat, value in gears[gear_set][slot]:
            if stat in gear_stats:
                gear_stats[stat] += value
            else:
                gear_stats[stat] = value
        for upgrade in gear_upgrades:
            for stat, value in upgrades[upgrade]:
                if stat in gear_stats:
                    gear_stats[stat] += value
                else:
                    gear_stats[stat] = value
        owned_gears[gear_set][slot] = [(stat, gear_stats[stat]) for stat in gear_stats.keys()]
    gears = owned_gears

# create stat points to stat value dictionary
# stats go from +80 to +0 (for reasons)
# values are from https://docs.google.com/spreadsheets/d/15Rqlh579x2V7gMRFIai-cDQtGYgeMFehLBWWwekpDSU
# humongous thanks to lydiaplayz for that document! it's literally the backbone of this calculator
stat_input = open("rodata/stats.txt", "r").read().split("\n")[1:].__reversed__()
stat_value = {"pp": [], "ff": [], "ft": [], "fm": [], "cm": []}
stat_list = []
for line in stat_input:
    newline = []
    for r in line.split("\t"):  # remove empty columns (double tabs)
        if r: newline.append(r)
    stat_list.append([float(s) for s in newline])
if settings.formulaic_stats:
    pp_coefs = poly.fit(range(81), [l[0] for l in stat_list], settings.polynomial_degree).convert().coef
    ff_coefs = poly.fit(range(81), [l[1] for l in stat_list], settings.polynomial_degree).convert().coef
    ft_coefs = poly.fit(range(81), [l[3] for l in stat_list], settings.polynomial_degree).convert().coef
x = 0
for line in stat_list:
    if settings.formulaic_stats: # for smooth increases in stats
        pp = sum([pp_coefs[n] * x ** n for n in range(settings.polynomial_degree + 1)])
        ff = sum([ff_coefs[n] * x ** n for n in range(settings.polynomial_degree + 1)])
        ft = sum([ft_coefs[n] * x ** n for n in range(settings.polynomial_degree + 1)])
        x += 1
    else: # by using the raw rounded values, there could be situations where stats seemingly don't increase when upgrading
        pp = float(line[0])
        ff = float(line[1])
        ft = float(line[3])
    fm = float(line[2])
    cm = float(line[4])
    # we can save time on a bunch of calculations by doing them outside the loop, here!
    # Average Accuracy Points = <Perfect Points> * Perfect Accuracy + 150 * Great Accuracy
    stat_value["pp"].append(pp * settings.perfect_accuracy + 150 * settings.great_accuracy)
    # Fever Fill Time = ( (Song Note Count / 3) / ((Perfect Accuracy + 0.5 * Great Accuracy) / <Fever Fill Rate>) ) / Song Hit Density
    stat_value["ff"].append(((settings.song_note_count / 3) / ((settings.perfect_accuracy + 0.5 * settings.great_accuracy) / ff)) / (settings.song_hit_count / settings.song_length))
    # this is just <Fever Multiplier> though
    stat_value["fm"].append(fm)
    # Effective Fever Time = Song Length * (<Fever Time> * 0.16/1.67 + 0.0435)
    stat_value["ft"].append(settings.song_length * (ft * 0.16/1.67 + 0.0435))
    # Average Combo Multiplier = ( (49.5  + Song Hit Count) * (<Combo Multiplier> - 1) + Song Hit Count ) / Song Hit Count
    stat_value["cm"].append(((49.5 + settings.song_hit_count) * (cm - 1) + settings.song_hit_count) / settings.song_hit_count)

# we calculate song fever percentage for all possible combinations of fever fill time and effective fever time beforehand
# this way, we don't have to repeat the super-slow division operations (integer division?! yucky!!) 250k times
fever_percentage_from_stats = []
for ff in range(81):
    y = []
    for ft in range(81):
        fever_fill_time = stat_value["ff"][ff]
        effective_fever_time = stat_value["ft"][ft]
        fever_cycle = fever_fill_time + effective_fever_time
        if settings.smooth_fever_percentage: # this alarmingly simple formula appears when song_length approaches infinity
            song_fever_percentage = effective_fever_time / fever_cycle - 10 / settings.song_length
            # i subtract 10/length to "de-idealize" the formula
        else:
            cycle_count = settings.song_length // fever_cycle
            incomplete_cycle = settings.song_length - fever_cycle * cycle_count  # song_length % fever_cycle
            if incomplete_cycle > fever_fill_time:  # if the final fever cycle got into the "fever phase" (active fever when song finished)
                song_fever_percentage = (effective_fever_time * cycle_count + incomplete_cycle - fever_fill_time) / settings.song_length
            else:
                song_fever_percentage = effective_fever_time * cycle_count / settings.song_length
        y.append(song_fever_percentage)
    fever_percentage_from_stats.append(y)


### FUNCTIONS

# returns the stats of the gear
def get_stats(current_gear):
    gear_stats = {"r": 0, "c": 0, "v": 0, "f": 0, "b": 0, "fm": 0, "pp": 0, "ff": 0, "cm": 0, "ft": 0}
    slot = 0
    for gear_set in current_gear:
        for stat, value in gears[gear_set][slot]:
            gear_stats[stat] += value
        slot += 1
    return gear_stats

# returns needed materials for the gear
def get_material_cost(current_gear):
    cost = {}
    slot = 0
    for gear_set in current_gear:
        if gear_set in material_costs:
            gear_cost = material_costs[gear_set][slot]
            for material in gear_cost:
                if material[0] in cost:
                    cost[material[0]] += material[1]
                else:
                    cost[material[0]] = material[1]
        slot += 1
    return cost

# gets a score from some current stats. self-explanatory
def get_score(current_stats, increase=None):
    stats = {}
    for stat in current_stats:
        stats[stat] = current_stats[stat]
    if increase:
        for stat in increase:
            stats[stat[0]] += stat[1]
    # get from stat_value
    ff = 80 if stats["ff"] > 80 else stats["ff"]
    ft = 80 if stats["ft"] > 80 else stats["ft"]
    fever_multiplier = stat_value["fm"][80] if stats["fm"] > 80 else stat_value["fm"][stats["fm"]]
    average_accuracy_points = stat_value["pp"][80] if stats["pp"] > 80 else stat_value["pp"][stats["pp"]]
    average_combo_multiplier = stat_value["cm"][80] if stats["cm"] > 80 else stat_value["cm"][stats["cm"]]
    # time to calculate!
    song_fever_percentage = fever_percentage_from_stats[ff][ft]
    average_fever_multiplier = fever_multiplier * song_fever_percentage - song_fever_percentage + 1
    color_points = stats[primary_color] * 2 + stats[secondary_color]
    return (average_accuracy_points + color_points) * average_combo_multiplier * average_fever_multiplier

def consider_combination(gear): # is there already a better combination in combinations? only used if memory_saver
    gear_stats = list(get_stats(gear).values())
    accepted = False

    if accepted:
        combinations.append(gear)
        combinations_stats.append(gear_stats)

# create all combinations of gear
def gear_combinations(cur=None, slot=0):
    if cur is None:
        cur = []
    if slot != 5:
        for gear_set in gears:
            if gears[gear_set][slot]:
                gear_combinations(cur + [gear_set], slot + 1)
    else:
        for gear_set in gears:
            if gears[gear_set][slot]:
                combinations.append(cur + [gear_set])
def gear_combinations_memory_saver(cur=None, slot=0):
    if cur is None:
        cur = []
    if slot != 5:
        for gear_set in gears:
            if gears[gear_set][slot]:
                gear_combinations_memory_saver(cur + [gear_set], slot + 1)
    else:
        for gear_set in gears:
            if gears[gear_set][slot]:
                yield cur + [gear_set]



### PRINT INFO

primary_color = "r" # it doesn't matter, they're all 0 anyway
secondary_color = "r"
base_score = get_score({"r": 0, "c": 0, "v": 0, "f": 0, "b": 0, "fm": 0, "pp": 0, "ff": 0, "cm": 0, "ft": 0})
def prepare_time(time): # excessively complicated function for converting microseconds to a proper time
    year = dt.now().year
    month = dt.now().month
    day = dt.now().day
    days = time // (1000000 * 60 * 60 * 24)
    hours = time % (1000000 * 60 * 60 * 24) // (1000000 * 60 * 60)
    minutes = time % (1000000 * 60 * 60) // (1000000 * 60)
    seconds = time % (1000000 * 60) // 1000000
    microseconds = time % 1000000
    dateformat = "%H:%M:%S.%f"
    if days:
        return str(days) + "d;" + dt.strftime(dt(year, month, day, hours, minutes, seconds, microseconds), dateformat)
    else:
        return dt.strftime(dt(year, month, day, hours, minutes, seconds, microseconds), dateformat)
combinations_length = 1
for slot in range(6):
    combinations_length *= len([gears[s][slot] for s in gears if gears[s][slot]])
print("Gear combination count: " + str(combinations_length))
if settings.use_owned_gear:
    print("Predicted time per song color: " + prepare_time(230 * combinations_length) + " to " + prepare_time(260 * combinations_length))
    print("Predicted time total: " + prepare_time(25 * 230 * combinations_length) + " to " + prepare_time(25 * 260 * combinations_length))
else:
    print("Predicted time per song color: " + prepare_time(2800 * combinations_length) + " to " + prepare_time(3100 * combinations_length))
    print("Predicted time total: " + prepare_time(25 * 2800 * combinations_length) + " to " + prepare_time(25 * 3100 * combinations_length))
print("Base predicted score: " + str(int(base_score * settings.song_hit_count)))
print("Combining gear...")
combinations = []
if settings.memory_saver:
    combinations_stats = []
    print("Predicted combination time: " + prepare_time(2500 * combinations_length) + " to " + prepare_time(2900 * combinations_length))
    now = dt.now()
    combinations = gear_combinations_memory_saver()
    print("Combining gear time: " + str(dt.now() - now))
    import time
    for a in combinations:
        print(a)
        time.sleep(.25)
else:
    now = dt.now()
    gear_combinations()
    print("Combining gear time: " + str(dt.now() - now))
if settings.debug:
    print(gears)
    print(material_costs)
    print(material_price)
    print(minis, mini_list)
    print(upgrades, upgrade_list)
    print(stat_value)
    quit()



### MAIN LOOP

while True:
    # create song colors
    song_colors = []
    song_colors_raw = input("Song color(s): ")
    if song_colors_raw == "all":
        song_colors = []
        for a in ["r", "c", "v", "f", "b"]:
            for b in ["r", "c", "v", "f", "b"]:
                song_colors.append(a + b)
            song_colors.append("") # skip
    else:
        song_colors = song_colors_raw.split(" ")
    # check song color
    bad = False
    for song_color in song_colors:
        for c in song_color:
            if c not in "rcvfb" or len(song_color) != 2:
                bad = True
    if bad:
        print("Bad color...")
        continue

    # main main loop?
    datalist = {"r": [], "c": [], "v": [], "f": [], "b": []}
    geardump = {}
    average_time = []
    average_time_per = []
    total_now = dt.now()
    for song_color in song_colors:
        if not song_color:
            print()
        else:
            primary_color = song_color[0]
            secondary_color = song_color[1]
            best_combination = []
            best_score = 0
            best_upgrades = []
            best_stats = {}
            if settings.use_owned_gear:
                if settings.timer:
                    now = dt.now()
                for combination in combinations: # yup, all 250k of them
                    gear_stats = get_stats(combination)
                    used_minis = []
                    temp_mini_list = mini_list.copy()
                    for n in range(3):
                        best = max(temp_mini_list, key=lambda x:get_score(gear_stats, minis[x]))
                        used_minis.append(best)
                        temp_mini_list.remove(best)
                        for stat, value in minis[best]:
                            gear_stats[stat] += value
                    new_score = get_score(gear_stats)
                    if new_score > best_score:
                        best_score = new_score
                        best_combination = combination
                        best_stats = gear_stats.copy()
                        best_minis = used_minis.copy()
                if settings.timer:
                    print("Time taken: " + str(dt.now() - now) + " (" + str((dt.now() - now) / len(combinations)) + " per combination)")
                    average_time.append(dt.now() - now)
                    average_time_per.append((dt.now() - now) / len(combinations))

            else:
                if settings.timer:
                    now = dt.now()
                for combination in combinations: # yup, all 250k of them
                    gear_stats = get_stats(combination)
                    used_upgrades = []
                    used_minis = []
                    temp_mini_list = mini_list.copy()
                    # time to upgrade this gear a bunch of times!
                    # everytime we upgrade, we pick the upgrade that will increase score the most.
                    for n in range(settings.upgrades_per_gear_set):
                        best = max(upgrade_list, key=lambda x: get_score(gear_stats, upgrades[x]))
                        used_upgrades.append(best)
                        for stat, value in upgrades[best]:
                            gear_stats[stat] += value
                    for n in range(3):
                        best = max(temp_mini_list, key=lambda x:get_score(gear_stats, minis[x]))
                        used_minis.append(best)
                        temp_mini_list.remove(best)
                        for stat, value in minis[best]:
                            gear_stats[stat] += value
                    # compare to previous best
                    new_score = get_score(gear_stats)
                    if new_score > best_score:
                        best_score = new_score
                        best_combination = combination
                        best_stats = gear_stats.copy()
                        best_upgrades = used_upgrades.copy()
                        best_minis = used_minis.copy()
                if settings.timer:
                    print("Time taken: " + str(dt.now() - now) + " (" + str((dt.now() - now) / len(combinations)) + " per combination)")
                    average_time.append(dt.now() - now)
                    average_time_per.append((dt.now() - now) / len(combinations))


            # print results
            print("Color: " + song_color)
            print("Gear: " + str(best_combination))
            if not settings.use_owned_gear:
                best_upgrades_short = {}
                best_upgrades_shorter = {}
                for u in best_upgrades:
                    if u in best_upgrades_short:
                        best_upgrades_short[u] += 1
                    else:
                        best_upgrades_short[u] = 1
                if settings.upgrades_per_gear_set > 30:
                    for u in best_upgrades[:30]:
                        if u in best_upgrades_shorter:
                            best_upgrades_shorter[u] += 1
                        else:
                            best_upgrades_shorter[u] = 1
                    print("Upgrades (first free 30): " + str(best_upgrades_shorter))
                    print("Upgrades (all): " + str(best_upgrades_short))
                else:
                    print("Upgrades: " + str(best_upgrades_short))
                print("Upgrade order: " + str(best_upgrades))
            print("Minis: " + str(best_minis))
            print("Gear stats: " + str(get_stats(best_combination)))
            print("Total stats: " + str(best_stats))
            print("Multiplier: " + str(round(get_score(best_stats) / base_score, 2)))
            if secondary_color != primary_color:
                og_secondary_color = secondary_color
                secondary_color = primary_color # how hacky
                print("Pure color multiplier: " + str(round(get_score(best_stats) / base_score, 2)))
                secondary_color = og_secondary_color
            if not settings.use_owned_gear:
                mat_cost = get_material_cost(best_combination)
                material_cost = {} # sorted mat_cost
                for x in sorted(mat_cost):
                    material_cost[x] = mat_cost[x]
                if settings.use_legendary_color_gear or settings.use_legendary_gear or settings.use_rare_color_gear:
                    print("Material cost: " + str(material_cost))
                if settings.use_legendary_color_gear or settings.use_legendary_gear:
                    print("Price in coins: " + str(sum([material_price[x] * mat_cost[x] for x in mat_cost])))
            print()

    # print some raw data for my excel document
            if song_colors_raw == "all" and not settings.use_owned_gear:
                if settings.use_legendary_color_gear or settings.use_legendary_gear:
                    toappend = best_combination.copy()
                    for gt in ["g-red", "g-blue", "g-green", "g-purple", "g-orange", "t-brass", "t-silver", "t-gold"]:
                        if gt in mat_cost:
                            toappend.append(str(mat_cost[gt]))
                        else:
                            toappend.append(" ")
                    toappend.append(str(sum([material_price[x] * mat_cost[x] for x in mat_cost])))
                    for upg in [("fm", "r"), ("pp", "c"), ("ff", "v"), ("cm", "f"), ("ft", "b")]:
                        tosum = 0
                        for upgr in upg:
                            if upgr in best_upgrades_shorter:
                                tosum += best_upgrades_shorter[upgr]
                        toappend.append(str(tosum) if tosum else " ")
                    totsum = 0
                    for upg in [("fm", "r", "red"), ("pp", "c", "blue"), ("ff", "v", "green"), ("cm", "f", "purple"), ("ft", "b", "orange")]:
                        tosum = 0
                        for upgr in upg[:2]:
                            if upgr in best_upgrades_short:
                                tosum += best_upgrades_short[upgr]
                        toappend.append(str(tosum) if tosum else " ")
                        totsum += material_price["g-" + upg[2]] * tosum
                    toappend.append(str(totsum))
                    datalist[secondary_color].append(toappend)
                else:
                    toappend = best_combination.copy()
                    for gt in ["l-red", "l-blue", "l-green", "l-purple", "l-orange", "m-red", "m-blue", "m-green", "m-purple", "m-orange"]:
                        if gt in mat_cost:
                            toappend.append(str(mat_cost[gt]))
                        else:
                            toappend.append(" ")
                    for upg in [("fm", "r"), ("pp", "c"), ("ff", "v"), ("cm", "f"), ("ft", "b")]:
                        tosum = 0
                        for upgr in upg:
                            if upgr in best_upgrades_shorter:
                                tosum += best_upgrades_shorter[upgr]
                        toappend.append(str(tosum) if tosum else " ")
                    for upg in [("fm", "r"), ("pp", "c"), ("ff", "v"), ("cm", "f"), ("ft", "b")]:
                        tosum = 0
                        for upgr in upg:
                            if upgr in best_upgrades_short:
                                tosum += best_upgrades_short[upgr]
                        toappend.append(str(tosum) if tosum else " ")
                    datalist[secondary_color].append(toappend)

    if song_colors_raw == "all" and not settings.use_owned_gear:
        for secondary_color in ["r", "c", "v", "f", "b"]:
            for valuelist in datalist[secondary_color]:
                print("§".join(valuelist), end="")
                print("¤", end="")
            print("£", end="")
        print()

    if settings.timer and song_colors_raw == "all":
        print("Average time taken: " + str(sum(average_time) / len(average_time)) + " (" + str(sum(average_time_per) / len(average_time_per)) + " per combination)")
    print("Total time taken: " + str(dt.now() - total_now))