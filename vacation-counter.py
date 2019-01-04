from __future__ import print_function
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

c = Calendar(content.decode('utf-8').replace('ACTION:NONE', 'ACTION:AUDIO'))
m = [x for x in c.events if x.name.lower().find(event_filter) > -1]

for m_off in sorted(m, key=lambda e: e.begin):
    working_days = len(
            [d for d in arrow.Arrow.range('day', m_off.begin, m_off.end)
                if d.weekday() < 5])
    print('{} - [{} - {}] ({} working day{})'
          .format(m_off.name, m_off.begin, m_off.end, working_days,
                  's' if working_days != 1 else ''))
    cross = [x for x in c.events
             if x.name.lower().find(overlap_filter) > -1
             and x.begin <= m_off.end and x.end >= m_off.begin]
    if cross:
        print('OVERLAP: {}\n'.format(cross))
