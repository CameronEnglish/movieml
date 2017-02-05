import json
import csv

with open('result_frame_raiders.json') as f:
    data = json.load(f)

frames = [
    frame
    for fragment in data['fragments']
    for frame in (fragment['events'] if 'events' in fragment else [[] for _ in range(round(data['framerate'] * fragment['duration'] / data['timescale']))])
]

max_id = max([event['id'] for frame in frames for event in frame])

scores = [[] for _ in range(max_id + 1)]
for frame in frames:
    sorted_events = sorted(frame, key=lambda k: k['id'])
    j = 0
    for i in range(max_id + 1):
        if j < len(sorted_events) and sorted_events[j]['id'] == i:
            scores[i].append(sorted_events[j]['scores'])
            j += 1
        else:
            scores[i].append(None)

for i in range(max_id + 1):
    with open('result_raiders_{}.csv'.format(i), 'w') as f:
        fieldnames = ['frame', 'surprise', 'fear', 'disgust', 'anger', 'contempt', 'happiness', 'neutral', 'sadness']
        blank = { key: "" for key in fieldnames }
        writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='unix')

        writer.writeheader()
        for i, score in enumerate(scores[i]):
            if score is None:
                blank['frame'] = i
                writer.writerow(blank)
            else:
                score['frame'] = i
                writer.writerow(score)
