FROM gym-dssat:debian-bullseye as gym-dssat

USER 0

RUN apt install -y git

RUN pip install git+https://github.com/microsoft/bonsai-common

RUN pip install git+https://github.com/microsoft/bonsai-gym@gym-dssat-agriculture-sample

USER gymusr

CMD ["python /opt/gym_dssat_pdi/samples/run_env.py"]
