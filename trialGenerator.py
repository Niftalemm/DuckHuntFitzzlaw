import random

objectTypes = [
    ['L', 'S', 'S'],
    ['L', 'S', 'M'],
    ['L', 'S', 'L'],
    ['L', 'M', 'S'],
    ['L', 'M', 'M'],
    ['L', 'M', 'L'],
    ['L', 'L', 'S'],
    ['L', 'L', 'M'],
    ['L', 'L', 'L'],
    ['R', 'S', 'S'],
    ['R', 'S', 'M'],
    ['R', 'S', 'L'],
    ['R', 'M', 'S'],
    ['R', 'M', 'M'],
    ['R', 'M', 'L'],
    ['R', 'L', 'S'],
    ['R', 'L', 'M'],
    ['R', 'L', 'L'],
]

def createTrials():
    repeats = 10  # 10 makes 180 trials. 
    trials = []
    for _ in range(repeats):
        trials.extend([item.copy() for item in objectTypes])
    random.shuffle(trials)
    return trials
