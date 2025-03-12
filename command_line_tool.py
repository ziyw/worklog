'''
THIS FILE IS NOT IN USE AT THE MOMENT
'''

def read_command_line(args):
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