FROM python:3

RUN curl -sSL https://install.python-poetry.org |  POETRY_HOME=/usr/local python3 -

ENV INSTALL_DIR=/opt/adishop
WORKDIR ${INSTALL_DIR}
COPY pyproject.toml .

RUN poetry install --no-root

# Development workaround - make sure we don't override poetry.lock inside the container with one we're copying from local
RUN mv poetry.lock poetry.lock.bak
COPY . .
RUN mv poetry.lock.bak poetry.lock

# install the app - as it wasn't there when we did this before
RUN poetry install 

ENV PYTHONUNBUFFERED=1