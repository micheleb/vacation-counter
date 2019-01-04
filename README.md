# vacation-counter
A script to count vacation days using an iCal calendar

# what this script does
It takes an .ics file that you pass to it as arg on the command line, and
counts working days (meaning, Monday to Friday, national holidays are not
excluded) in event ranges labeled with some search string (by default, it looks
for events labeled `michele off`, as that's what I set for myself on my team's
Google calendar).

It also shows you overlapping ranges matching another search string (by default
it's `holiday`), so you can semi-manually check for national holidays and the
like.

# running
Create a virtualenv (optional), then run:

    pip install -r requirements.txt
    python vacation-counter.py /path/to/my/ics/file

# pro-tip
To export an .ics file from Google Calendar, go to Settings/Import & export.
