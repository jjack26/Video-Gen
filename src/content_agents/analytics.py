"""Keep explicit human feedback separate from observed performance."""
def record_lesson(feedback: str, metrics: dict | None=None, window: str | None=None) -> dict:
    if not feedback.strip():
        raise ValueError('feedback is required')
    if metrics and not window:
        raise ValueError('metrics require a measurement window')
    return {'human_feedback':feedback,'metrics':metrics or {},'measurement_window':window,'verified_performance':False}
