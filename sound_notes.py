# starting health 3
# max health 10-15
# gameplay around 2-3 mins

# starting samples playing
# rtms_3, rate: 0.25, amp: 1.5 w/ reverb and pitch shift
# live_loop :rtms_3, rate: 0.25 w/ reverb and slicer
# live_loop :rtms_1, rate: 0.05, lpf: 50, amp: 2

# +4 health
# live_loop :rtms_2, rate: 0.95, amp: 0.4, hpf: 95

# +5 health
# live_loop :twinkle2, rate: 0.98, finish: 11

# +6 health
# guitar scrape (once only)
# :twinkle2 slow down a bit?

# +7 health
# :twinkle2 slow down even more
# stop rtms_2

# +8 health
# live_loop :M3
# stop :twinkle2

# +9 health
# live_loop :twinkle
# stop :rtms_3

# +10 health
# stop :rtms_1
# live_loop :bass

# +11 health
# live_loop :harmony slowly bring in

# +12 health
# more harmony
# live_loop :melody

# +13 health
# stop :M3
# stop :twinkle

def makeGameSound():
	if startMode:
		'/trigger/starting_loops'

	if playerObj['health'] <= 4 and > 10:
		'/trigger/rtms_1'
		'/trigger/rtms_2'
	else: # playerObj and rockObj collide
		stop sample

	if playerObj['health'] == 5:
		'/trigger/ring'
	elif playerObj['health'] == 6:
		'/trigger/ring [22.5, 0.96, 0.3]'
	elif playerObj['health'] == 7:
		'/trigger/ring [22, 0.94, 0.35]'
	elif playerObj['health'] < 5 or > 7:
			stop sample

	if playerObj['health'] == 6:
		'trigger/guitar_scrape'

	if playerObj['health'] <= 8 and >13:
		'/trigger/guitar_M3'
	else:
		stop sample

	if playerObj['health'] <= 9 and > 13:
		'/trigger/guitar_microtonal'
	else:
		stop sample

	if playerObj['health'] <= 10:
		'/trigger/bass'

	if playerObj['health'] <= 11:
		'/trigger/harmony [50]' # cutoff

	if playerObj['health'] <= 12:
		'/trigger/harmony [70]' # cutoff
	elif playerObj['health'] > 12:
		'/trigger/harmony [50]'

	if playerObj['health'] <= 12:
		'/trigger/melody'




		





