"""
Simple command line tool for myself to log my daily time consumption:
run the following command to use:
python3 worklog.py start activity-name: this will create a new entry in the log file
python3 worklog.py show: this will show current entry or previous entry
python3 worklog.py done: this will end current entry
"""

import os
from datetime import datetime
import sys

LOG_FILE_NAME = 'worklog.csv'

def main(args):
  last_line = get_last_line(LOG_FILE_NAME)
  last_entry = LogEntry.from_entry_line(last_line)

  if args[1] == 'start':
    if last_entry.is_active:
      print(f'Error: existing on-going activity: {last_entry.to_string()}')
    else:
      new_entry = LogEntry.from_cur_time(args[2], datetime.now())
      append_to_file(LOG_FILE_NAME, new_entry.to_string())
      print(f'Work started: {new_entry.to_string()}')
    return
  
  if args[1] == 'done':
    if last_entry.is_active:
      end_time = get_time(datetime.now())
      append_to_file(LOG_FILE_NAME, f',{end_time}\n')
      last_entry.end_time = end_time
      last_entry.is_active = False
      print(f'DONE: {last_entry.to_string()}')
    else:
     print('No active activity')
    return
    
  if args[1] == 'show':
    if last_entry.is_active:
      print(f'On going activity: {last_entry.to_string()}')
    else:
      print(f'No active entry, Last entry: {last_entry.to_string()}')
    return
  
  print('Unknown command')
  return

def get_last_line(filename) -> str:
  with open(filename, 'rb') as f:
    try:
      f.seek(-2, os.SEEK_END)
      while f.read(1) != b'\n':
        f.seek(-2, os.SEEK_CUR)
    except OSError:
      f.seek(0)
    last_line = f.readline().decode()
    return last_line
  return 'can not read file'

def append_to_file(filename, new_str):
  with open(filename, 'a') as file:
    file.write(new_str)
  return

def get_date(cur_time) -> str:
  return cur_time.strftime("%m/%d/%Y")

def get_time(cur_time) -> str:
  return cur_time.strftime("%H:%M")

class LogEntry(object):
  def __init__(self, date, activity, start_time, end_time, is_active):
    self.date = date
    self.activity = activity
    self.start_time = start_time
    self.end_time = end_time
    self.is_active = is_active
  
  @classmethod
  def from_cur_time(cls, activity, cur_time):
    return cls(get_date(cur_time), activity, get_time(cur_time), '', True)

  @classmethod
  def from_entry_line(cls, entry_line):
    parts = entry_line.split(',')
    if len(parts) > 3:
      return cls(parts[0], parts[1], parts[2], parts[3], False)
    else:
      return cls(parts[0], parts[1], parts[2], '', True)
  
  def to_string(self):
    if self.is_active:
      return f'{self.date},{self.activity},{self.start_time}'
    else:
      return f'{self.date},{self.activity},{self.start_time},{self.end_time}'

if __name__=="__main__":
  main(sys.argv)