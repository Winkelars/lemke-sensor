- Das [Dashboard](http://raspberrypi:8086/signin?returnTo=/orgs/82b1167a07bfad1c/dashboards/0e724adf9ee09000) aktualisiert sich über diesen Link automatisch alle paar Sekunden für Monitoring. 
- Todo 1: Die Liste der Subscriber muss persistent gemacht werden
- Todo 2: Es sollten Ports und URLs (auch 'localhost') am besten über Umgebungsvariablen, und nicht hard-coded implementiert werden

- Todo 3: (größter Aufwand): Es sollte bei mehreren erkannten MAC-Adressen für jede Adresse ein Bucket in Influxdb erstellt werden, sodass mehrere Sensoren gelesen werden können 
- Todo 3,5: Man sollte dann auch bei Telegram aussuchen können, welchen Sensor man subscribed.

- Todo 4: Variable 'Threshholds' einbauen, bei denen alternative Subscriptions andere Nachrichten auslösen wie "Warnung, Luftfeuchtigkeit zu niedrig!"


