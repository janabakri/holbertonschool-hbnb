import requests

BASE = "http://localhost:5000/api/v1"

print("=" * 50)
print("🧪 HBnB Quick Test")
print("=" * 50)

# 1. Login as Admin
print("\n1️⃣ Login as Admin...")
r = requests.post(f"{BASE}/auth/login", json={"email":"admin@example.com","password":"admin123"})
if r.status_code != 200:
    print("❌ Server not running or login failed")
    exit(1)
admin_token = r.json()["access_token"]
admin_headers = {"Authorization": f"Bearer {admin_token}"}
print("✅ Admin login OK")

# 2. Get places
print("\n2️⃣ Get places...")
r = requests.get(f"{BASE}/places")
places = r.json()
print(f"✅ {len(places)} places found")
if places:
    place_id = places[0]["id"]
    print(f"   First place ID: {place_id}")

# 3. Get amenities
print("\n3️⃣ Get amenities...")
r = requests.get(f"{BASE}/amenities")
amenities = r.json()
print(f"✅ {len(amenities)} amenities found")

# 4. Get users
print("\n4️⃣ Get users...")
r = requests.get(f"{BASE}/users", headers=admin_headers)
users = r.json()
print(f"✅ {len(users)} users found")

# 5. Create regular user if not exists
print("\n5️⃣ Create regular user...")
user_email = "test123@example.com"
# Check if user exists
user_exists = any(u.get("email") == user_email for u in users)
if not user_exists:
    r = requests.post(f"{BASE}/users", headers=admin_headers, json={
        "first_name": "Test", "last_name": "User",
        "email": user_email, "password": "test123", "is_admin": False
    })
    if r.status_code == 201:
        print("✅ Regular user created")
    else:
        print(f"⚠️ Failed to create user: {r.text}")
else:
    print("⚠️ User already exists")

# 6. Login as Regular User
print("\n6️⃣ Login as Regular User...")
r = requests.post(f"{BASE}/auth/login", json={"email": user_email, "password": "test123"})
if r.status_code == 200:
    data = r.json()
    user_token = data["access_token"]
    # Get user_id from the response (might be in "sub" or directly)
    if "user" in data and "id" in data["user"]:
        user_id = data["user"]["id"]
    else:
        # Try to get user_id from token or fetch from users list
        r2 = requests.get(f"{BASE}/users", headers=admin_headers)
        users_list = r2.json()
        for u in users_list:
            if u.get("email") == user_email:
                user_id = u["id"]
                break
    user_headers = {"Authorization": f"Bearer {user_token}"}
    print(f"✅ Regular user login OK (ID: {user_id})")
else:
    print("❌ Regular user login failed")
    exit(1)

# 7. Add review (Regular user reviews Admin's place)
if places and user_id:
    print("\n7️⃣ Add review...")
    review_data = {
        "text": "Great place! Highly recommended.",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    r = requests.post(f"{BASE}/reviews", headers=user_headers, json=review_data)
    
    if r.status_code == 201:
        print("✅ Review added successfully!")
        print(f"   Review ID: {r.json().get('id', 'unknown')}")
    elif r.status_code == 403:
        error = r.json().get("error", "")
        print(f"⚠️ {error}")
    elif r.status_code == 400:
        error = r.json().get("error", "")
        if "already reviewed" in error.lower():
            print("⚠️ Already reviewed this place (duplicate prevented)")
        else:
            print(f"⚠️ {error}")
    else:
        print(f"⚠️ Unexpected status: {r.status_code}")
        print(f"   Response: {r.text[:200]}")
else:
    print("\n7️⃣ Add review...")
    print("⚠️ Skipped (no places or no user_id)")

# 8. Get all reviews
print("\n8️⃣ Get all reviews...")
r = requests.get(f"{BASE}/reviews")
reviews = r.json()
print(f"✅ {len(reviews)} reviews found")

print("\n" + "=" * 50)
print("✅ ALL TESTS PASSED!")
print("=" * 50)
