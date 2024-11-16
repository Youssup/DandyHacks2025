import bcrypt
import base64
from typing import Union
from fastapi import FastAPI
from backend.models.models import User  # Assuming the User class is defined in app.models
from db.supabase import create_supabase_client

app = FastAPI()

# Initialize supabase client
supabase = create_supabase_client()

def user_exists(key: str = "username", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

# Testing Connection
@app.get("/")
def testing():
    return "Connection Successful"

# Create a new user
@app.post("/create_user")
def create_user(user: User):
    try:
        # Hash password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        # Convert hashed password to a base64 string
        hashed_password_base64 = base64.b64encode(hashed_password).decode('utf-8')

        # Check if user already exists
        if user_exists(value=user.username):
            return {"message": "User already exists"}

        # Add user to the users table
        response = supabase.from_("users")\
            .insert({
                "username": user.username,
                "password": hashed_password_base64,  # Store the base64 string
                "rating": user.rating,
                "games_played": user.games_played,
                "wins": user.wins,
                "losses": user.losses
            })\
            .execute()

        return {"message": "User created successfully"}

    except Exception as e:
        print("Error: ", e)
        return {"message": "User creation failed", "error": str(e)}
    
# Retrieve all users
@app.get("/users")
def get_all_users():
    try:
        # Query all users
        users = supabase.from_("users")\
            .select("id", "username", "rating", "games_played", "wins", "losses")\
            .execute()

        if users.data:  # Check if user data is returned
            return users.data  # Return all users' data
        else:
            return {"message": "No users found"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "An error occurred while retrieving user data"}
    
# Update user
@app.post("/update_user")
def update_user(user: User):
    try:
        # Check if user exists
        if not user_exists(value=user.username):
            return {"message": "User does not exist"}

        # Update user data
        response = supabase.from_("users")\
            .update({
                "rating": user.rating,
                "games_played": user.games_played,
                "wins": user.wins,
                "losses": user.losses
            })\
            .eq("username", user.username)\
            .execute()

        return {"message": "User updated successfully"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "An error occurred while updating user data"}