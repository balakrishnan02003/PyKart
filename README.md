# PyKart - E-Commerce Project

A Django-based e-commerce platform with a modern frontend.

## Project Structure

```
E-Commerce Project PyKart/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── pykart/                   # Main project directory
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── store/                    # Store app (Products & Categories)
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py             # Category, Product, ProductImage models
│   ├── admin.py              # Admin configuration
│   ├── views.py              # Home, category products, product detail views
│   ├── urls.py               # Store URL patterns
│   └── templates/
│       └── store/
│           ├── base.html     # Base template
│           ├── home.html     # Home page with categories
│           ├── category_products.html  # Category product listing
│           └── product_detail.html    # Product detail page
│
├── static/                   # Static files (CSS, JS, images)
│   └── store/
│       ├── css/
│       │   └── style.css     # Main stylesheet
│       └── js/
│           └── main.js       # Main JavaScript
│
└── media/                    # User uploaded files (created after first run)
    ├── categories/           # Category images
    └── products/             # Product images
```

## Setup Instructions

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (to access admin panel):
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Home page: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Store App Features

### Models
- **Category**: Product categories (name, slug, image)
- **Product**: Products (name, slug, price, stock, description, main_image, category, is_active)
- **ProductImage**: Additional product images

### Views
- **Home**: Displays all categories as cards
- **Category Products**: Shows products for a specific category
- **Product Detail**: Detailed product view with images and description

### Admin Features
- Full CRUD operations for Categories and Products
- Inline editing for ProductImages
- Stock management
- Product activation/deactivation

## Next Steps

The following apps will be implemented:
- **cart**: Shopping cart functionality
- **accounts**: User authentication and address management
- **orders**: Checkout, order creation, and invoice generation

## Notes

- Static files are served from the `static/` directory
- Media files (uploads) are stored in the `media/` directory
- The project uses SQLite by default (can be changed in settings.py)

