# Ad Management Project

This project allows users to create and like ads. When a user registers, they can create an ad. Other users can like ads, which will trigger a Kafka message indicating that the user has liked a specific ad. Users can log out, which will store their JWT token in Redis for 30 minutes, preventing the same token from being reused by adding it to a blacklist. By default, a registered user is not an admin, but an admin can be added in the initial setup. Admins can manage users and ad types in addition to creating and liking ads.

## Features
- User registration
- Ad creation
- Liking ads (with Kafka integration)
- User logout (with Redis JWT blacklist)
- Admin management of users and ad types

## Local Setup

#### 1. Clone repo on your machine
  ```bash
  git clone https://github.com/StipeKordic/FreelanceFastAPI
```

#### 2. Create and configure .env file
   In .env_example file you can see how it should look like

#### 3. Create initial_setup.py file for initial database data. (Optional)   
Here is example how initial_setup.py could look like:
   ```bash
  import utils
from models import User, AdType
from database import SessionLocal

db = SessionLocal()



password = utils.hash("12345678")
new_admin = User(username="admin", password=password, email="admin@mail.com", is_admin=True)
db.add(new_admin)
db.commit()

password = utils.hash("12345678")
new_user = User(username="user", password=password, email="user@mail.com", is_admin=False)
db.add(new_user)
db.commit()


new_adtype = AdType(ad_type="Ad type 1", description="Ad type 1 description", price=100)
db.add(new_adtype)
db.commit()

db.close()
```

#### 4. Create docker containers
  Type:
  ```bash
  docker-compose up -d
```



