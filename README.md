# 📚 Manga Watcher

Manga Watcher is a simple script that monitors updates on **Listado Manga** for a list of tracked series and sends email notifications whenever new volumes are available.

------------------------------------------------------------------------

## 🚀 Features

-   Track multiple manga series
-   Automatically check for updates
-   Send email notifications when new volumes are released
-   Lightweight and easy to configure

------------------------------------------------------------------------

## 🛠️ Setup

### 1. Clone the Repository

``` bash
git clone <repository-url>
cd manga-watcher
```

------------------------------------------------------------------------

### 2. Install Dependencies (using `uv`)

This project uses [`uv`](https://github.com/astral-sh/uv) for fast Python environment and dependency management.

#### Install `uv` (if you don't have it)

``` bash
pip install uv
```

#### Create and sync the environment

``` bash
uv venv
uv sync
```

#### Activate the environment (optional)

``` bash
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows
```

------------------------------------------------------------------------

## 🔐 Environment Variables

You must configure the following environment variables for email
notifications:

  Variable     Description
  ------------ -----------------------------------------
  SMTP_HOST    SMTP server host (e.g., smtp.gmail.com)
  SMTP_PORT    SMTP server port (e.g., 587)
  SMTP_USER    SMTP username
  SMTP_PASS    SMTP password or app password
  EMAIL_FROM   Sender email address
  EMAIL_TO     Recipient email address

### Example (Linux/macOS)

``` bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your_email@gmail.com
export SMTP_PASS=your_password
export EMAIL_FROM=your_email@gmail.com
export EMAIL_TO=recipient@gmail.com
```


------------------------------------------------------------------------

## ▶️ Running the Application

``` bash
python checker.py
```

------------------------------------------------------------------------

## 🧩 Configuration

Make sure to update the list of mangas you want to track inside the `watch.txt` file.