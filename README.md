# Django Authentication Loyihasi

Bu loyiha Django asosida yozilgan autentifikatsiya (login/logout, JWT tokenlar bilan) tizimi. Loyihada foydalanuvchilar ro‘yxatdan o‘tishi, tizimga kirishi, chiqishi (logout) va tokenlar bilan ishlash imkoniyati mavjud.

---

## Loyihani o‘rnatish va ishga tushirish

Quyidagi bosqichlarni bajarib loyiha ishga tushiriladi.

### 1. Loyihani klonlash

```bash
git clone https://github.com/abduvalimurodullayev1/Authentication.git
cd Authentication


python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt


sudo -u postgres psql

CREATE DATABASE authentication_db;
CREATE USER auth_user WITH PASSWORD 'password123';
ALTER ROLE auth_user SET client_encoding TO 'utf8';
ALTER ROLE auth_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE auth_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE authentication_db TO auth_user;
\q

python manage.py migrate


python manage.py runserver
