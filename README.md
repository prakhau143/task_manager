# Task Management Application (Oritso Screening Assignment)

## 2.1.3.1 Overview of what is being built

This repository contains a **Task Management web application** built for the Oritso Private Limited screening assignment.

The application demonstrates the required MVC/MVT areas:

- **Create** tasks from a web UI
- **Read** tasks from a web UI (dashboard + task details)
- **Update** tasks from a web UI (edit form + inline status update)
- **Delete** tasks from a web UI (delete confirmation)
- **Search** tasks from a web UI (query + status + due date)

The UI is modern and interactive (dark futuristic theme, glassmorphism, gradient buttons), and includes:

- **Three.js animated starfield background**
- **Three.js 3D Task Board** where tasks appear as rotating cubes, color-coded by status and clickable to open details

---

## 2.1.3.2 Explanation of DB Design

### 2.1.3.2.1 ER Diagram

**Entities**

- `Task`

**Relationships**

- This implementation stores `created_by` and `last_updated_by` as strings (`username (#id)`) for simplicity and to match the assignment’s “Name and Id” requirement.

ER (textual):

- `Task` (standalone)

### 2.1.3.2.2 Data Dictionary

**Table: tasks_task**

| Column          | Type          | Nullable | Description |
|-----------------|---------------|----------|-------------|
| id              | bigint (PK)   | No       | Auto-increment primary key |
| title           | varchar(200)  | No       | Task Title |
| description     | text          | Yes      | Task Description |
| due_date        | date          | Yes      | Task Due Date |
| status          | varchar(20)   | No       | Task Status (`todo`, `in_progress`, `done`, `blocked`) |
| remarks         | text          | Yes      | Task Remarks |
| created_on      | timestamptz   | No       | Created On (Time Stamp) |
| last_updated_on | timestamptz   | No       | Last Updated On (Time Stamp) |
| created_by      | varchar(150)  | No       | Created By (Name + Id as string) |
| last_updated_by | varchar(150)  | No       | Last Updated By (Name + Id as string) |

### 2.1.3.2.3 Documentation of Indexes used

Indexes are defined at model level using `db_index=True` to speed up searches and filters:

- `title` (search)
- `status` (filter)
- `due_date` (filter)

### 2.1.3.2.4 Code first or DB First and why?

- **Approach used**: **Code First** (Django ORM + migrations)
- **Why**:
  - Version controlled schema changes via migration files
  - Faster development workflow for an assignment timeline
  - Easier to reproduce setup on any machine

---

## 2.1.3.3 Structure of the application

### 2.1.3.3.2 Standard MVC server-side page rendering

This project uses **server-side rendering (MPA)** with Django templates (Django MVT pattern).

- **Models**: `tasks/models.py`
- **Views/Controllers**: `tasks/views.py` (class-based views)
- **Templates**: `templates/` (HTML pages)
- **Static assets**: `static/` (CSS/JS)

---

## 2.1.3.4 Frontend Structure

### 2.1.3.4.1 What kind of frontend has been used and why?

- **Django Templates + HTML/CSS/JS** were used to keep the solution simple, fast to run, and easy to demonstrate.
- **Three.js** is used for:
  - Starfield background animation
  - 3D Task Board (rotating, color-coded, clickable cubes)

### 2.1.3.4.2 Web or mobile?

- **Web frontend** (Django templates)

---

## 2.1.3.5 Build and install

### 2.1.3.5.1 Environment details and dependencies

- Python 3.10+ recommended
- Django 5
- PostgreSQL 14+ recommended

Dependencies are listed in `requirements.txt`.

### 2.1.3.5.2 Instructions to build / compile

This is a Python/Django project; no compile step is required. Install dependencies via pip.

### 2.1.3.5.3 Instructions to run

#### 1) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2) Create PostgreSQL database and user

```sql
CREATE DATABASE task_db;
CREATE USER task_user WITH ENCRYPTED PASSWORD 'task_password';
GRANT ALL PRIVILEGES ON DATABASE task_db TO task_user;
```

#### 3) Set environment variables (recommended)

```bash
export POSTGRES_DB=task_db
export POSTGRES_USER=task_user
export POSTGRES_PASSWORD=task_password
export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT=5432
```

#### 4) Run migrations + create admin user

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 5) Start server

```bash
python manage.py runserver
```

Open:

- `http://127.0.0.1:8000/admin/` (login)
- `http://127.0.0.1:8000/` (dashboard)

---

## General Documentation (not covered above)

- **Dashboard**
  - Shows latest tasks (3D board shows up to 10 cubes in a fixed 2×5 grid)
  - Search panel filters tasks by query, status, due date
  - Inline status dropdown allows updating status quickly
- **3D Task Board**
  - Cube color indicates status (Todo/Blue, In Progress/Yellow, Done/Green, Blocked/Red)
  - Clicking a cube opens `/tasks/<id>/` task details page


