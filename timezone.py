import pytz
from datetime import datetime


# Define the target timezone
target_timezone = pytz.timezone('US/Eastern')
current_time = datetime.now(target_timezone)

# Format the time as a string
formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

# Print the result
print("Current time in Eastern Time Zone:", formatted_time)