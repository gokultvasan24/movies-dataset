import altair as alt
import pandas as pd
import streamlit as st

# ---------------------------------------------
# PAGE SETUP
# ---------------------------------------------
st.set_page_config(page_title="Intraday Trade Calculator", page_icon="📈")
st.title("📈 Intraday Trade Calculator Dashboard")

st.write(
    """
    This dashboard helps you calculate **quantity**, **targets**, and **stop-loss**
    for **intraday trading**.  
    Select **Buy/Sell**, enter **Capital** and **Entry Price**, and view results instantly.
    """
)

# ---------------------------------------------
# INPUT WIDGETS
# ---------------------------------------------
trade_type = st.selectbox("Trade Type", ["Buy", "Sell"])
capital = st.number_input("Capital Amount (₹)", min_value=1000, value=10000, step=500)
entry_price = st.number_input("Entry Price (₹)", min_value=1.0, step=0.1)

# Target percentages
targets = [1, 3, 5]
stop_loss_percent = 1.5

# ---------------------------------------------
# CALCULATIONS
# ---------------------------------------------
if entry_price > 0:

    qty = int(capital // entry_price)

    # Target price calculations
    t1 = entry_price * (1 + targets[0] / 100)
    t2 = entry_price * (1 + targets[1] / 100)
    t3 = entry_price * (1 + targets[2] / 100)

    # Stop-loss calculations
    if trade_type.lower() == "buy":
        sl = entry_price * (1 - stop_loss_percent / 100)
    else:
        sl = entry_price * (1 + stop_loss_percent / 100)

    # ---------------------------------------------
    # CREATE RESULT DATAFRAME
    # ---------------------------------------------
    df = pd.DataFrame(
        {
            "Level": ["Entry Price", "Target 1 (+1%)", "Target 2 (+3%)", "Target 3 (+5%)", "Stop-Loss (-1.5%)"],
            "Price (₹)": [
                entry_price,
                t1,
                t2,
                t3,
                sl
            ],
        }
    )

    # ---------------------------------------------
    # DISPLAY RESULT TABLE
    # ---------------------------------------------
    st.subheader("📊 Trade Levels")
    st.dataframe(
        df,
        use_container_width=True,
        column_config={"Price (₹)": st.column_config.NumberColumn("Price (₹)", format="₹%.2f")}
    )

    # ---------------------------------------------
    # ALTair CHART
    # ---------------------------------------------
    st.subheader("📉 Visual Chart")

    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Level:N", title="Trade Levels"),
            y=alt.Y("Price (₹):Q", title="Price (₹)"),
            color=alt.value("#4e79a7"),
        )
        .properties(height=320)
    )

    st.altair_chart(chart, use_container_width=True)

    # ---------------------------------------------
    # QUANTITY DISPLAY
    # ---------------------------------------------
    st.subheader("🧮 Quantity You Can Buy/Sell")
    st.success(f"**You can trade:** {qty} shares")

else:
    st.warning("Enter a valid entry price.")

# ---------------------------------------------
# FOOTER CREDIT
# ---------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:14px; color:gray;'>"
    "Created by <b>Gokul Thanigaivasan</b>"
    "</p>",
    unsafe_allow_html=True
)
