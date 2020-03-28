# pygame sound objects
# starting health +3
# map something to direction?

rtms_1 = "/users/orlando1723/Documents/sonic_pi/pygame_samples/rtms1.wav"
rtms_2 = "/users/orlando1723/Documents/sonic_pi/pygame_samples/rtms2.wav"
rtms_3 = "/users/orlando1723/Documents/sonic_pi/pygame_samples/rtms3.wav"
guitar_scrape = "/users/orlando1723/Documents/sonic_pi/pygame_samples/guitar_scrape.wav"
guitar_M3 = "/users/orlando1723/Documents/sonic_pi/pygame_samples/guitar_M3.wav"
guitar_microtonal = "/users/orlando1723/Documents/sonic_pi/pygame_samples/guitar_microtonal.wav"
seashells = "/users/orlando1723/Documents/sonic_pi/pygame_samples/seashells.wav"

# starting rate- 0.25, amp: 1.5 w/ reverb and pitch shift
# hit obstacles- rate: 0.5

live_loop :woosh do
  with_fx :reverb, pre_amp: 4, mix: 0.5, room: 0.6 do
    with_fx :pitch_shift, pitch: 1, pitch_slide: 14 do |s|
      control s, pitch: 2
      a = sync "/osc*/trigger/rtms_3"
      sample rtms_3, rate: 0.25, amp: 1.5, attack: 0.5, release: 1 if a[0] == 1
      sleep 5
      stop if a[0] == 0
    end
  end
end

# starting- rate: 0.25 w/ reverb and slicer
# hit obstacles- phase: 0.75, reverb- mix: 0.8, room: 0.9
# +9 health- stop loop

live_loop :rtms3 do
  with_fx :reverb, pre_amp: 2, mix: 0.7, room: 0.8 do
    with_fx :slicer, phase: 1.5 do
      use_real_time
      b = sync "/osc*/trigger/rtms_3_1"
      sample rtms_3, rate: 0.25 if b[0] == 1
      sleep 8
      stop if b[0] == 0
    end
  end
end

# starting- rate: 0.05, lpf: 50, amp: 2
# hit obstacles- change lpf value to 70
# +10 health- stop loop

live_loop :rtms1 do
  with_fx :reverb, pre_amp: 2, mix: 0.7, room: 0.8 do
    use_real_time
    c = sync "/osc*/trigger/rtms_1"
    sample rtms_1, rate: 0.05, lpf: 60, start: 0.25, finish: 0.37 if c[0] == 1
    sleep 6
    stop if c[0] == 0
  end
end

# +4 health- rate: 0.95, amp: 0.4, hpf: 95
# maybe take down hpf at some point? or rate?
# +7 health- stop loop

live_loop :rtms2 do
  with_fx :reverb, mix: 0.7 do
    with_fx :whammy, transpose: 0.5, grainsize: 0.5 do
      use_real_time
      d = sync "/osc*/trigger/rtms_2"
      sample rtms_2, rate: 0.95, amp: 0.4, hpf: 95 if d[0] == 1
      sleep 6
      stop if d[0] == 0
    end
  end
end

# +5 health- rate: 0.98, finish: 0.11
# +6 health- rate: 0.97, sleep: 0.3
# +7 health- rate: 0.96, sleep: 0.35
# +8 health- stop loop

with_fx :reverb, mix: 0.5, room: 0.4 do
  live_loop :ring do
    with_fx :pitch_shift, pitch: 23 do
      e = sync "/osc*/trigger/ring"
      sample guitar_microtonal, rate: e[1], finish: 0.11, attack: 0.1, release: 0.4, amp: 0.7 if e[0] == 1
      sleep e[2]
      stop if e[0] == 0
    end
  end
end

# +6 health- guitar scrape (once only)

with_fx :reverb, mix: 0.75, room: 0.75 do
  with_fx :echo, decay: 3 do
    sync "/osc*/trigger/guitar_scrape"
    sample guitar_scrape, amp: 0.7, attack: 3
  end
end

# +8 health- start loop
# - whammy mix: 0.2, 0.3, 0.35 transpose: -0.5, -1, -2
# +13 health- stop loop?


