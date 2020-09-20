FROM python:3.7-stretch

# Airflow env
ENV AIRFLOW_HOME=/usr/local/bin

# Define en_US
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

# Copy the working directory in to image
ADD . /usr/local/airflow

# Set working directory
WORKDIR "/usr/local/airflow"

# Install pyton requirements
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:$AIRFLOW_HOME

EXPOSE 8080

RUN chmod u+x entrypoint.sh

ENTRYPOINT ["/usr/local/airflow/entrypoint.sh"]
CMD ["webserver"]
