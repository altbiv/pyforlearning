import time
import argparse
from datetime import timedelta


def countdown(task_name: str, duration: str):
    try:
        h, m, s = map(int, duration.split(":"))
        total_seconds = h * 3600 + m * 60 + s
    except ValueError:
        print("Invalid time format. Use HH:MM:SS (e.g. 00:25:00)")
        return

    print(f"⏳ Task: {task_name}")
    print(f"Timer set for {duration} (HH:MM:SS)\n")

    while total_seconds > 0:
        td = str(timedelta(seconds=total_seconds))
        print(f"\rTime left: {td}", end="", flush=True)
        time.sleep(1)
        total_seconds -= 1

    print("\r✅ Time’s up! Task complete:", task_name)


def main():
    parser = argparse.ArgumentParser(description="Simple CLI Task Timer")
    parser.add_argument("task", type=str, help="Name of the task")
    parser.add_argument("duration", type=str, help="Timer in HH:MM:SS format (e.g., 00:25:00)")
    args = parser.parse_args()

    countdown(args.task, args.duration)


if __name__ == "__main__":
    main()
