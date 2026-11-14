"""
Interactive Gamified 'Earth System Detective Casebook' Missions payload builder.
"""
from typing import Dict, Any, List
from config.missions import DETECTIVE_MISSIONS, JUDGE_EXECUTIVE_TOUR_STEPS


def get_missions_payload() -> Dict[str, List[Dict[str, Any]]]:
    """Return structured Casebook Missions and Judge's 60-Second Executive Tour."""
    return {
        "missions": DETECTIVE_MISSIONS,
        "judge_tour": JUDGE_EXECUTIVE_TOUR_STEPS,
    }
