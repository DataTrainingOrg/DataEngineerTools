FROM python:3

RUN mkdir /home/dev/ && mkdir /home/dev/code/

WORKDIR /home/dev/code/

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "/bin/bash" ]
