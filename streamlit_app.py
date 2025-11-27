import streamlit as st

st.title("📈 Intraday Buy/Sell Calculator (Created by Gokul Thanigaivasan)")
st.write("Groww Intraday Brokerage + Charges Auto Calculator")

# ----------------------------
# INPUTS
# ----------------------------
side = st.selectbox("Buy or Sell", ["Buy", "Sell"])
capital = st.number_input("Capital Amount (₹)", min_value=100.0, value=10000.0)
entry = st.number_input("Entry Price (₹)", min_value=0.1, value=100.0)

target_choice = st.selectbox("Select Target", [
    "Target 1 (1%)", 
    "Target 2 (3%)", 
    "Target 3 (5%)", 
    "Stop Loss (-1.5%)"
])

# ----------------------------
# TARGET CALCULATION
# ----------------------------
if target_choice == "Target 1 (1%)":
    change = 0.01
elif target_choice == "Target 2 (3%)":
    change = 0.03
elif target_choice == "Target 3 (5%)":
    change = 0.05
else:
    change = -0.015  # Stop Loss

if side == "Buy":
    exit_price = entry * (1 + change)
else:
    exit_price = entry * (1 - change)

# ----------------------------
# QTY CALCULATION (20% margin)
# ----------------------------
effective_capital = capital * 5      # 20% margin = 5X exposure
qty = int(effective_capital // entry)

st.subheader("📌 Quantity & Target")
st.write(f"**Qty:** {qty}")
st.write(f"**Exit Price:** ₹{exit_price:.2f}")

# ----------------------------
# GROSS PROFIT / LOSS
# ----------------------------
if side == "Buy":
    gross_pl = (exit_price - entry) * qty
else:
    gross_pl = (entry - exit_price) * qty

# ----------------------------
# BROKERAGE & CHARGES (Groww)
# ----------------------------
buy_value  = entry * qty
sell_value = exit_price * qty

# brokerage
brokerage_buy  = min(20, 0.001 * buy_value)
brokerage_sell = min(20, 0.001 * sell_value)

# STT (only on sell)
stt = 0.00025 * sell_value

# stamp duty (only buy)
stamp = 0.00003 * buy_value

# exchange charges (both)
exch = 0.00002997 * (buy_value + sell_value)

# sebi charges (both)
sebi = 0.000001 * (buy_value + sell_value)

# IPFT charges
ipft = 0.000001 * (buy_value + sell_value)

# GST on brokerage + exchange
gst = 0.18 * (brokerage_buy + brokerage_sell + exch)

total_charges = (
    brokerage_buy + brokerage_sell + stt + stamp +
    exch + sebi + ipft + gst
)

net_pl = gross_pl - total_charges

# ----------------------------
# OUTPUT
# ----------------------------
st.subheader("📊 Groww Intraday Charges")
st.write(f"**Brokerage (Buy + Sell): ₹{brokerage_buy + brokerage_sell:.2f}**")
st.write(f"**STT (Sell only): ₹{stt:.2f}**")
st.write(f"**Stamp Duty (Buy only): ₹{stamp:.2f}**")
st.write(f"**Exchange Charges: ₹{exch:.2f}**")
st.write(f"**SEBI Charges: ₹{sebi:.2f}**")
st.write(f"**IPFT Charges: ₹{ipft:.2f}**")
st.write(f"**GST: ₹{gst:.2f}**")

st.subheader("💰 Final P&L Summary")
st.write(f"**Gross P&L:** ₹{gross_pl:.2f}")
st.write(f"**Total Charges:** ₹{total_charges:.2f}")
st.write(f"### ✅ Net P&L After Charges: ₹{net_pl:.2f}")
