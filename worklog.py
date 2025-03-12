from menu import WorkLogBarApp
from manager import LogManager

if __name__ == "__main__":
  manager = LogManager("/Users/ziyan/code/worklog.csv")
  WorkLogBarApp(manager).run()