import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", help="path to config file")

args = parser.parse_args()

with open(args.config) as f:
    config = json.load(f)

frames_per_beat = round(config['fps'] * config['bps'])
bpf = 1/config['fps']

prompts = config['prompts']
beat_frames = []
beat_seconds = []


last_beat = 0
next_beat = last_beat
time = last_beat

for i in range(config['total_frames']):
    if time >= next_beat:
        beat_frames.append(i)
        beat_seconds.append(i * bpf)
        last_beat = next_beat
        next_beat += config['bps']
    time += bpf

strengths = []

for frame in beat_frames:
    if frame == 0:
        strengths.append(f"{frame}: ({config['high_strength']})")
    else: 
        strengths.append(f"{frame}: ({config['low_strength']}), {frame+1}: ({config['super_high_strength']}), {frame+4}: ({config['high_strength']})")


prompt_dict = {}
for i, f in enumerate(beat_frames):
    if i % config['prompts_per_beat'] == 0:
        prompt_dict[f] = prompts[min(len(prompts)-1, i//config['prompts_per_beat'])]

# load the automatic1111 webui settings file
with open(config['settings_file']) as f:
    data = json.load(f)

with open(config['video_settings_file']) as f:
    video_data = json.load(f)

# update the automatic1111 webui settings file
data['prompts'] = prompt_dict
data['strength_schedule'] = ", ".join(strengths)
data['max_frames'] = config['total_frames']

video_data['fps'] = config['fps']
# save the automatic1111 webui settings file
with open(config['settings_file'], 'w') as f:
    json.dump(data, f, indent=4)

with open(config['video_settings_file'], 'w') as f:
    json.dump(video_data, f, indent=4)

print('updated settings file')