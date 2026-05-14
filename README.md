🚀 Helpdesk Support System | Full-Stack Ticket Management with Real-time Chat
<div align="center">
https://via.placeholder.com/800x200/4F46E5/ffffff?text=Helpdesk+Support+System

A Professional Open-Source Support Platform with Real-time Chat, Ticket Management, and RBAC

https://img.shields.io/badge/Django-4.2-green.svg
https://img.shields.io/badge/React-18.2-blue.svg
https://img.shields.io/badge/WebSocket-Real--time-orange.svg
https://img.shields.io/badge/Docker-Ready-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/PRs-welcome-brightgreen.svg

</div>
📖 Table of Contents
Project Overview

Key Features

Live Demo

Technologies

Quick Start with Docker

Manual Installation

Project Structure

API Documentation

WebSocket Communication

Environment Variables

Screenshots

Troubleshooting

Roadmap

Contributing

License

Support

🎯 Project Overview
Helpdesk Ticketing System is a professional, open-source support platform that enables organizations and businesses to efficiently manage customer support requests. Built with modern web technologies, it provides a seamless real-time experience for all users.

What Problem Does It Solve?
Problem	Solution
Scattered ticket management	Centralized platform for all requests
Delayed responses	Real-time chat for instant communication
Lack of transparency	Real-time ticket status tracking
Unclear permissions	Granular RBAC system
Target Users
Role	Description	Expected Count
Admin	Full system access	1-3 users
Support Agent	Ticket management and response	5-50 users
Customer	Ticket creation and tracking	Unlimited
✨ Key Features
For Customers
✅ Create tickets with multiple categories

✅ View complete ticket history

✅ Real-time chat with support agents

✅ Track ticket status (Open, In Progress, Resolved, Closed)

✅ Receive instant notifications

For Support Agents
✅ View all system tickets

✅ Self-assign tickets

✅ Change ticket status

✅ Real-time response to customers

✅ Advanced filtering and search

✅ Ticket assignment management

For Admins
✅ Complete user management (CRUD)

✅ Category management

✅ Access to all support features

✅ System configuration

✅ View analytics and reports

Technical Features
✅ JWT Authentication

✅ WebSocket Real-time Communication

✅ Docker Support (Production Ready)

✅ PostgreSQL Database

✅ Redis Channel Layer

✅ RESTful API with DRF

✅ Responsive Design (Mobile/Tablet/Desktop)

✅ RTL Support (Persian/Arabic)

🎥 Live Demo
Coming Soon! The demo will be available at: https://helpdesk.yourdomain.com

Demo Credentials:

text
Admin: admin@example.com / admin123
Support: support@example.com / support123
Customer: customer@example.com / customer123
🛠 Technologies
Backend Stack
Technology	Version	Purpose
Python	3.11+	Core language
Django	4.2+	Web framework
Django REST Framework	3.14+	API development
Django Channels	4.0+	WebSocket support
PostgreSQL	15+	Primary database
Redis	7.0+	Channel layer
Daphne	4.0+	ASGI server
JWT	5.3+	Authentication
Docker	Latest	Containerization
Frontend Stack
Technology	Version	Purpose
React	18.2+	UI framework
Vite	5.0+	Build tool
Tailwind CSS	3.4+	Styling
React Router	6.20+	Routing
Axios	1.6+	HTTP client
WebSocket API	-	Real-time
Docker	Latest	Containerization
🚀 Quick Start with Docker
Prerequisites
bash
- Docker 20.10+
- Docker Compose 2.20+
- Git
- 4GB RAM minimum
Backend Setup
bash
# 1. Clone the repository
git clone https://github.com/yourusername/helpdesk-backend.git
cd helpdesk-backend

# 2. Copy environment variables
cp .env.example .env

# 3. Edit .env file with your values
nano .env

# 4. Start the backend services
docker-compose up -d

# 5. Run migrations
docker-compose exec backend python manage.py migrate

# 6. Create superuser
docker-compose exec backend python manage.py createsuperuser

