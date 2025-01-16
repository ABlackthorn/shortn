# syntax=docker/dockerfile:1

FROM archlinux:latest

RUN pacman -Syu --noconfirm
RUN pacman -S python python-pip --noconfirm
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m venv venv
ENV PATH="./venv/bin:$PATH"

RUN pip install -r requirements.txt

COPY ./src /code

CMD ["/code/venv/bin/fastapi", "run", "main.py", "--port", "8000"]
