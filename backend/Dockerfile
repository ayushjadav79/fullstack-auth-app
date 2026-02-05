# 1. Use an official Python image as a starting point
FROM python:3.10-slim

# 2. Set the working directory inside container
WORKDIR /app

# 3. Copy only the requirements file first
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the backend code
COPY . .

# 6. Command to start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]