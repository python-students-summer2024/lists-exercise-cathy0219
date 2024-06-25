import datetime
import os

def assess_mood():
    mood_map = {
        'happy': 2,
        'relaxed': 1,
        'apathetic': 0,
        'sad': -1,
        'angry': -2
    }
    
    def get_mood():
        while True:
            mood = input("Enter your mood (happy, relaxed, apathetic, sad, angry): ").strip().lower()
            if mood in mood_map:
                return mood_map[mood]
            print("Invalid mood. Please enter a valid mood.")

    date_today = str(datetime.date.today())
    data_dir = 'data'
    mood_file_path = os.path.join(data_dir, 'mood_diary.txt')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if os.path.exists(mood_file_path):
        file = open(mood_file_path, 'r')
        lines = file.readlines()
        file.close()
        for line in lines:
            if line.startswith(date_today):
                print("Sorry, you have already entered your mood today.")
                return

    mood_value = get_mood()
    
    file = open(mood_file_path, 'a')
    file.write(f"{date_today},{mood_value}\n")
    file.close()

    diagnose_mood(mood_file_path, mood_map)

def diagnose_mood(mood_file_path, mood_map):
    file = open(mood_file_path, 'r')
    lines = file.readlines()
    file.close()
    
    if len(lines) < 7:
        return
    
    recent_moods = [int(line.strip().split(',')[1]) for line in lines[-7:]]
    mood_count = {
        'happy': 0,
        'relaxed': 0,
        'apathetic': 0,
        'sad': 0,
        'angry': 0
    }
    
    for mood_value in recent_moods:
        for mood, value in mood_map.items():
            if mood_value == value:
                mood_count[mood] += 1
    
    if mood_count['happy'] >= 5:
        diagnosis = 'manic'
    elif mood_count['sad'] >= 4:
        diagnosis = 'depressive'
    elif mood_count['apathetic'] >= 6:
        diagnosis = 'schizoid'
    else:
        average_mood_value = round(sum(recent_moods) / 7)
        diagnosis = next(key for key, value in mood_map.items() if value == average_mood_value)

    print(f"Your diagnosis: {diagnosis}!")
