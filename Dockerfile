FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-fonts-recommended \
        texlive-pictures \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p tmp log

EXPOSE 5006

CMD ["sh", "-c", "python3 -m gunicorn controller:app --bind 0.0.0.0:${PORT:-5006}"]
