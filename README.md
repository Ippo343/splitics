# splitics

This script takes an .ics calendar file and splits it into smaller files.
You can split the file based on the file size, number of events, or both.

It's useful when you want to migrate a calendar into Google Calendar,
since it will only accept files that are smaller than about 1MB.

## Examples

    python splitics.py my_calendar.ics -s 1M
    python splitics.py my_calendar.ics -n 50
    python splitics.py my_calendar.ics -s 500k -n 20

