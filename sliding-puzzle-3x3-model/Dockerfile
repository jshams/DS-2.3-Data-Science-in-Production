FROM python:3.7-buster
WORKDIR /app
COPY ./ ./
COPY ./solvers ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
ENV FLASK_APP=/app/app.py 

EXPOSE 5000
ENTRYPOINT [ "python3" ] 
CMD ["-m", "flask", "run"]