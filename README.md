# Task Manager – Django + Three.js

## 1. Project Overview

This is a Task Management web application built with Django and SQLite following the MVC/MVT pattern.  
It allows users to **create, read, update, delete, and search tasks**, with a **3D task board** implemented using **Three.js**.

Each task is visualized as a rotating cube whose color reflects its status (Todo, In Progress, Done, Blocked).  
The UI uses a **dark futuristic theme**, **glassmorphism cards**, **gradient buttons**, and a **Three.js floating starfield background**.

---

## 2. Technology Stack

- **Backend**: Python 3, Django 5
- **Database**: SQLite
- **Frontend**: Django Templates (HTML, CSS, JavaScript)
- **3D/Graphics**: Three.js

---

## 3. Database Design

### 3.1 ER Diagram (Description)

Entities:

- **Task**

Relationships:

- Standalone entity in this version. `created_by` and `last_updated_by` are stored as string fields (user name / id) rather than foreign keys for simplicity.

### 3.2 Data Dictionary

**Table: tasks_task**

| Column           | Type         | Nullable | Description                                      |
|------------------|-------------|----------|--------------------------------------------------|
| id               | bigint PK   | No       | Auto-increment primary key                       |
| title            | varchar(200)| No       | Task title                                       |
| description      | text        | Yes      | Detailed description                             |
| due_date         | date        | Yes      | Task due date                                    |
| status           | varchar(20) | No       | One of `todo`, `in_progress`, `done`, `blocked` |
| remarks          | text        | Yes      | Additional comments / notes                      |
| created_on       | datetime    | No       | Timestamp when the task was created              |
| last_updated_on  | datetime    | No       | Timestamp of last modification                   |
| created_by       | varchar(150)| No       | Name/id of creator (stored as string)           |
| last_updated_by  | varchar(150)| No       | Name/id of last updater (stored as string)      |

### 3.3 Indexes

Indexes are applied via model field options:

- `title` – `db_index=True` for faster search by title
- `status` – `db_index=True` for filtering by status
- `due_date` – `db_index=True` for date-based filtering

These cover the main query axes of the search feature.

### 3.4 Code-First Approach

- **Approach**: Code-first using Django models and migrations.
- **Reasons**:
  - Schema is version-controlled alongside application code.
  - Changes flow through migration files, which are easy to apply and roll back.
  - Faster development and safer evolution of the schema compared to editing SQL manually.

---

## 4. Application Structure

Project layout:

```text
taskmanager/
  manage.py
  requirements.txt

  taskmanager/
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py

  tasks/
    __init__.py
    apps.py
    models.py
    forms.py
    views.py
    urls.py
    admin.py
    migrations/
      __init__.py

  templates/
    base.html
    tasks/
      task_list.html
      task_form.html
      task_confirm_delete.html

  static/
    css/
      main.css
    js/
      stars.js
      task_board.js
```

Key components:

- **Models (`tasks/models.py`)** – `Task` model with all required fields and indexes.
- **Forms (`tasks/forms.py`)** – `TaskForm` as a `ModelForm` with basic widgets.
- **Views (`tasks/views.py`)** – Class-based views:
  - `TaskListView` – dashboard listing with filters
  - `TaskSearchView` – dedicated search endpoint reusing the same template
  - `TaskCreateView` – create task
  - `TaskUpdateView` – edit task
  - `TaskDeleteView` – delete confirmation and delete
- **URLs (`tasks/urls.py`)** – routes for all views, included from `taskmanager/urls.py`.
- **Templates** – `base.html` layout plus task-specific pages.
- **Static** – shared CSS (`main.css`), `stars.js` for animated background, `task_board.js` for the 3D task cubes.

---

## 5. Installation Steps

### 5.1 Prerequisites

- Python 3.10+ (recommended)
- pip

### 5.2 Setup

From the project root (`taskmanager/` directory containing `manage.py`):

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 5.3 Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5.4 Create Superuser

```bash
python manage.py createsuperuser
```

Use this account to log into the admin and the application.

### 5.5 Run the Development Server

```bash
python manage.py runserver
```

Visit:

- `http://127.0.0.1:8000/admin/` – Django admin
- `http://127.0.0.1:8000/` – Task dashboard

---

## 6. Features

### 6.1 CRUD Operations

- **Create** – Use “Create Task” from navbar or sidebar; form validates all fields.
- **Read** – Dashboard lists all tasks and visualizes them in 3D.
- **Update** – Edit button opens the form with existing values.
- **Delete** – Delete button opens a confirmation page before removal.

### 6.2 Search

- Search panel on the left:
  - Text query matches `title`, `description`, `remarks`.
  - Status filter matches `status`.
  - Due date filter matches `due_date`.
- Implemented via `TaskListView`/`TaskSearchView` with `Q` filters.

### 6.3 3D Task Board

- Implemented in `static/js/task_board.js` and used by `task_list.html`.
- Each task is a rotating cube:
  - Todo → blue
  - In Progress → yellow
  - Done → green
  - Blocked → red
- Hovering over a cube enlarges it using a raycaster and scale animation.

### 6.4 Three.js Starfield Background

- Implemented in `static/js/stars.js` and loaded in `base.html`.
- Floating stars rendered with `THREE.Points`.
- Mouse movement changes camera position slightly for a parallax effect.

---

## 7. Environment & Dependencies

- **Python**: 3.10+
- **Django**: 5.0.6
- **SQLite**: default Django backend (no extra install)
- **Three.js**: loaded from CDN in `base.html`

No additional system dependencies are required beyond a working Python environment.

---

## 8. How to Extend

- Replace `created_by` / `last_updated_by` string fields with `ForeignKey` to Django’s `User` model when you need full user management.
- Add pagination UI for long task lists.
- Add extra fields like priority, tags, or attachments.

