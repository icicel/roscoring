# Roscoring

This tool calculates the optimal combination of gear, gear upgrades and minis required to theoretically maximize score from any given Robeats song.

### Vocabulary
*HIT* - An action that increases score. Single notes have one hit, long notes have two.

*NOTE* - One singular instance of a note, can be single or long.

### Facts

- Combo is updated (that is, increased by one) BEFORE points are given for hitting.
- All formulas may be completely wrong. Especially those involving Song Length and Song Note Count are guesswork.
- ***This formatting*** means it's a gear stat


# Score formulas

## Score per hit
> (AP + CP) * CM * FM

### AP (Accuracy Points)
> ***Perfect Points*** if Perfect, 150 if Great, 100 if Ok, 0 if Miss

### CP (Color Points)
> **Primary Color Power** * 2 + **Secondary Color Power**

### CM (Combo Multiplier)
> 1 + min(**Combo**/100, 1) * (***Combo Multiplier*** - 1)

### FM (Fever Multiplier)
> ***Fever Multiplier*** if Fever, 1 otherwise


## Total score
(idealized; assuming no Ok, no Miss, a bunch of other things)

> **Song Hit Count** * (AAP + ACP) * ACM * AFM

### AAP (Average Accuracy Points)
> ***Perfect Points*** * **Perfect Accuracy** + 150 * Great Accuracy

> (100% accuracy) ***Perfect Points***

### ACP (Average Color Points)
> **Color Points**

### ACM (Average Combo Multiplier)
> ( (49.5 + **Song Hit Count**) * (***Combo Multiplier*** - 1) + **Song Hit Count** ) / **Song Hit Count**

### AFM (Average Fever Multiplier)
> ***Fever Multiplier*** * FP - FP + 1


## Miscellaneous

### FP (Fever Percentage)
> TFF + EFT + TFF + EFT ... until >= **Song Length**

> (approximation) EFT / (EFT + TFF)

> (adjusted for imperfect fevers) EFT / (EFT + TFF) - 10 / **Song Length**

### EFT (Effective Fever Time)
This is almost completely guesswork, but comparing with lydiaplayz's fever percentage stats it actually works.
This can't be the actual formula used in Robeats, can it??? The constants are so arbitrary...
> **Song Length** * (***Fever Time*** * 0.16/1.67 + 0.0435)

### TFF (Time For Fever)
> HFF / HD

### HD (Hit Density)
> **Song Hit Count** / **Song Length**

### HFF (Hits For Fever)
> FSFF / FSPH

> (technically) ceil(FSFF / FSPH)

### FSFF (Fever Score For Fever)
> Song Note Count / 3

### FSPH (Fever Score Per Hit)
> AFA / ***Fever Fill Rate***

### AFA (Average Fever Accuracy)
> **Perfect Accuracy** + 0.5 * **Great Accuracy**

> (100% accuracy) 1



# Building Fever

Amount of Fever Score required for a Fever:
> **Song Note Count** / 3

Fever Score per hit:
> BA * FR

BA
> 1 if Perfect, 1/2 if Great, 0 if Ok

FR
> 1 / ***Fever Fill Rate***

Theory: Both hits (hit and release) of an LN gives Fever Score, despite LNs only counting as one note when calculating Song Note Count above.
This would explain a phenomenon where the Fever Bar is filled faster than usual on LN-heavy songs like Chiwawa, Dubstepah and Small Theft Auto.
Therefore, we need to distinguish between a "note" and a "hit".


# Draining Fever

Base Fever Time:
> ***Fever Time*** * **Song Length** / 6

Fever Score drained per second:
> **Song Note Count** * 2 / (***Fever Time*** * **Song Length**)

Fever Score drained per hit:
> AQ * **Song Note Count** / 3

AQ
> 0 if Perfect or Great, 1/?? if Ok, 1/?? if Miss

Theory: Both Miss and Ok remove a certain percentage of the full Fever bar (described above as AQ), maybe 1/10th for a Miss, for example. Further research needed!


# Accuracy

Hit windows:
> (base) Perfect - +40/-20, Great - +190/-95

> (+80) Perfect - ?, Great - ?

Accuracy percentage:
> ( 200 * **Perfect Amount** + 150 * **Great Amount** + 100 * **Ok Amount** + 0 * **Miss Amount** ) / ( 200 * **Hit Count** )

> **Raw Score** / **Maximum Raw Score**
