import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Web Calculator", layout="centered")

st.title("🧮 Simple Web Calculator")

# Handle reset early
if "reset_triggered" not in st.session_state:
    st.session_state.reset_triggered = False

if st.session_state.reset_triggered:
    st.session_state.num1 = 0.0
    st.session_state.num2 = 0.0
    st.session_state.operation = "Choose"
    st.session_state.reset_triggered = False
    st.rerun()  # restart app after clearing

# Input fields
num1 = st.number_input("Enter first number (using the keyboard):", format="%.2f", key="num1")
num2 = st.number_input("Enter second number (using the keyboard):", format="%.2f", key="num2")


# Operation selector
operation = st.selectbox("Choose Operation", ["Choose", "Add", "Subtract", "Multiply", "Divide"], 
                         index=0, key="operation")

# Calculate result
if st.button("Calculate"):
    if operation == "Choose":
        st.error("❌ Please Choose operation to perform! ")
        result = None
    elif operation == "Add":
        result = num1 + num2
        symbol = "+"
    elif operation == "Subtract":
        result = num1 - num2
        symbol = "-"
    elif operation == "Multiply":
        result = num1 * num2
        symbol = "×"
    elif operation == "Divide":
        if num2 == 0:
            st.error("❌ Cannot divide by zero!")
            result = None
        else:
            result = num1 / num2
            symbol = "÷"

    if result is not None:
        st.success(f"✅ {num1} {symbol} {num2} = {result}")
        # Append to history
        with open("history.txt", "a") as f:
            f.write(f"{num1},{num2},{operation},{result}\n")

# Reset calculator values
if st.button("🔁 Reset Calculator"):
    st.session_state.reset_triggered = True
    st.rerun()


# View history
if st.button("📖 View History"):
    if os.path.exists("history.txt") and os.path.getsize("history.txt") > 0:
        df = pd.read_csv("history.txt", header=None, names=["Num1", "Num2", "Operation", "Answer"])
        st.dataframe(df)
    else:
        st.info("📭 No history found.")

# Clear history
if st.button("🧹 Clear History"):
    open("history.txt", "w").close()
    st.info("✅ History cleared.")

