from argparse import ArgumentParser
from smart_schedule import schedule_notion_to_google

parser = ArgumentParser()

parser.add_argument("--today", action="store_true", help="start scheduling events today")
parser.add_argument("--days", type=int, default=1, help="number of days to schedule events")
parser.add_argument("--reschedule", action="store_true", help="reschedule events if already scheduled")
parser.add_argument("--delete", action="store_true", help="delete events if in calendar, but do not schedule anything.")
parser.add_argument("--force", action="store_true", help="don't ask for confirmation before rescheduling events")

args = parser.parse_args()

if __name__ == "__main__":
    schedule_notion_to_google(args.today, args.days, args.reschedule, args.delete)
