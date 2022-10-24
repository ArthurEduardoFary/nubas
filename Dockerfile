FROM python:3.10
WORKDIR /nubas
COPY requirements.txt /nubas/
RUN pip install -r requirements.txt
COPY . /nubas
CMD python main.py