with_fx :reverb, mix: 0.7, room: 0.7 do
  with_fx :echo, mix: 0.3, phase: 0.25 do
    live_loop :M3 do
      use_real_time
      f = sync "/osc*/trigger/M3"
      with_fx :whammy, mix: f[1], transpose: f[2] do
        sample guitar_M3, hpf: 30, amp: 0.8, release: 1 if f[0] == 1
        sleep 6
        stop if f[0] == 0
      end
    end
  end
end

# +9 health- start loop
# whammy transpose: -0.5, -1, -2 rate: 0.98, 0.97, 0.96 lpf: 100, 90, 85
# +13 health- stop loop

with_fx :reverb, mix: 0.5, room: 0.6 do
  with_fx :whammy, mix: 0.3, transpose: -0.5 do
    live_loop :twinkle do
      g = sync "/osc*/trigger/twinkle"
      sample guitar_microtonal, rate: 0.98, amp: 0.9, lpf: 100 if g[0] == 1
      sleep 8
      stop if g[0] == 0
    end
  end
end

# +12 health- start echo mix: 0.4, phase: 0.25
# - echo mix: 0.7, phase: 0.1, notes_quarter
# add woosh?

with_fx :reverb, mix: 1, room: 1 do
  with_fx :echo, mix: 0.4, phase: 0.25 do
    live_loop :melody do
      h = sync "/osc*/trigger/melody"
      notes = (ring 84.8, :r, 83, 80.9, 79.1, :r, :r, 75.8, 74, 73.2, :r, :r, 70.9, 69.2, 67, :r, :r, :r)
      notes_quarter = (ring 84.3, :r, 82.5, 80.4, 78.6, :r, :r, 75.3, 73.5, 72.7, :r, :r, 70.4, 68.7, 66.5, :r, :r, :r)
      use_synth :pretty_bell
      play notes.tick, amp: 0.1, pan: rrand(-1, 1) if h[0] == 1
      play notes.tick, amp: 0.1, pan: rrand(-1, 1) if h[0] == 2
      sleep 0.5
      stop if h[0] == 0
    end
  end
end

# +11 health- slowly bring in (low cutoff?)
# +12 health- raise cutoff?

with_fx :reverb, mix: 0.7, room: 0.6 do
  with_fx :wobble, mix: 0.3, phase: 0.25, res: 0.4, wave: 3 do
    live_loop :harmony do
      j = sync "/osc*/trigger/harmony"
      use_synth :mod_fm
      har_1 = play [81.2, 85.2, 87.8], attack: 2, release: 2, amp: 0.75, cutoff: 70, mod_range: 4, mod_phase: 0.75, mod_phase_slide: 3, pan: 0.5 if j[0] == 1
      control har_1, mod_phase: 0.25
      sleep 4
      har_2 = play [77, 81.2, 84.3], attack: 3, release: 2, amp: 0.75, cutoff: 70, mod_range: 4, mod_phase: 0.75, mod_phase_slide: 4, pan: -0.5 if j[0] == 1
      control har_2, mod_phase: 0.25
      sleep 5
      stop if j[0] == 0
    end
  end
end

# +10 health- start

live_loop :bass do
  k = sync "/osc*/trigger/bass"
  use_synth :subpulse
  play :cs4, amp: 0.1, attack: 2, sustain: 2, release: 1, cutoff: 50 if k[0] == 1
  bass_1 = play :a2, amp: 0.2, attack: 1, sustain: 3, release: 1, cutoff: 40, cutoff_slide: 6 if k[0] == 1
  control bass_1, cutoff: 60
  sleep 6
  play :a3, amp: 0.1, attack: 2, sustain: 2, release: 1, cutoff: 50 if k[0] == 1
  bass_2 = play :f2, amp: 0.2, attack: 1, sustain: 3, release: 1, cutoff: 40, cutoff_slide: 20 if k[0] == 1
  control bass_2, cutoff: 60
  sleep 7
  stop if k[0] == 0
end

# +13 health start

live_loop :seashells do
  m = sync "/osc*/trigger/seashells"
  sample seashells, amp: 0.8, attack: 1, release: 1 if m[0] == 1
  sleep 15
  stop if m[0] == 0
end
