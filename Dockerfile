FROM python:3

RUN mkdir /home/dev/ && mkdir /home/dev/code/

WORKDIR /home/dev/code/

#ENV http_proxy http://147.215.1.189:3128
#ENV https_proxy http://147.215.1.189:3128

COPY . .
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

CMD [ "jupyter", "notebook" ]
