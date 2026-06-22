import streamlit as st
import difflib
from datetime import datetime

# Website ka Title aur Layout set karna
st.set_page_config(page_title="Python Restaurant", page_icon="🍔", layout="centered")

st.title("🍔 Python Restaurant Billing System")
st.write("Welcome to the smartest web-based billing software!")

# Master Menu aur Password ko browser ki memory (Session State) mein save rakhna
if "menu" not in st.session_state:
    st.session_state.menu = {"samosa": 20, "chai": 10, "burger": 50, "pizza": 120, "coffee": 30}
if "current_bill" not in st.session_state:
    st.session_state.current_bill = 0
if "order_list" not in st.session_state:
    st.session_state.order_list = []

ADMIN_PASSWORD = "1234"

# ─── SIDEBAR: ADMIN PANEL ───
st.sidebar.header("🛠️ Admin Control Panel")
admin_pass = st.sidebar.text_input("Admin Password darj karein:", type="password")

if admin_pass == ADMIN_PASSWORD:
    st.sidebar.success("Access Granted!")
    st.sidebar.subheader("Change Item Price")
    item_to_change = st.sidebar.selectbox("Select Item:", list(st.session_state.menu.keys()))
    new_price = st.sidebar.number_input("Naya Price set karein:", min_value=1, value=int(st.session_state.menu[item_to_change]))
    
    if st.sidebar.button("Update Price"):
        st.session_state.menu[item_to_change] = new_price
        st.sidebar.success(f"{item_to_change.title()} ka price Rs.{new_price} ho gaya hai!")

# ─── MAIN SCREEN: CUSTOMER SIDE ───
st.subheader("📋 Our Delicious Menu")

# Menu ko sundar columns mein dikhana
cols = st.columns(len(st.session_state.menu))
for idx, (item, price) in enumerate(st.session_state.menu.items()):
    cols[idx].metric(label=item.title(), value=f"Rs.{price}")

st.write("---")

# Customer ka Naam aur Order Input
customer_name = st.text_input("Customer ka naam likhiye:", placeholder="e.g. Rahul")

if customer_name:
    order_input = st.text_input("Aap kya order karna chahte hain? (Enter dabaen):").strip().lower()
    
    if order_input:
        if order_input in st.session_state.menu:
            price = st.session_state.menu[order_input]
            st.session_state.current_bill += price
            st.session_state.order_list.append(f"{order_input.title()} (Rs.{price})")
            st.success(f"✔ Added {order_input.title()} to cart!")
        else:
            # Smart Suggestion logic for web
            matches = difflib.get_close_matches(order_input, st.session_state.menu.keys(), n=1, cutoff=0.6)
            if matches:
                st.warning(f"🤔 Kya aapka matlab '{matches[0].title()}' tha?")
            else:
                st.error(f"❌ Sorry, hamare paas '{order_input}' available nahi hai.")

    # Cart aur Current Order Status dikhana
    if st.session_state.order_list:
        st.subheader("🛒 Aapka Cart:")
        for current_item in st.session_state.order_list:
            st.write(f"- {current_item}")
        
        st.write(f"**Current Total:** Rs.{st.session_state.current_bill}")

        # Final Bill and Discount System Button
        if st.button("🧾 Generate Final Bill"):
            original = st.session_state.current_bill
            discount = 0
            final_paid = original
            
            if original >= 100:
                discount = original * 0.10
                final_paid = original - discount
                st.balloons() # Screen par celebration balloons udane ke liye!
            
            st.write("### ============ RECEIPT ============")
            st.write(f"**Customer Name:** {customer_name.title()}")
            st.write(f"**Original Bill:** Rs.{original}")
            if discount > 0:
                st.write(f"**🎉 10% Discount Applied:** -Rs.{discount}")
            st.write(f"### 💰 Final Payable Amount: Rs.{final_paid}")
            st.write("=================================")
            
            # File me record save karna
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("all_bills.txt", "a") as file:
                file.write(f"Date: {now} | Name: {customer_name.title()} | Paid: Rs.{final_paid}\n")
            
            # Reset memory for next order
            st.session_state.current_bill = 0
            st.session_state.order_list = []
