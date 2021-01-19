# Flask YOLO API

---

## Option a) Run as Docker container

### 1. Clone repo

```bash
git clone https://github.com/patryklaskowski/Flask_YOLO_API.git && \
cd Flask_YOLO_API
```

### 2. Run as Docker container using Docker-Compose

**[NOTE]** Make sure Docker is up and running.

```bash
docker-compose up --remove-orphans
```

Docker container with API is now running.<br>
Go to `http://localhost:5000/` to see the README.md.<br>
*Server available externally as well: `http://<IP addr>:5000/`*<br>

---

## Option b) Run as Python script using virtual environment

### 1. Clone repo

```bash
git clone https://github.com/patryklaskowski/Flask_YOLO_API.git && \
cd Flask_YOLO_API
```

### 2. To run server as Python script using venv (virtual environment).

```bash
python3.7 -m venv env && \
source env/bin/activate && \
python3.7 -m pip install -U pip && \
python3.7 -m pip install -r requirements.txt && \
python3.7 run.py
```

### 3. To deactivate virtual environment
```bash
deactivate
```


Server is now running.<br>
Go to `http://localhost:5000/` to see the README.md.<br>
*Server available externally as well: `http://<IP addr>:5000/`*<br>

---

## TODO:
- [ ] Make API with multiprocessing server (image processing is CPU bound).
- [ ] Send data into db.
- [ ] Activated models limit. Depends on CPU cores using decorator that record all instances.
- [ ] Create doc on how to use API.
- [ ] Allow to use multiple models by /predict/<model>
