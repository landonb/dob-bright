# This file exists within 'dob-bright':
#
#   https://github.com/hotoffthehamster/dob-bright
#
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it  and/or  modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any later version  (GPLv3+).
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or  FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU  General  Public  License  for  more  details.
#
# If you lost the GNU General Public License that ships with this software
# repository (read the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

"""Journal writer output format module."""

from click_hotoffthehamster._compat import term_len

# 2020-06-03: (lb): I tried a plain texttable, which sorta works, except it
# won't work with styling -- the style bleeds to the end of line and from the
# start of the next line if the value is cell-wrapped; and also other columns'
# cell-wrapped value don't align on rows without something styled, because the
# width is not computed properly.
# - I cannot think of any advantage to using the table library, other than
#   aligning columns or enforcing width constraints, neither of which matter
#   to the Journal format. So use LineWriter and do what little special
#   formatting there is on output in this writer class.
# - To test with texttable, derive from TableWriter and use the plain-esque
#   table format:
#       import TableWriter
#       ...
#       class JournalWriter(TableWriter):
#           def __init__(self, *args, **kwarg):
#               kwargs['output_format'] = 'texttable_borderless_headerless'
#               super(JournalWriter, self).__init__(*args, **kwargs)
#   except then tabulate_results() needs to do the blank line section
#   injection and first column value scrubbing that makes Journal special.

from .line_writer import LineWriter

__all__ = (
    'JournalWriter',
)


class JournalWriter(LineWriter):
    def __init__(self, *args, **kwargs):
        super(JournalWriter, self).__init__(*args, **kwargs)

    def write_report(self, table, headers):
        self.curr_section = None
        return super(JournalWriter, self).write_report(table, headers)

    def _write_result(self, row, columns):
        line = ''
        next_section = self.curr_section
        if self.curr_section is None or row[0] != self.curr_section:
            next_section = row[0]
            if self.curr_section is not None:
                # Emit a blank row-line.
                self.output_write()
            line += row[0]
        else:
            # Omit the first column value when it's the same as the previous row's.
            # Strip Unicode/ASNI control characters to compute whitespace to fill.
            line += ' ' * term_len(row[0])
        i_remainder = 1

        line += '  ' + '  '.join([str(val) for val in row[i_remainder:]])

        # LATER/2020-06-03: Print formatted text.
        #  from prompt_toolkit import print_formatted_text
        #  print_formatted_text(...)

        self.output_write(line)

        self.curr_section = next_section
