from memory import remember
from store import BASE_INCIDENTS, incident_text

for inc in BASE_INCIDENTS:
    remember(incident_text(inc))
    print("Stored:", inc["id"], inc["service"])