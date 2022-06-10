FROM python:3.9

# Install fundamental packages
RUN apt update -y \
  && apt upgrade -y \
  && apt install -y curl \
  && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN python3 -m pip install --no-cache-dir --upgrade pip \
  && python3 -m pip install --no-cache-dir setuptools \
  && python3 -m pip install --no-cache-dir poetry \
  && rm -rf ~/.cache/pip

# Configure poetry
RUN poetry config virtualenvs.create false

# Copy files and install depending python packages
RUN mkdir -p /opt/app
COPY ./pyproject.toml ./poetry.loc[k] /opt/app/
WORKDIR /opt/app
RUN poetry install \
  || ( \
    poetry update \
    && poetry install \
  ) \
  ; rm -rf ~/.cache/pypoetry/{cache,artifacts}

# Copy the remaining files
COPY . /opt/app

# Installation for CLI commands
RUN poetry install -vvv && rm -rf ~/.cache/pypoetry/{cache,artifacts}

# Default CMD
ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]
CMD ["/bin/bash"]
