#Base image: Using Python 3.9.6 slim variant for a lightweight environment
FROM python:3.9.6-slim

#Set the working directory inside the container
WORKDIR /app

#Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy the rest of the application code
COPY . .

#Ensure the entrypoint script is executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

#Expose Streamlit's default port
EXPOSE 8501

#Define the container's entrypoint
ENTRYPOINT ["./entrypoint.sh"]
