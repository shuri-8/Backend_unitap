from app import database, models

db = next(database.get_db())

models.Base.metadata.create_all(bind=database.engine)

# Add demo users
user1 = models.User(name="Aarav Singh", rfid="RFID123456", balance=500.00, status="active")
user2 = models.User(name="Meera Sharma", rfid="RFID654321", balance=1200.00, status="active")

db.add_all([user1, user2])
db.commit()

print("Demo users added!")
