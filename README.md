# 🚀 Feature Flag Service

A lightweight and scalable **Feature Flag system** built with FastAPI to control feature rollouts dynamically without redeploying applications.

---

## 🧠 Overview

This service allows you to:

- Enable/disable features globally  
- Roll out features to a percentage of users  
- Override feature access for specific users  

It helps teams safely release features, run experiments, and control behavior in production.

---

## ⚙️ Tech Stack

- **FastAPI** — API framework  
- **SQLite / PostgreSQL** — Database  
- **Redis (optional)** — Caching for fast flag evaluation  

---

## 🧩 Features

- Create and manage feature flags  
- Toggle features on/off  
- Percentage-based rollout  
- User-specific overrides  
- Deterministic evaluation (same user gets same result)

---

## 📦 API Endpoints

### ➤ Create Feature
POST /features

### ➤ Update Feature
PATCH /features/{id}

### ➤ Check Feature for User
GET /features/{name}/check?user_id=123

---

## 🧠 How It Works

Feature evaluation follows this order:

1. Check user-specific override  
2. Apply percentage rollout logic  
3. Fallback to global feature flag  

---

## 🔢 Rollout Logic

```python
hash(user_id) % 100 < rollout_percentage