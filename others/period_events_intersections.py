import datetime

start_date = datetime.date(2025, 1, 1)
end_date = datetime.date(2025, 1, 8)

count_stopped = 0
for day in range((end_date - start_date).days + 1):
    if (start_date + datetime.timedelta(days=day)).weekday() == 1:
        count_stopped += 1

print(count_stopped)

