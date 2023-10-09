This tool calculates the optimal combination of gear,  upgrades and minis required to theoretically maximize score from any given Robeats song.

Most of these formulas have been formulated through experimentation and some guessing.
Expect that some may be incorrect.

# Basics

Robeats is a vertically scrolling rhythm game with RPG mechanics.

## Gear and stats



There are six slots available for you to equip gear on


# Scoring

## Vocabulary

*POINTS* - You gain this for hitting notes.

*SCORE* - The total amount of points gained in a song.
This is what this tool attempts to maximize.

*NOTE* - One singular instance of a note.
It can be a single note which merely requires pressing it at the right time, or an LN (long note) which you have to hold and release.

*HIT* - An action that gives you points and increases score.
Single notes have one hit (press), LNs have two hits (press *and* release).

The distinction between a note and a hit is *very* important, and it has some funky consequences in Fever calculation as we will see later.

## Raw points

Raw points are purely the points gained from accuracy and color power, ignoring all multipliers.
The amount of raw points gained per hit is:

$$Raw Points = Color Points + \begin{cases}
    Perfect Points &\text{if Perfect} \\
    150 &\text{if Great} \\
    100 &\text{if Ok}
\end{cases}$$

Color Points are calculated using the current song's Color.
With no gear, it is equal to 0.

$$Color Points = Primary Color Power * 2 + Secondary Color Power$$

## Multipliers

The Raw Points are multiplied with two multipliers, Current Combo Multiplier and Current Fever Multiplier (more on them later).
This becomes the final point value added to the score.

$$Points = Raw Points * Current Combo Multiplier * Current Fever Multiplier$$

Keep in mind Current Combo/Fever Multiplier are distinct from the actual stats, Combo/Fever Multiplier!
The stats can be thought of as "Max Combo/Fever Multiplier" to avoid confusion.


# Combo

$$Current Combo Multiplier = 1 + min(\frac{Combo}{100}, 1) * (Combo Multiplier - 1)$$

Combo is updated (that is, increased by one) *before* points are given for hitting.


# Fever

While playing a song while making no mistakes, the Fever Bar will slowly fill up.
Once it's full, a Fever activates and an additional multiplier is added to every points calculation.
We can represent this mathematically:

$$Current Fever Multiplier = \begin{cases}
    Fever Multiplier &\text{if Fever active} \\
    1 &\text{otherwise}
\end{cases}$$

## Building Fever

In order to fill the Fever Bar, a certain amount of Fever Score must be generated.
Every *hit* generates Fever Score based on accuracy:

$$Fever Score = \begin{cases}
    1 &\text{if Perfect} \\
    1/2 &\text{if Great} \\
    0 &\text{if Ok}
\end{cases}$$

The amount of Fever Score required for a Fever is calculated as such:

$$Max Fever Score = \frac{Song Note Count}{3} * Fever Fill Rate$$

Notice how Max Fever Score is calculated using the amount of *notes*, despite Fever Score being generated on *hits*.
This explains a phenomenon where the Fever Bar is filled faster than usual on LN-heavy songs like Chiwawa and Small Theft Auto.
As an LN counts as two hits, but only one note, the Max Fever Score ends up being very low compared to the amount of hits when there are many LNs.

## Draining Fever

$$Effective Fever Time = Fever Time * \frac{Song Length}{6}$$

Fever Score drained per second:

$$Song Note Count * \frac{2}{Fever Time * Song Length}$$

Fever Score is also drained on Ok's and Misses as a one-time value.

$$DrainedFeverScore = Max Fever Score * \begin{cases}
    1/12 &\text{if Ok} \\
    1/6 &\text{if Miss}
\end{cases}$$

**NOTE**: Further research is needed here. The exact proportions drained are currently rough estimates.


# Accuracy

Hit windows:
> (base) Perfect - +40/-20, Great - +190/-95

> (+80) Perfect - ?, Great - ?

Accuracy percentage:
> ( 200 * **Perfect Amount** + 150 * **Great Amount** + 100 * **Ok Amount** + 0 * **Miss Amount** ) / ( 200 * **Hit Count** )

> **Raw Score** / **Maximum Raw Score**


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