# 7. Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
Frontend Setup
bash
# 1. Clone the repository
git clone https://github.com/yourusername/helpdesk-frontend.git
cd helpdesk-frontend

# 2. Copy environment variables
cp .env.example .env

# 3. Edit .env file with your API URL
nano .env

# 4. Build and run frontend
docker-compose up -d

# 5. Access the application
# Open browser: http://localhost
Docker Compose Files
<details> <summary><b>Backend docker-compose.yml</b></summary>
yaml
services:
  db:
    image: docker.arvancloud.ir/postgres:15-alpine
    container_name: helpdesk_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-tickets_db}
      - POSTGRES_USER=${POSTGRES_USER:-tickets_user}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-strong_password_here}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-tickets_user}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - helpdesk_network
    restart: unless-stopped

  redis:
    image: docker.arvancloud.ir/redis:7-alpine
    container_name: helpdesk_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - helpdesk_network
    restart: unless-stopped

  backend:
    build: .
    container_name: helpdesk_backend
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG:-True}
      - ALLOWED_HOSTS=localhost,127.0.0.1,backend
      - POSTGRES_DB=${POSTGRES_DB:-tickets_db}
      - POSTGRES_USER=${POSTGRES_USER:-tickets_user}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-strong_password_here}
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - helpdesk_network
    restart: unless-stopped

networks:
  helpdesk_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
</details><details> <summary><b>Frontend docker-compose.yml</b></summary>
yaml
services:
  frontend:
    build: .
    container_name: helpdesk_frontend
    ports:
      - "80:80"
    networks:
      - backend_helpdesk_network
    restart: unless-stopped

networks:
  backend_helpdesk_network:
    external: true
    name: backend_helpdesk_network
</details>
📦 Manual Installation
Backend Installation
bash
# 1. Clone repository
git clone https://github.com/yourusername/helpdesk-backend.git
cd helpdesk-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database (PostgreSQL)
sudo -u postgres psql
CREATE DATABASE tickets_db;
CREATE USER tickets_user WITH PASSWORD 'strong_password';
ALTER ROLE tickets_user SET client_encoding TO 'utf8';
ALTER ROLE tickets_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE tickets_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE tickets_db TO tickets_user;
\q

# 5. Configure environment
cp .env.example .env
nano .env

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Start Redis (for WebSocket)
# Using Docker
docker run -d -p 6379:6379 redis

# Or using system package manager
sudo apt-get install redis-server
sudo systemctl start redis-server

# 9. Run the server
# Development (without WebSocket)
python manage.py runserver

# Production (with WebSocket)
daphne -b 0.0.0.0 -p 8000 helpdesk_backend.asgi:application
Frontend Installation
bash
# 1. Clone repository
git clone https://github.com/yourusername/helpdesk-frontend.git
cd helpdesk-frontend

# 2. Install dependencies
npm install
# or
yarn install

# 3. Configure environment
cp .env.example .env
nano .env

# 4. Run development server
npm run dev
# or
yarn dev

# 5. Build for production
npm run build
# or
yarn build

