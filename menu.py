import rumps
from manager import LogManager
from manager import DEFAULT_ACTIVITY

class WorkLogBarApp(rumps.App):
    def __init__(self, log_manager):
        super(WorkLogBarApp, self).__init__("work")
        self.menu = ["start", "stop", "show"]
        self.quit_button = None
        self.start_button = self.menu['start']
        self.stop_button = self.menu['stop']
        self.log_manager = log_manager
    
    @rumps.clicked("start")
    def start_log(self, _):
      self.toggle(self.start_button, None)
      self.toggle(self.stop_button, self.stop_log)
      self.title = DEFAULT_ACTIVITY
      self.log_manager.start_new_log()
    
    @rumps.clicked("stop")
    def stop_log(self, _):
      self.toggle(self.start_button, self.start_log)
      self.toggle(self.stop_button,None) 
      self.title = 'work'
      self.log_manager.stop_cur_log()

    @rumps.clicked("show")
    def show_current_entry(self,_):
      last_entry = self.log_manager.get_last_entry()
      if last_entry is None:
        rumps.notification("WorkLog", "No Entry", "Nothing is going on")
        return
      
      if last_entry.is_active:
       rumps.notification("WorkLog", "ON GOING", last_entry.to_string())
       return
       
      rumps.notification("WorkLog", "Last entry:", last_entry.to_string())
      return
    
    @rumps.clicked("quit")
    def quit(self, _):
      last_entry = self.log_manager.get_last_entry()
      if last_entry is not None and last_entry.is_active:
        self.log_manager.stop_cur_log()
      rumps.quit_application()
    
    def toggle(self, button, callback_func):
      button.set_callback(callback_func)