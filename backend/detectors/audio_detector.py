import os

def detect_audio_risk(path):
    """
    NOTE: This is a lightweight file-size sanity check, NOT real deepfake/voice-clone
    detection. True audio deepfake detection requires a trained acoustic model
    (spectral analysis, voice biometrics) which this version does not include.
    Flag this honestly in any customer-facing copy until a real model is integrated.
    """
    size = os.path.getsize(path) / (1024 * 1024)
    if size > 7:
        return 85
    elif size > 3:
        return 55
    else:
        return 15