# 6. Preview production build
npm run preview
📁 Project Structure
Backend Structure
text
helpdesk-backend/
├── accounts/                 # User management
│   ├── models.py            # Custom User model
│   ├── views.py             # User CRUD operations
│   ├── serializers.py       # User data serialization
│   └── urls.py              # User endpoints
├── tickets/                  # Ticket management
│   ├── models.py            # Ticket & Category models
│   ├── views.py             # Ticket operations
│   ├── serializers.py       # Ticket serialization
│   └── urls.py              # Ticket endpoints
├── chats/                    # Real-time chat system
│   ├── models.py            # ChatMessage model
│   ├── consumers.py         # WebSocket consumers
│   ├── routing.py           # WebSocket routing
│   └── views.py             # Message API
├── helpdesk_backend/         # Project config
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URLs
│   └── asgi.py              # ASGI config
├── requirements.txt          # Dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker compose
├── .env.example             # Environment template
└── manage.py                # Django CLI
Frontend Structure
text
helpdesk-frontend/
├── src/
│   ├── components/          # React components
│   │   ├── auth/           # Login, Register
│   │   ├── tickets/        # TicketList, TicketCard, TicketDetail
│   │   ├── categories/     # Category management
│   │   ├── users/          # User management
│   │   └── common/         # Navbar, LoadingSpinner
│   ├── services/            # API services
│   │   ├── api.js          # Axios config
│   │   ├── auth.js         # Auth service
│   │   ├── ticketService.js
│   │   ├── categoryService.js
│   │   ├── userService.js
│   │   ├── messageService.js
│   │   └── websocketService.js
│   ├── contexts/            # React contexts
│   │   └── AuthContext.js
│   ├── hooks/               # Custom hooks
│   ├── utils/               # Utilities
│   ├── styles/              # Global styles
│   ├── App.jsx              # Main component
│   └── main.jsx             # Entry point
├── public/                  # Static files
├── Dockerfile              # Docker config
├── nginx.conf              # Nginx config
├── .env.example            # Environment template
├── vite.config.js          # Vite config
├── tailwind.config.js      # Tailwind config
└── package.json            # Dependencies
📡 API Documentation
Authentication Endpoints
Method	Endpoint	Description	Request	Response
POST	/api/token/	Login	{username, password}	{access, refresh}
POST	/api/token/refresh/	Refresh token	{refresh}	{access}
User Endpoints
Method	Endpoint	Description	Permissions
GET	/api/users/	List users	Admin
POST	/api/users/	Create user	Admin
GET	/api/users/{id}/	Get user	Admin/Support
PUT	/api/users/{id}/	Update user	Admin
DELETE	/api/users/{id}/	Delete user	Admin
Ticket Endpoints
Method	Endpoint	Description	Permissions
GET	/api/tickets/	List tickets	All authenticated
POST	/api/tickets/	Create ticket	Customer
GET	/api/tickets/{id}/	Get ticket	Role-based
PUT	/api/tickets/{id}/	Update ticket	Support/Admin
PATCH	/api/tickets/{id}/	Partial update	Support/Admin
Category Endpoints
Method	Endpoint	Description	Permissions
GET	/api/categories/	List categories	All authenticated
POST	/api/categories/	Create category	Admin
PUT	/api/categories/{id}/	Update category	Admin
DELETE	/api/categories/{id}/	Delete category	Admin
Message Endpoints
Method	Endpoint	Description	Permissions
GET	/api/chat-messages/	Get messages	Role-based
POST	/api/chat-messages/	Send message	Role-based
POST	/api/chat-messages/mark_as_read/	Mark as read	Role-based
API Usage Examples
bash
# 1. Login
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 2. Create Ticket
curl -X POST http://localhost:8000/api/tickets/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Login Issue",
    "description": "Cannot access account",
    "category": 1,
    "priority": "high"
  }'

# 3. List Tickets
curl -X GET "http://localhost:8000/api/tickets/?status=open&priority=high" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Update Ticket Status
curl -X PATCH http://localhost:8000/api/tickets/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'

# 5. Get Messages
curl -X GET "http://localhost:8000/api/chat-messages/?ticket=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
🔌 WebSocket Communication
Connection
text
ws://localhost:8000/ws/chat/{ticket_id}/?token={jwt_token}
Send Message Types
1. Chat Message
json
{
  "type": "message",
  "message": "Hello, I need help!",
  "user_id": 1,
  "username": "john_doe"
}
2. Typing Indicator
json
{
  "type": "typing",
  "is_typing": true
}
3. Status Update (Support/Admin only)
json
{
  "type": "status_update",
  "status": "resolved"
}
Receive Message Types
1. New Chat Message
json
{
  "type": "message",
  "message": "How can I help?",
  "username": "support_agent",
  "user_id": 3,
  "created_at": "2024-01-15T10:30:00Z",
  "message_id": 123
}
2. Status Update
json
{
  "type": "status_update",
  "status": "in_progress",
  "updated_by": "support_agent"
}
3. Typing Indicator
json
{
  "type": "typing",
  "username": "john_doe",
  "is_typing": true
}
Testing WebSocket with wscat
bash
# Install wscat
npm install -g wscat

