FROM archlinux

COPY . /predict

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm python python-pip glu

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install onnxruntime pyzmq opencv-python

WORKDIR /predict

ENTRYPOINT ["python","predict.py"]