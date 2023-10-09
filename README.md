# roscoring
 
IMPORTANT (?) VOCABULARY  
HIT - An action that increases score. Single notes have one hit, long notes have two  
NOTE - One singular instance of a note, can be single or long

Combo is updated (that is, increased by one) BEFORE points are given for hitting.
All formulas may be completely wrong. Especially those involving Song Length and Song Note Count are guesswork.
<This> means it's a gear stat


SCORE

Points per hit:
(AP + CP) * CM * FM
where
AP = <Perfect Points> if Perfect, 150 if Great, 100 if Ok
CP = Primary Color Power * 2 + Secondary Color Power
CM = min( (Combo / 100), 1 ) * (<Combo Multiplier> - 1) + 1
FM = <Fever Multiplier> if Fever

Total score (idealized; assuming no Ok, no Miss, a bunch of other things):
Song Hit Count * (AAP + CP) * ACM * AFM
where
AAP = <Perfect Points> * Perfect Accuracy + 150 * Great Accuracy
CP = Primary Color Power * 2 + Secondary Color Power
ACM = ( (49.5  + Song Hit Count) * (<Combo Multiplier> - 1) + Song Hit Count ) / Song Hit Count
AFM = <Fever Multiplier> * tft - tft + 1
<Fever Multiplier> * tft + 1 * (1 - tft)

tft = percentage time spent in fever
	tff + eft + tff + eft ... until > Song Length
an approximation
	eft / (eft + tff)
adjusted (i think) for imperfect fever timing
	eft / (eft + tff) - 10 / Song Length

This is almost completely guesswork, but comparing with lydiaplayz's fever percentage stats it actually works.
This can't be the actual formula used in Robeats, can it??? The constants are so arbitrary...
eft = effective fever time
	Song Length * (<Fever Time> * 0.16/1.67 + 0.0435)

Miscellaneous formulas
tff = time for fever
	hff / hd
hd = hit density
	Song Hit Count / Song Length
hff = hits for fever
	fsff / fspn - technically ceil(fsff / fspn)
fsff = fever score for fever
	Song Note Count / 3
fspn = fever score per hit
	AFA * FR
AFA = Perfect Accuracy + 0.5 * Great Accuracy
FR = 1 / <Fever Fill Rate>




BUILDING FEVER

Amount of Fever Score required for a Fever:
Song Note Count / 3

Fever Score per hit:
BA * FR
where
BA = 1 if Perfect, 1/2 if Great, 0 if Ok
FR = 1 / <Fever Fill Rate>

Theory: Both hits (hit and release) of an LN gives Fever Score, despite LNs only counting as one note when calculating Song Note Count above. This would explain a phenomenon where the Fever Bar is filled faster than usual on LN-heavy songs like Chiwawa, Dubstepah and Small Theft Auto.
Therefore, we need to distinguish between a "note" and a "hit".


DRAINING FEVER

Base Fever Time:
<Fever Time> * Song Length / 6

Fever Score drained per second:
Song Note Count * 2 / (<Fever Time> * Song Length)

Fever Score drained per hit:
AQ * Song Note Count / 3
where AQ = 0 if Perfect or Great, 1/?? if Ok, 1/?? if Miss

Theory: Both Miss and Ok remove a certain percentage of the full Fever bar (described above as AQ), maybe 1/10th for a Miss, for example. Further research needed!


ACCURACY

Hit windows:
Base ( +0 Perfect Time ): Perfect - +40/-20 (+-30), Great - +190/-95
Bruh ( +80 Perfect Time ): Perfect - 

Accuracy percentage:
( 200 * Perfect Amount + 150 * Great Amount + 100 * OK Amount + 0 * Miss Amount ) / ( 200 * Hit Count )