# Connect
wscat -c "ws://localhost:8000/ws/chat/1/?token=YOUR_TOKEN"

# Send message
{"type": "message", "message": "Test", "user_id": 1, "username": "test"}
🔐 Environment Variables
Backend .env Example
env
# Django Settings
SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=tickets_db
POSTGRES_USER=tickets_user
POSTGRES_PASSWORD=your-strong-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=5  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1  # days

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
Frontend .env Example
env
# API Configuration
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=localhost:8000

# App Configuration
VITE_APP_NAME=Helpdesk Support System
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_WEBSOCKET=true
VITE_ENABLE_NOTIFICATIONS=true
📸 Screenshots
<details> <summary><b>Click to view screenshots</b></summary>
Login Page
https://via.placeholder.com/800x400/4F46E5/ffffff?text=Login+Page

Dashboard
https://via.placeholder.com/800x400/4F46E5/ffffff?text=Dashboard

Ticket List
https://via.placeholder.com/800x400/4F46E5/ffffff?text=Ticket+List

Ticket Detail & Chat
https://via.placeholder.com/800x400/4F46E5/ffffff?text=Ticket+Detail+with+Chat

User Management
https://via.placeholder.com/800x400/4F46E5/ffffff?text=User+Management

Category Management
https://via.placeholder.com/800x400/4F46E5/ffffff?text=Category+Management

</details>
🐛 Troubleshooting
Common Issues & Solutions
Issue 1: WebSocket 403 Error
bash
# Problem: Customer cannot connect to ticket WebSocket
# Solution: Check ticket ownership
# Ensure customer only connects to their own tickets
# Support/Admin can connect to all tickets
Issue 2: Database Connection Error
bash
# Problem: Cannot connect to PostgreSQL
# Solution: Check database credentials and host
docker-compose logs db
docker-compose exec db pg_isready -U tickets_user
Issue 3: Redis Connection Failed
bash
# Problem: Redis not responding
# Solution: Use InMemory channel for development
# In settings.py:
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
Issue 4: CORS Error
python
# Problem: Frontend cannot access API
# Solution: Add to settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True
Issue 5: Static Files Not Loading
bash
# Solution: Collect static files
python manage.py collectstatic --noinput
# Check STATIC_URL and STATIC_ROOT in settings
Issue 6: WebSocket Connection Timeout
bash
# Problem: WebSocket handshake timeout
# Solution: Increase timeout in nginx
proxy_read_timeout 300s;
proxy_connect_timeout 75s;
🗺 Roadmap
Version 1.1 (Q2 2024)
Email notifications

File attachments in chat

Export reports to PDF/Excel

Dark mode

Version 1.2 (Q3 2024)
Mobile app (React Native)

SLA management

Customer satisfaction surveys

Bulk ticket operations

Version 2.0 (Q4 2024)
AI-powered ticket routing

Knowledge base integration

Multi-language support

Advanced analytics dashboard

👥 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

Development Guidelines
bash
# Backend development
python manage.py runserver
daphne -b 0.0.0.0 -p 8000 helpdesk_backend.asgi:application

# Frontend development
npm run dev

# Run tests
python manage.py test
npm test

# Linting
flake8 accounts tickets chats
npm run lint
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

text
MIT License

Copyright (c) 2024 Helpdesk System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...

Full license text available in the repository.
💬 Support
Get Help
📧 Email: mohajmmad200@gmail.com
🐙 GitHub Issues: Create an issue

💬 Discord: Join our Discord server

📚 Documentation: Read full docs

Show Your Support
If this project helped you, please consider:

⭐ Starring the repository on GitHub

🍴 Forking the project

📢 Sharing it with others

💰 Sponsoring the project

🌟 Star History
https://api.star-history.com/svg?repos=yourusername/helpdesk-backend&type=Date

<div align="center">
Built with ❤️ by the Open Source Community

⬆ Back to Top
</div>