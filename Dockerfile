FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Do the variable commands
COPY ./db ./db
RUN  prisma generate --schema ./db/schema.prisma
RUN python -m nltk.downloader punkt_tab

# Bring In the fixed stuff
COPY ./models ./models
COPY ./pipeline.py ./pipeline.py
COPY ./data ./data


ENTRYPOINT ["python3", "pipeline.py"]
CMD [""]
