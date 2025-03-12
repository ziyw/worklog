"""
Simple command line tool for myself to log my daily time consumption:
run the following command to use:
python3 worklog.py start activity-name: this will create a new entry in the log file
python3 worklog.py show: this will show current entry or previous entry
python3 worklog.py done: this will end current entry
"""

import os
import sys
from datetime import datetime

HEADER_LINE = 'date,activity,start_time,end_time\n'
DEFAULT_ACTIVITY = 'working'

## Utility Functions   
def get_last_line(log_file_name) -> str: 
  with open(log_file_name, 'rb') as f:
    try:
      f.seek(-2, os.SEEK_END)
      while f.read(1) != b'\n':
        f.seek(-2, os.SEEK_CUR)
    except OSError:
      f.seek(0)
    last_line = f.readline().decode()
    return last_line
  return 'can not read file'

def append_to_file(log_file_name, new_str):
  with open(log_file_name, 'a') as file:
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

class LogManager:
  def __init__(self, log_file_name):
    self.log_file_name = log_file_name
    if not os.path.exists(log_file_name):
      with open(log_file_name, 'w') as file:
        file.write(HEADER_LINE)
  
  def start_new_log(self, activity=DEFAULT_ACTIVITY) -> bool:
    last_entry = self.get_last_entry()
    
    # last entry is header, create new entry directly
    if last_entry is None:
      new_entry = LogEntry.from_cur_time(activity, datetime.now())
      append_to_file(self.log_file_name, new_entry.to_string())
      return True
    
    if last_entry.is_active:
      print(f'Error: existing on-going activity: {self.last_entry.to_string()}')
      return False;

    new_entry = LogEntry.from_cur_time(activity, datetime.now())
    append_to_file(self.log_file_name, new_entry.to_string())
    return True
  
  def stop_cur_log(self) -> bool:
    last_entry = self.get_last_entry()
    if last_entry is None or not last_entry.is_active:
      return False
    
    end_time = get_time(datetime.now())
    append_to_file(self.log_file_name, f',{end_time}\n')
    return True

  def get_last_entry(self) -> LogEntry:
    last_line = get_last_line(self.log_file_name)
    if last_line == HEADER_LINE:
      return None
    return LogEntry.from_entry_line(last_line)