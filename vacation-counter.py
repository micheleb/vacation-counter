import arrow
from ics import Calendar
import sys

event_filter = 'michele off'  # search str in the iCal event name (count these)
overlap_filter = 'holiday'    # search str for events to check for overlaps

if len(sys.argv) != 2:
    print('Usage:')
    print('  python vacation-counter.py /path/to/ics/file')
    sys.exit(1)

with open(sys.argv[1], 'r') as file_in:
    content = file_in.read()

# .replace('ACTION:NONE', 'ACTION:AUDIO'))
c = Calendar(content)
m = [x for x in c.events if x.name.lower().find(event_filter) > -1]

for m_off in sorted(m, key=lambda e: e.begin):
    working_dates = [d for d in arrow.Arrow.range('day', m_off.begin, m_off.end)
                     if d.weekday() < 5]
    working_days = len(working_dates)
    hours = 8

    if working_days == 1:
        hours = len(arrow.Arrow.range('hour', m_off.begin, m_off.end))
        working_days = 0.5 if (hours / 8) < 1 else 1
    else:
        if m_off.begin.hour >= 12:
            working_days -= 0.5

        if m_off.end.day == working_dates[-1].day:
            if m_off.end.hour == 0:
                working_days -= 1
            elif m_off.end.hour <= 12:
                working_days -= 0.5

    cross = [x for x in c.events
             if x.name.lower().find(overlap_filter) > -1
             and x.begin <= m_off.end and x.end >= m_off.begin]

    report = '{} - [{} - {}] ({} working day{}{})'\
        .format(m_off.name, m_off.begin, m_off.end, working_days,
                's' if working_days != 1 else '',
                '' if hours >= 8 else ' - {} hours'.format(hours))
    if cross:
        print()
        print('*** found holiday overlap (check manually) ***********************')
        print(report)
        print('overlapping with: {}'.format(cross))
        print('******************************************************************\n')
    else:
        print(report)
