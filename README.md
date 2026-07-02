![Tests](https://github.com/rivondave/E-Commerce-API/actions/workflows/tests.yml/badge.svg)
# E-Commerce Backend API

A production-style E-Commerce REST API built with FastAPI, PostgreSQL, SQLAlchemy, Docker, and JWT Authentication.

This project demonstrates backend engineering concepts including authentication, role-based authorization, product management, shopping cart functionality, order processing, inventory management, and relational database design.

## Live Demo

API Base URL:

https://e-commerce-api-dihq.onrender.com

Swagger Documentation:

https://e-commerce-api-dihq.onrender.com/docs

---

## Features

### Authentication

* User registration
* User login
* JWT-based authentication
* Protected routes

### Product Management

* Create products
* View products
* Update products
* Delete products
* Product search and filtering

### Categories

* Create categories
* View categories

### Shopping Cart

* Add products to cart
* View cart contents
* Remove cart items

### Orders

* Checkout cart
* Create orders
* View orders
* View individual order details

### Inventory Management

* Automatic stock reduction during checkout
* Stock validation before purchases

### Authorization

* Role-based access control
* Admin-only product management

---

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication
* Docker
* Render

---

## API Endpoints

### Authentication

| Method | Endpoint       | Description   |
| ------ | -------------- | ------------- |
| POST   | /auth/register | Register user |
| POST   | /auth/login    | Login user    |

### Categories

| Method | Endpoint    | Description     |
| ------ | ----------- | --------------- |
| GET    | /categories | Get categories  |
| POST   | /categories | Create category |

### Products

| Method | Endpoint               | Description    |
| ------ | ---------------------- | -------------- |
| GET    | /products              | Get products   |
| POST   | /products              | Create product |
| GET    | /products/{product_id} | Get product    |
| PUT    | /products/{product_id} | Update product |
| DELETE | /products/{product_id} | Delete product |

### Cart

| Method | Endpoint             | Description      |
| ------ | -------------------- | ---------------- |
| POST   | /cart/add            | Add to cart      |
| GET    | /cart                | Get cart         |
| DELETE | /cart/{cart_item_id} | Remove cart item |

### Orders

| Method | Endpoint           | Description |
| ------ | ------------------ | ----------- |
| POST   | /orders/checkout   | Checkout    |
| GET    | /orders            | Get orders  |
| GET    | /orders/{order_id} | Get order   |

---

## Project Structure

```text
app/
├── api/
├── core/
├── models/
├── schemas/
├── main.py

Dockerfile
docker-compose.yml
requirements.txt
.env
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost/ecommerce_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Local Installation

Clone the repository:

```bash
git clone https://github.com/rivondave/E-Commerce-API.git

cd E-Commerce-API
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Docker Setup

Build and run containers:

```bash
docker compose up --build
```

Access API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## What I Learned

* REST API design
* JWT Authentication
* Role-Based Access Control (RBAC)
* Relational Database Design
* Shopping Cart Architecture
* Order Processing Workflows
* Inventory Management
* Docker Containerization
* API Deployment with Render

```
```

## Testing

This project uses Pytest for automated testing.

### Covered Workflows

- User Registration
- User Login
- Product Creation
- Product Retrieval
- Cart Management
- Order Checkout

Run tests locally:

```bash
python -m pytest
