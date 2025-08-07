from datetime import datetime, timedelta
from homeassistant.components.recorder.util import session_scope
from homeassistant.components.recorder.models import States


def get_average_on_time(hass, entity_id, hour_start=18, hour_end=23, days=7):
    times = []

    with session_scope(hass=hass) as session:
        for i in range(days):
            day = datetime.now() - timedelta(days=i + 1)
            start = day.replace(hour=hour_start, minute=0, second=0, microsecond=0)
            end = day.replace(hour=hour_end, minute=0, second=0, microsecond=0)

            on_states = session.query(States).filter(
                States.entity_id == entity_id,
                States.state == "on",
                States.last_updated >= start,
                States.last_updated <= end
            ).all()

            for state in on_states:
                times.append(state.last_updated.time())

    if not times:
        return None

    avg_minutes = sum([t.hour * 60 + t.minute for t in times]) / len(times)
    avg_hour = int(avg_minutes // 60)
    avg_minute = int(avg_minutes % 60)
    return f"{avg_hour:02d}:{avg_minute:02d}"
