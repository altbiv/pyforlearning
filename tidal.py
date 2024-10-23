import csv
from collections import defaultdict

def calculate_tidal_height_from_csv(file_name):
    daily_averages = {}
    monthly_totals = defaultdict(list)

    with open(file_name, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            date = row['Date']
            value1 = float(row['1st value'])
            value2 = float(row['2nd value'])
            value3 = float(row['3rd value'])
            value4 = row.get('4th value', '')

            if value4 == '':
                value4 = value2
            else:
                value4 = float(value4)

            values = [value1, value2, value3, value4]
            daily_average = sum(values) / len(values)

            daily_averages[date] = daily_average

            month = date.split('/')[1]
            monthly_totals[month].append(daily_average)

    monthly_averages = {month: sum(averages) / len(averages) for month, averages in monthly_totals.items()}

    overall_average = sum(sum(averages) for averages in monthly_totals.values()) / sum(len(averages) for averages in monthly_totals.values())

    return daily_averages, monthly_averages, overall_average

file_name = "paradip.csv"  
daily_averages, monthly_averages, overall_average = calculate_tidal_height_from_csv(file_name)

print("Daily Averages:")
for date, avg in daily_averages.items():
    print(f"{date}: {avg:.2f} m")

print("\nMonthly Averages:")
for month, avg in monthly_averages.items():
    print(f"Month {month}: {avg:.2f} m")

print(f"\nOverall Average Tidal Height: {overall_average:.2f} m")
