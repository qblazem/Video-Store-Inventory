from database.customers import get_customer
from database.database import supabase


#database connection test
try:
    response = (
        supabase.table("Customers")
        .select("*")
        .limit(5)
        .execute()
    )

    print("Database connected successfully!")
    print(response.data)

except Exception as e:
    print("Database connection failed:", e)