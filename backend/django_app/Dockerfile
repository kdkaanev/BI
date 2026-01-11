FROM python:3.11-slim

# Enviroment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


#Working directory
WORKDIR /app
# Copy project
COPY . /app/

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/bi_dashboard
# Collect static files
RUN cd bi_dashboard && python manage.py collectstatic --noinput
COPY bi_dashboard/ /app/bi_dashboard/
EXPOSE 8000
CMD ["gunicorn", "bi_dashboard.wsgi:application", "--bind", "0.0.0.0:8000"]




