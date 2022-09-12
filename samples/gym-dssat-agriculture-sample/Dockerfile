FROM gym-dssat:debian-bullseye as gym-dssat

USER 0

# Install libraries and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    zlib1g-dev \
    swig\
    git

# Set up the simulator
WORKDIR /src

# Copy simulator files to /src
COPY . /src

# Update this number to force a rebuild when the gym package changes.
ARG CACHE_VERSION=6

# Install simulator dependencies
RUN pip3 install -r requirements.txt

#USER gymusr

# Override the base run_env.py
COPY run_env.py /opt/gym_dssat_pdi/samples/run_env.py
CMD ["python /opt/gym_dssat_pdi/samples/run_env.py"]

# # This will be the command to run the simulator
#CMD ["python3", "gym-dssat-simulator.py", "--headless"]
CMD ["python /src/gym-dssat-simulator.py"]
