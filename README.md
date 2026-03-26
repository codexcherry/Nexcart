# 🛒 NexCart

A modern e-commerce platform built with Streamlit and SQLite, featuring a clean dark-themed UI for seamless online shopping.

## ✨ Features

- **Product Catalog**: Browse products with search, category filtering, and sorting options
- **Shopping Cart**: Add items to cart with quantity management
- **Order Management**: Place orders and track order history
- **User Authentication**: Simple user registration and login system
- **Admin Dashboard**: Manage products, orders, and view analytics
- **Responsive Design**: Clean, modern dark-themed interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/nexcart.git
cd nexcart
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run main.py
```

5. Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
nexcart/
├── backend/
│   ├── crud/           # Database CRUD operations
│   ├── services/       # Business logic layer
│   ├── db.py          # Database initialization
│   ├── schema.py      # Data models
│   └── seed.py        # Sample data seeding
├── ui/
│   ├── home.py        # Home page
│   ├── cart.py        # Shopping cart
│   ├── orders.py      # Order management
│   └── admin.py       # Admin dashboard
├── utils/
│   ├── helpers.py     # Utility functions
│   ├── logger.py      # Logging utilities
│   └── reporter.py    # Reporting utilities
├── data/              # SQLite database storage
├── tests/             # Test suite
├── main.py            # Application entry point
└── requirements.txt   # Python dependencies
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Database**: SQLite
- **Backend**: Python
- **Data Validation**: Pydantic
- **Testing**: Pytest, Hypothesis

## 📝 Usage

### For Customers

1. Register or select a user from the sidebar
2. Browse products on the home page
3. Use search and filters to find products
4. Add items to your cart
5. Review cart and place orders
6. Track your order history

### For Admins

1. Login with admin credentials
2. Access the Admin dashboard from navigation
3. Manage products (add, edit, delete)
4. View and manage orders
5. Access analytics and reports

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📧 Contact

For questions or support, please open an issue on GitHub.
