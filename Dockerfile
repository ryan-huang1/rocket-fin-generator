FROM python:3.9-slim

WORKDIR /app

COPY fin_svg_server.py .

RUN pip install flask

EXPOSE 5000

CMD ["python", "fin_svg_server.py"] 