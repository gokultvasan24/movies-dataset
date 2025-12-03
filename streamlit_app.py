import streamlit as st

st.set_page_config(layout="wide")

st.title("📈 Groww Trading Calculator (Created by Gokul Thanigaivasan)")
st.write("Intraday & Equity Brokerage + Charges Calculator")

# ----------------------------
# SIDEBAR FOR INPUTS
# ----------------------------
with st.sidebar:
    st.header("📋 Trade Details")
    
    trade_type = st.selectbox("Trade Type", ["Intraday", "Equity"])
    side = st.selectbox("Buy or Sell", ["Buy", "Sell"])
    capital = st.number_input("Capital Amount (₹)", min_value=100.0, value=10000.0)
    entry = st.number_input("Entry Price (₹)", min_value=0.1, value=100.0)
    
    target_choice = st.selectbox("Select Target", [
        "Target 1 (1%)", 
        "Target 2 (3%)", 
        "Target 3 (5%)", 
        "Stop Loss (-1%)",
        "Custom Target (Manual)"
    ])
    
    if target_choice == "Custom Target (Manual)":
        custom_target = st.number_input("Enter Custom Target Percentage (%)", 
                                         min_value=-100.0, 
                                         max_value=1000.0, 
                                         value=2.0,
                                         format="%.2f")
        change = custom_target / 100
    elif target_choice == "Target 1 (1%)":
        change = 0.01
    elif target_choice == "Target 2 (3%)":
        change = 0.03
    elif target_choice == "Target 3 (5%)":
        change = 0.05
    else:  # Stop Loss (-1%)
        change = -0.01
    
    # Quantity calculation
    if trade_type == "Intraday":
        effective_capital = capital * 5  # 20% margin = 5X exposure
    else:
        effective_capital = capital  # No margin for equity delivery
    
    qty = int(effective_capital // entry)
    
    # Exit price calculation
    if side == "Buy":
        exit_price = entry * (1 + change)
    else:
        exit_price = entry * (1 - change)
    
    st.subheader("Trade Summary")
    st.write(f"**Trade Type:** {trade_type}")
    st.write(f"**Quantity:** {qty} shares")
    st.write(f"**Entry Price:** ₹{entry:.2f}")
    st.write(f"**Exit Price:** ₹{exit_price:.2f}")

# ----------------------------
# MAIN CONTENT AREA - TWO COLUMNS
# ----------------------------
col1, col2 = st.columns(2)

# Column 1: Intraday Calculator
with col1:
    st.header("📊 Intraday Trading")
    
    if trade_type == "Intraday":
        st.success("**ACTIVE MODE** - Calculating Intraday Charges")
    else:
        st.info("Reference Mode - Showing Intraday Charges")
    
    # Calculate values for intraday
    buy_value_intra = entry * qty if side == "Buy" else exit_price * qty
    sell_value_intra = exit_price * qty if side == "Buy" else entry * qty
    
    # Intraday Brokerage (Groww)
    brokerage_buy_intra = min(20, 0.0001 * buy_value_intra) if trade_type == "Intraday" else 0  # 0.01% for intraday
    brokerage_sell_intra = min(20, 0.0001 * sell_value_intra) if trade_type == "Intraday" else 0
    
    # STT (only on sell for intraday)
    stt_intra = 0.00025 * sell_value_intra if side == "Buy" else 0.00025 * buy_value_intra
    
    # Stamp duty (only buy)
    stamp_intra = 0.00003 * buy_value_intra if side == "Buy" else 0.00003 * sell_value_intra
    
    # Exchange charges (NSE)
    exch_intra = 0.0000297 * (buy_value_intra + sell_value_intra)
    
    # SEBI charges
    sebi_intra = 0.000001 * (buy_value_intra + sell_value_intra)
    
    # IPFT charges (NSE)
    ipft_intra = 0.000001 * (buy_value_intra + sell_value_intra)
    
    # GST on brokerage + exchange
    gst_intra = 0.18 * (brokerage_buy_intra + brokerage_sell_intra + exch_intra)
    
    total_charges_intra = (
        brokerage_buy_intra + brokerage_sell_intra + stt_intra + stamp_intra +
        exch_intra + sebi_intra + ipft_intra + gst_intra
    )
    
    # Gross P&L for intraday
    if side == "Buy":
        gross_pl_intra = (exit_price - entry) * qty
    else:
        gross_pl_intra = (entry - exit_price) * qty
    
    net_pl_intra = gross_pl_intra - total_charges_intra
    
    # Display intraday charges
    st.subheader("Intraday Charges Breakdown")
    
    st.write("**Brokerage**")
    st.write(f"- Buy (0.01% or ₹20 max): ₹{brokerage_buy_intra:.2f}")
    st.write(f"- Sell (0.01% or ₹20 max): ₹{brokerage_sell_intra:.2f}")
    st.write(f"**Total Brokerage: ₹{brokerage_buy_intra + brokerage_sell_intra:.2f}**")
    
    st.write("**Taxes & Charges**")
    st.write(f"- STT (0.025% on sell): ₹{stt_intra:.2f}")
    st.write(f"- Stamp Duty (0.003% on buy): ₹{stamp_intra:.2f}")
    st.write(f"- Exchange Charges (NSE 0.00297%): ₹{exch_intra:.2f}")
    st.write(f"- SEBI Charges (0.0001%): ₹{sebi_intra:.2f}")
    st.write(f"- IPFT Charges (0.0001%): ₹{ipft_intra:.2f}")
    st.write(f"- GST (18% on brokerage + exchange): ₹{gst_intra:.2f}")
    
    st.write("**Summary**")
    st.write(f"**Total Charges: ₹{total_charges_intra:.2f}**")
    st.write(f"**Gross P&L: ₹{gross_pl_intra:.2f}**")
    st.write(f"### 🎯 **Net P&L: ₹{net_pl_intra:.2f}**")
    
    if trade_type == "Intraday":
        st.balloons()

# Column 2: Equity/Delivery Calculator
with col2:
    st.header("🏦 Equity Delivery Trading")
    
    if trade_type == "Equity":
        st.success("**ACTIVE MODE** - Calculating Equity Delivery Charges")
    else:
        st.info("Reference Mode - Showing Equity Delivery Charges")
    
    # Calculate values for equity delivery
    # For equity delivery, we need to consider actual quantity based on capital (no margin)
    qty_equity = int(capital // entry)
    buy_value_eq = entry * qty_equity if side == "Buy" else exit_price * qty_equity
    sell_value_eq = exit_price * qty_equity if side == "Buy" else entry * qty_equity
    
    # Equity Brokerage (Groww - Zero brokerage for equity delivery)
    brokerage_buy_eq = 0
    brokerage_sell_eq = 0
    
    # STT (0.1% on buy and sell for equity delivery)
    stt_eq = 0.001 * (buy_value_eq + sell_value_eq)
    
    # Stamp duty (0.015% on buy for equity)
    stamp_eq = 0.00015 * buy_value_eq if side == "Buy" else 0.00015 * sell_value_eq
    
    # Exchange charges (NSE)
    exch_eq = 0.0000297 * (buy_value_eq + sell_value_eq)
    
    # SEBI charges
    sebi_eq = 0.000001 * (buy_value_eq + sell_value_eq)
    
    # IPFT charges (NSE)
    ipft_eq = 0.000001 * (buy_value_eq + sell_value_eq)
    
    # DP Charges (per sell transaction)
    dp_charges = 0
    if (side == "Buy" and exit_price < entry) or (side == "Sell" and exit_price > entry):
        # This is a sell transaction scenario
        dp_charges = 16.5  # Groww DP charges
    
    # GST on brokerage + exchange (brokerage is 0, so only on exchange)
    gst_eq = 0.18 * (brokerage_buy_eq + brokerage_sell_eq + exch_eq)
    
    total_charges_eq = (
        brokerage_buy_eq + brokerage_sell_eq + stt_eq + stamp_eq +
        exch_eq + sebi_eq + ipft_eq + gst_eq + dp_charges
    )
    
    # Gross P&L for equity
    if side == "Buy":
        gross_pl_eq = (exit_price - entry) * qty_equity
    else:
        gross_pl_eq = (entry - exit_price) * qty_equity
    
    net_pl_eq = gross_pl_eq - total_charges_eq
    
    # Display equity charges
    st.subheader("Equity Delivery Charges Breakdown")
    
    st.write("**Brokerage**")
    st.write(f"- Buy: ₹0 (Zero Brokerage)")
    st.write(f"- Sell: ₹0 (Zero Brokerage)")
    st.write(f"**Total Brokerage: ₹0.00**")
    
    st.write("**Taxes & Charges**")
    st.write(f"- STT (0.1% on both sides): ₹{stt_eq:.2f}")
    st.write(f"- Stamp Duty (0.015% on buy): ₹{stamp_eq:.2f}")
    st.write(f"- Exchange Charges (NSE 0.00297%): ₹{exch_eq:.2f}")
    st.write(f"- SEBI Charges (0.0001%): ₹{sebi_eq:.2f}")
    st.write(f"- IPFT Charges (0.0001%): ₹{ipft_eq:.2f}")
    st.write(f"- GST (18% on exchange): ₹{gst_eq:.2f}")
    
    if dp_charges > 0:
        st.write(f"- DP Charges (Groww): ₹{dp_charges:.2f}")
    else:
        st.write("- DP Charges (Groww): ₹0.00")
    
    st.write("**Summary**")
    st.write(f"**Quantity (No Margin):** {qty_equity} shares")
    st.write(f"**Total Charges: ₹{total_charges_eq:.2f}**")
    st.write(f"**Gross P&L: ₹{gross_pl_eq:.2f}**")
    st.write(f"### 🏦 **Net P&L: ₹{net_pl_eq:.2f}**")
    
    if trade_type == "Equity":
        st.balloons()

# ----------------------------
# COMPARISON SECTION
# ----------------------------
st.markdown("---")
st.header("📊 Comparison: Intraday vs Equity Delivery")

comp_col1, comp_col2, comp_col3 = st.columns(3)

with comp_col1:
    st.metric("Intraday Net P&L", f"₹{net_pl_intra:.2f}", 
              f"{((net_pl_intra/capital)*100):.2f}%" if capital > 0 else "0%")
    
with comp_col2:
    st.metric("Equity Delivery Net P&L", f"₹{net_pl_eq:.2f}", 
              f"{((net_pl_eq/capital)*100):.2f}%" if capital > 0 else "0%")

with comp_col3:
    difference = net_pl_intra - net_pl_eq
    st.metric("Difference (Intraday - Equity)", f"₹{difference:.2f}", 
              f"{((difference/capital)*100):.2f}%" if capital > 0 else "0%")

# ----------------------------
# CHARGE RATES REFERENCE TABLE
# ----------------------------
st.markdown("---")
st.subheader("📋 Groww Charges Reference (Based on your image)")

st.write("""
| Charge Type | Intraday Rate | Equity Delivery Rate | Applied On |
|-------------|---------------|----------------------|------------|
| **Brokerage** | 0.01% or ₹20 per order | ₹0 (Zero Brokerage) | Both sides |
| **STT** | 0.025% | 0.1% | Sell side only for intraday, Both sides for equity |
| **Stamp Duty** | 0.003% | 0.015% | Buy side only |
| **Exchange Charge** | 0.00297% (NSE) | 0.00297% (NSE) | Both sides |
| **SEBI Charge** | 0.0001% | 0.0001% | Both sides |
| **IPFT Charge** | 0.0001% | 0.0001% | Both sides |
| **GST** | 18% on brokerage + exchange | 18% on exchange | Both sides |
| **DP Charges** | Not applicable | ₹16.5 per sell transaction | Sell side only |
""")

st.info("💡 **Note:** The calculator automatically switches to ACTIVE mode based on your selected trade type. The other mode shows reference calculations.")
