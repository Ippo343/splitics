#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
This script takes an .ics calendar file and splits it into smaller files.
You can split the file based on the file size, number of events, or both.
It's useful when you want to migrate a calendar into Google Calendar,
since it will only accept files that are smaller than about 1MB.
"""

# This script is full of globals. Please don't program like this.
# It's 11PM on a saturday. I'll come back and refactor it, I swear [1]

import argparse
import io
import re
import sys


def parse_size(s):
    """
    Parses a human-readable size to a number of bytes.
    Only accepts kilos and megs because seriously, there's no point in other units (not for ics files anyway).
    """
    sizes = {
        'K': 1024,
        'M': 1024 * 1024,
    }

    pattern = re.compile('^(\d+)([Kk]|M)[Bb]?$')
    match = pattern.match(s)
    if not match:
        raise ValueError("Cannot understand size specification {}".format(s))

    v, u = match.groups()
    return int(v) * sizes[u.upper()]


BEGIN_CALENDAR = "BEGIN:VCALENDAR\n"
END_CALENDAR = "END:VCALENDAR\n"
END_EVENT = "END:VEVENT"


def dump():
    """
    Dumps the current stream to file.
    """
    with open("{}.{}.ics".format(args.input.name, file_count), "w", encoding=args.encoding) as outfile:
        outfile.write(stream.getvalue())


if __name__ == '__main__':

    # region Setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'), help='The .ics input file')
    parser.add_argument('-s', '--size', type=str, default='1M', help='Maximum size of each file (approximate)')
    parser.add_argument('-n', '--number', type=int, default=float('inf'), help='Maximum number of events in each file')
    parser.add_argument('-e', '--encoding', type=str, default='utf8', help='Encoding of the input file')

    args = parser.parse_args(sys.argv[1:])
    try:
        args.size = parse_size(args.size)
    except ValueError as e:
        print(e)
        sys.exit(1)
    # endregion

    stream = io.StringIO()
    size, event_count, file_count = 0, 0, 0

    for line in args.input:

        # Copy the file line by line, tracking the current file size
        stream.write(line)
        size += len(line)

        if line.startswith(END_EVENT):
            event_count += 1
            if size > args.size or event_count >= args.number:
                # Reached a rollover point: write the calendar's end and flush the file.
                stream.write(END_CALENDAR)

                dump()

                # Reset the stream (adding a new header for the calendar)
                stream = io.StringIO()
                stream.write(BEGIN_CALENDAR)
                size, event_count = 0, 0

                file_count += 1
            else:
                continue

    else:
        # Finished the file, nothing to do except flushing
        pass

    # Flush the last part of the file. There's no need to add the calendar's end (the file already has it).
    dump()


# [1] Never gonna happen
