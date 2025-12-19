# Receipt Tracker (Django + OCR)

A web application that lets you upload receipts, extract text using OCR, parse items, and track spending over time.

## Features (Completed Week 1)
- Dockerized Django environment
- PostgreSQL database
- Receipts app with models (Vendor, Receipt, Item)
- Admin dashboard
- Homepage with navigation
- Unit tests for models and queries

## Tech Stack
- Django 5
- PostgreSQL
- Docker & Docker Compose
- Tesseract OCR (coming in Week 3)

## How to Run
docker compose up --build

Visit:
- http://localhost:8000 → Homepage
- http://localhost:8000/admin → Admin
- http://localhost:8000/receipts → Receipts app