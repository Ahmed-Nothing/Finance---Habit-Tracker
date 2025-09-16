import streamlit as st
import matplotlib.pyplot as plt
import json
import os

class User:
 def __init__(self,username,password):
  self.__username = username
  self.__password = password
  self.transactions = []
  self.habits = []
  self.points = 0

def check_login(self,username,password):
 return self.__username==username and self.__password==password

#===Transaction Class===#

class Transaction:
 def __init__(self,amount,category,date): #Parent Class
  self.amount=amount
  self.category=category
  self.date=date

 def get_type(self):
  return "Transaction"

class Income(Transaction): #Child Class
 def __init__(self,amount,category,date):  
  super().__init__(amount,category,date)
 def get_type(self):
  return "Income"

class Expense(Transaction): #Child Class
 def __init__(self,amount,category,date):
  super().__init__(amount,category,date)
 def get_type(self):
  return "Expense"
 
# === Habit Class=== # 

class Habit:
 def __init__(self,h_name,h_type):
  self.h_name=h_name
  self.h_type=h_type

 def get_points(self):
  return 0

class GoodHabit(Habit):
 def __init__(self,h_name):
  super().__init__(h_name,"Good")
 def get_points(self):
  return 10

class BadHabit(Habit):
 def __init__(self,h_name):
  super().__init__(h_name,"Bad")
 def get_points(self):
  return -5



# === Streamlit === #
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "transactions" not in st.session_state:
    st.session_state["transactions"] = []
if "habits" not in st.session_state:
    st.session_state["habits"] = []

st.header("💰Finance & Habit Tracker🎯")

# === Helper functions ===
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists("users.json"):
        return {}
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, reset it
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

users = load_users()


# === Signup/Login ===
menu = st.sidebar.selectbox("Go To", ["Signup", "Login", "Transactions", "Habits", "Dashboard"])

if menu == "Signup":
    st.markdown("""
                       Turn :rainbow[ habits ] into points, and  :rainbow[ money ] into clarity
        """
    )
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        if new_user in users:
            st.error("Username already exists ❌")
        else:
            users[new_user] = {"password": new_pass, "transactions": [], "habits": []}
            save_users(users)
            st.success("Account created! ✅")

elif menu == "Login":
    st.markdown("""
                       Turn :rainbow[ habits ] into points, and  :rainbow[ money ] into clarity
        """
    )
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.success("Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            # Load user-specific data into session
            st.session_state["transactions"] = users[username].get("transactions", [])
            st.session_state["habits"] = users[username].get("habits", [])
        else:
            st.error("Invalid username or password")



elif menu == "Transactions":
    if not st.session_state["logged_in"]:
        st.warning("🚫 Please login to access Transactions.")
    else:
        st.subheader("💰 Transactions")
        st.write("Here you’ll add incomes & expenses.")
        a=st.number_input("Amount", min_value=1)
        c=st.text_input("Category")
        d=st.date_input("Date")
        t=st.selectbox("Type",["Income","Expense"])
        if st.button("Add Transaction"):
         if t=="Income":
          trn = {
            "amount": a,
            "category": c,
            "date": str(d),   # save as string for JSON
            "type": t
            }
         else:
          trn = {
            "amount": a,
            "category": c,
            "date": str(d),   # save as string for JSON
            "type": t
            }
        

          # Save in session
         st.session_state["transactions"].append(trn)
         st.success(f"{t} added successfully ✅")

          # --- Display Transactions ---
        if st.session_state["transactions"]:
            st.write("### Transactions")
        data = []
        for t in st.session_state["transactions"]:
            data.append({
            "Date": t["date"],
            "Amount": t["amount"],
            "Category": t["category"],
            "Type": t["type"]
            })
        st.table(data)

        
         # 🔴 Reset Button
        if st.button("Reset Transactions"):
         st.session_state["transactions"].clear()
         st.warning("All transactions cleared.")
        

elif menu == "Habits":
    if not st.session_state["logged_in"]:
        st.warning("🚫 Please login to access Habits Page.")
    else:
        st.subheader("🎯 Habits")
        st.write("Here you’ll add and track habits.")
        n=st.text_input("Habit Name")
        ht=st.selectbox("Habit Type",["Good","Bad"])
        if st.button("Add Habit"):
         if ht=="Good": 
          hbt = {"name": n, "type": "Good", "points": 10}
          st.balloons()
          st.success("Good habit added! 🎉")
         else: 
          hbt = {"name": n, "type": "Bad", "points": -5}
          st.warning("Bad habit added! 😞")
        
     
         # Save in session
         st.session_state["habits"].append(hbt)
         
           # --- Display Habits ---
        if st.session_state["habits"]:
            st.write("### Habits")

    # Convert objects → dicts only for table
            data = []
            for h in st.session_state["habits"]:
                data.append({
                "Name": h["name"],
                "Type": h["type"],
                "Points": h["points"]
                })
            st.table(data)

        else:
            st.info("No habits yet. Add one above.")

        # 🔴 Reset Button
        if st.button("Reset Habits"):
         st.session_state["habits"].clear()
         st.warning("All habits cleared.")        


elif menu == "Dashboard":
    if not st.session_state["logged_in"]:
        st.warning("🚫 Please login to see Dashboard.")
    else:
        st.subheader("📊 Dashboard")

        # ===== Finance Summary =====
        total_income = 0
        total_expense = 0
        for txn in st.session_state["transactions"]:
            if txn["type"] == "Income":
                total_income += txn["amount"]
            else:
                total_expense += txn["amount"]
        balance = total_income - total_expense

        st.metric("💰 Total Income", f"{total_income}")
        st.metric("💸 Total Expense", f"{total_expense}")
        st.metric("📊 Net Balance", f"{balance}")
        
# === Add Pie Chart Here ===

        if total_income>0 or total_expense>0:
            labels = ["Income", "Expense"]
            values = [total_income, total_expense]
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct="%1.1f%%")
            st.pyplot(fig)  
    	
        # ===== Habit Summary =====
        good_count = 0
        bad_count = 0
        total_points = 0
        for habit in st.session_state["habits"]:
            if habit["type"] == "Good":
                good_count += 1
            else:
                bad_count += 1
            total_points += habit["points"]


        st.metric("🌟 Good Habits", f"{good_count}")
        st.metric("⚠️ Bad Habits", f"{bad_count}")
        st.metric("🏆 Total Points", f"{total_points}")
    # === Habit Bar Chart ===
        if good_count > 0 or bad_count > 0:
            labels = ["Good", "Bad"]
            values = [good_count, bad_count]
            fig, ax = plt.subplots()
            ax.bar(labels, values, color=["green", "red"])
            st.pyplot(fig)

if st.session_state.get("logged_in", False):

    if st.sidebar.button("🚪 Logout"):
        username = st.session_state["username"]

        # Try to get password safely
        old_password = users.get(username, {}).get("password", st.session_state.get("password", ""))

        # Save user data with password
        users[username] = {
            "password": old_password,
            "transactions": st.session_state.get("transactions", []),
            "habits": st.session_state.get("habits", [])
        }
        save_users(users)

        st.session_state.clear()
        st.info("You have been logged out.")
        st.stop()
