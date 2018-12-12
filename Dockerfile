FROM python:3.6 

RUN mkdir /home/dev/ && mkdir /home/dev/code/

WORKDIR /home/dev/code/

ENV http_proxy http://147.215.1.189:3128
ENV https_proxy http://147.215.1.189:3128

COPY . .
RUN  pip install --upgrade pip &&  pip install pipenv && pipenv install --skip-lock

#CMD ["pipenv", "run",  "jupyter", "notebook" ]
CMD ["/bin/bash"]
