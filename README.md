# Khadka CMS

A **basic, self-use Content Management System (CMS)** built with **Flask + SQLite** to manage a personal portfolio / landing page.

This project was created for **personal use only** — it is intentionally simple, lightweight, and easy to extend when the landing page grows.

---

## 🚀 Features

- Secure admin login
- Clean admin dashboard UI
- Manage:
  - Hero section
  - Biography / About
  - Projects
  - Testimonials
  - Contact info
- Image upload support
- Collapsible sidebar navigation
- SQLite database (no external DB setup)

---

## 🧠 Project Philosophy

- **Not a SaaS**
- **Not multi-user**
- **Not over-engineered**

This CMS is meant to:
- Edit a personal website fast
- Be readable and hackable
- Scale *only when needed*

If the landing page grows, you add new sections **manually and cleanly**.

---








---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install flask

2. Run the app
python app.py

3. Access

Landing page: http://127.0.0.1:5000/

Admin panel: http://127.0.0.1:5000/login

🔐 Authentication

This CMS uses simple credential-based login defined in app.py.

There is:

No user registration

No roles

No password reset

Because this CMS is intended for single-owner self use.

🗄️ Database Design

The project uses SQLite with one table per content type.

Example:

hero

about

projects

testimonials

contact

Each section on the landing page corresponds to one table.

➕ How to Add a New Section (Important)

If your landing page grows and you need new sections, follow this pattern.

1️⃣ Create a new table

Example: adding a services section

CREATE TABLE services (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  description TEXT
);

2️⃣ Handle the new form in app.py
if request.form['type'] == 'services':
    title = request.form['title']
    description = request.form['description']
    cursor.execute(
        "INSERT INTO services (title, description) VALUES (?, ?)",
        (title, description)
    )
    conn.commit()

3️⃣ Add admin UI (admin.html)
<section id="services">
  <h2>Services</h2>
  <form method="POST">
    <input type="hidden" name="type" value="services">
    <input name="title" placeholder="Service Title">
    <textarea name="description" placeholder="Description"></textarea>
    <button>Add Service</button>
  </form>
</section>

4️⃣ Render on landing page (index.html)

Fetch from DB and loop like other sections.

📌 Guidelines for Scaling

One section = one table

Keep forms simple

Avoid generic JSON blobs

Add tables only when content becomes permanent

Do not prematurely abstract

This keeps the CMS maintainable and readable.

🧪 Limitations (By Design)

Single admin

No WYSIWYG editor

No API

No permissions system

These are intentional choices.

🧾 License

This project is free for personal use.

You may:

Fork it

Modify it

Learn from it

But this CMS was not designed for commercial resale.

✍️ Author

Sharad Khadka

Built for personal workflow, learning, and control.


---


