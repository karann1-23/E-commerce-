# E-commerce Website

A Django-based e-commerce website I built to learn web development and create a functional online store. Features include product browsing, shopping cart, user authentication, and Stripe payment integration.

## What I Built

This is a complete e-commerce solution that lets users:
- Browse products with search and category filters
- Add items to cart and wishlist
- Create accounts and manage profiles
- Complete purchases with Stripe payments
- Admin panel for managing products and orders

## Features

### Shopping Features
- Product catalog with responsive grid layout
- Search products by name, description, or category
- Filter products by categories
- Shopping cart with add/remove functionality
- Wishlist to save products for later
- Mobile-friendly responsive design

### User Features
- User registration and login system
- User profiles with address and phone storage
- Persistent shopping cart and wishlist
- Secure authentication

### Payment Features
- Stripe payment gateway integration
- Checkout process with shipping costs
- Payment success confirmation
- Order tracking

### Admin Features
- Django admin panel for product management
- Add/edit products with images
- Manage categories
- View orders and user data

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. Clone the repo
```bash
git clone https://github.com/yourusername/django-ecommerce-website.git
cd django-ecommerce-website
```

2. Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

3. Install packages
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file:
```
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
SECRET_KEY=your_django_secret_key
```

5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create admin user
```bash
python manage.py createsuperuser
```

7. Start the server
```bash
python manage.py runserver
```

8. Visit the site
- Main site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
e-commerce-website/
├── app/                    # Main app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin config
│   └── templates/         # HTML templates
├── ecommerce/             # Project settings
├── media/                 # Uploaded files
├── manage.py             # Django management
└── requirements.txt      # Dependencies
```

## Tech Stack

- **Backend**: Django 4.2
- **Database**: SQLite (easy to switch to PostgreSQL/MySQL)
- **Payment**: Stripe API
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with modern design

## Dependencies

```
Django>=4.2.0
Pillow>=9.0.0
stripe>=5.0.0
python-decouple>=3.6
```

## Stripe Setup

1. Sign up at [stripe.com](https://stripe.com)
2. Get your API keys from the dashboard
3. Add to `.env` file:
```
STRIPE_PUBLIC_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
```

## What I Learned

Building this project taught me:
- Django framework fundamentals
- Database modeling and relationships
- User authentication and sessions
- Payment gateway integration
- Frontend development with HTML/CSS
- Responsive web design
- Git version control

## Challenges I Faced

- Setting up Stripe integration properly
- Managing user sessions and cart persistence
- Creating responsive design for mobile
- Handling image uploads and storage
- Implementing search and filtering

## Future Improvements

Some ideas for future versions:
- Product reviews and ratings
- Email notifications
- Order history tracking
- Discount codes
- Multiple payment methods
- Inventory management
- Analytics dashboard

## Deployment

For production deployment:
1. Set `DEBUG = False` in settings
2. Use a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure web server (Nginx/Apache)
5. Add SSL certificates

## Contributing

Feel free to fork this project and submit pull requests. I'm always open to suggestions and improvements!

## License

This project is open source and available under the MIT License.

## Contact

If you have questions or want to connect:
- GitHub: [your-username](https://github.com/your-username)
- Email: your-email@example.com

---

Thanks for checking out my e-commerce project! 🛍️
