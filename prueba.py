from datetime import datetime, timedelta

from datetime import datetime, timedelta

def get_nearest_sunday_saturday(date):
    if date.weekday() == 6:  # If today is Sunday
        past_sunday = date  # Past Sunday is a week ago
        # Calculate the next Saturday by adding 6 days to the past Sunday
        next_saturday = past_sunday + timedelta(days=6)
    else:
        # Calculate the past Sunday by going back to the last Sunday
        past_sunday = date - timedelta(days=date.weekday() + 1)
        # Calculate the next Saturday by adding the remaining days of the current week and then advancing a week
        next_saturday = date + timedelta(days=(5 - date.weekday()))

    return past_sunday, next_saturday
# Obtener la fecha actual
fecha_actual = datetime(day=1, month=3, year=2024) # Solo necesitamos la fecha, no la hora
print(fecha_actual)
print(get_nearest_sunday_saturday(fecha_actual))