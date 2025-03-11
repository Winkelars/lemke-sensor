# 1. Verwende das Go-Image als Basis
FROM cosmtrek/air:latest AS builder

# 2. Setze das Arbeitsverzeichnis
WORKDIR /app

# 4. Kopiere Go Module-Dateien und lade Abhängigkeiten
COPY go.mod ./
RUN go mod download

# 5. Kopiere den gesamten Code
COPY . .

# 6. Starte "air" für Live-Reload während der Entwicklung
CMD ["air"]

