From python:3.10.1
RUN mkdir /uploads
ENV UPLOADS=/uploads
ENV PATH=/root/.local/bin:$PATH

ENV PORT 5000
ENV HOST "0.0.0.0"

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN [ "python3", "-c", "import nltk; nltk.download('stopwords', download_dir='/usr/local/nltk_data'); nltk.download('punkt', download_dir='/usr/local/nltk_data');" ]
# Minimize image size
RUN (apt-get autoremove -y; \
     apt-get autoclean -y)
ADD . /app/

EXPOSE $PORT
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
#ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", $PORT]
CMD uvicorn main:app --host 0.0.0.0 --port $PORT