FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build the vector store at image build time so it ships ready-to-query.
# (In a real pipeline, this would instead pull a pre-built store from
# object storage so a knowledge-base update doesn't require a rebuild.)
RUN python knowledge/build_index.py

EXPOSE 5000
ENV FLASK_APP=app.py

CMD ["python", "app.py"]
