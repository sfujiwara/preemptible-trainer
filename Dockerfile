FROM tensorflow/tensorflow:2.0.0rc0-gpu-py3

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY trainer /app/trainer

ENTRYPOINT ["python", "-m", "trainer.train"]
