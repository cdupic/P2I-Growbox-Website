select *
from Sensors
where type in ('temperature', 'soil_humidity', 'air_humidity', 'light', 'O2')