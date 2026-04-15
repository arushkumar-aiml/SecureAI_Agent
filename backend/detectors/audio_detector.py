import os
def detect_audio_risk(path):
    size=os.path.getsize(path)/(1024*1024)
    if size > 7:
        return 85
    elif size > 3:
        return 55
    else:
        return 15