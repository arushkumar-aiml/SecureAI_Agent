# =====================================
# SMART RISK FUSION
# =====================================

def fuse_risk(audio, ocr, clip):

    # weighted fusion (better than sum)
    score = int(
        0.5 * audio +
        0.3 * ocr +
        0.2 * clip
    )

    if score < 40:
        decision = "SAFE"
    elif score < 70:
        decision = "FLAGGED"
    else:
        decision = "BLOCKED"

    return {
        "risk_score": score,
        "decision": decision
    }

