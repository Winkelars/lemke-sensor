FROM python:3.12
WORKDIR /app
COPY . .
RUN echo "folgende Packages werden installiert:" && cat requirements.txt && pip install --no-cache-dir -r requirements.txt
CMD ["python3", "script.py"]
