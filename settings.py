
### GEAR POOL SETTINGS
use_tutorial_gear = False # boomboxes
use_shop_gear = False # onii, xsitsu, random, xana, goonie, kagan, koneko, mighty and gamer's sets, and guitars
use_event_gear = False # gear that was introduced in events (ex. slynk, landino and kurante's sets)
use_legendary_gear = False # marshall, musketeer and rebel's sets
use_rare_color_gear = True
use_legendary_color_gear = False

### GEAR SETTINGS
use_unobtainable_gear = True # will not ignore sets defined below
unobtainable_sets = ["e-poppy"] # not exhaustive
upgrades_per_gear_set = 90 # 0 = no upgrades, 6 = 1 per slot, 30 = 5 per slot, 90 = 15 per slot etc.
use_owned_gear = True # restricts selection to gear defined in owned.txt
mini_level = 20 # rank is calculated automatically

### PROGRAM SETTINGS
memory_saver = True # uses a modified method to create gear combinations in case you run into memory problems
debug = False # prints debug info and quits
timer = False # times the main loop

### GAMEPLAY SETTINGS
# percentage of hits that are Greats (the program assumes no Oks or Misses)
# only values above 0.05 have a significant impact
great_accuracy = 0
perfect_accuracy = 1 - great_accuracy

### SONG SETTINGS
song_length = 135 # from first note to last note
song_hit_count = 177 # Perfects + Greats
song_ln_count = 10 # just count them manually lol
song_note_count = song_hit_count - song_ln_count # aka tap count + ln count
# here's some predefined songs for ya:
# strawberry sherbet (easy) - length 135, hits 177, lns 10
# be my time machine (hard) - length 127, hits 1502, lns 255

### ALGORITHM SETTINGS
smooth_fever_percentage = True # modified fever percentage formula
formulaic_stats = True # fit a polynomial onto the stat data to get smoother values
polynomial_degree = 8