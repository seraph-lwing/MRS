FROM python:3.9-slim-bullseye

# docker can't find modules if root directory of project not added to python path
ENV PYTHONPATH "${PYTHONPATH}:/home/myapp"


RUN apt-get update && apt-get install -y build-essential

RUN mkdir -p /home/recommendation_system

# busting cache, so that if requirements.txt changes in future, it builds fresh always
ARG CACHEBUST=1
COPY requirements.txt /home/recommendation_system/requirements.txt

WORKDIR /home/recommendation_system

RUN pip install -r requirements.txt
# download nltk ressources
RUN python -c "import nltk; nltk.download('punkt')"

COPY . .

EXPOSE 5000

# change workdir and use flask command to configure port (python app.py also possible)
WORKDIR api

ENTRYPOINT ["flask"]

CMD ["run", "--host", "0.0.0.0"]