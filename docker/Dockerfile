# Use the existing autogen_base_img as the base image
FROM autogen_base_img:latest

# Set environment variables to optimize Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /home/autogen/autogen/myapp

# Copy the requirements.txt file into the container
COPY myapp/requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY myapp/ .

# Set the default command to execute the script
CMD ["python", "main_twoagent.py"]
