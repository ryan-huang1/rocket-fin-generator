FROM python:3.9-slim

WORKDIR /app

COPY fin_svg_server.py .

RUN pip install flask

# Explicitly expose the port
EXPOSE 5000

# Use the updated Flask configuration
CMD ["python", "fin_svg_server.py"] 