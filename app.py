import streamlit as st
from datetime import datetime, time
import pandas as pd

# Page configuration
st.set_page_config(page_title="Baby Sleep Coach", page_icon="🌙", layout="wide")

# Session state to store data
if "sleep_data" not in st.session_state:
    st.session_state.sleep_data = pd.DataFrame(columns=["Date", "Bedtime", "Wakeup Time", "Nap Duration", "Notes"])
if "milestones" not in st.session_state:
    st.session_state.milestones = []

# Helper functions
def log_sleep(bedtime, wakeup_time, nap_duration, notes):
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Bedtime": bedtime,
        "Wakeup Time": wakeup_time,
        "Nap Duration": nap_duration,
        "Notes": notes,
    }
    st.session_state.sleep_data = st.session_state.sleep_data.append(new_entry, ignore_index=True)

def add_milestone(milestone):
    st.session_state.milestones.append({"Date": datetime.now().strftime("%Y-%m-%d"), "Milestone": milestone})

# Main app
def main():
    st.title("🌙 Baby Sleep Coach")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Sleep Tracker", "Sleep Plan", "Milestones"])

    if page == "Home":
        st.header("Welcome to Baby Sleep Coach!")
        st.write("This app helps you track your baby's sleep patterns, create personalized sleep plans, and log developmental milestones.")
        st.image("https://via.placeholder.com/800x400.png?text=Sleep+Coach+App", use_column_width=True)

    elif page == "Sleep Tracker":
        st.header("Sleep Tracker")
        st.write("Log your baby's sleep details below.")

        col1, col2 = st.columns(2)
        with col1:
            bedtime = st.time_input("Bedtime", value=time(20, 0))
        with col2:
            wakeup_time = st.time_input("Wakeup Time", value=time(7, 0))

        nap_duration = st.slider("Nap Duration (hours)", 0.5, 4.0, 1.5)
        notes = st.text_area("Notes (e.g., fussiness, feeding)")

        if st.button("Log Sleep"):
            log_sleep(bedtime, wakeup_time, nap_duration, notes)
            st.success("Sleep logged successfully!")

        st.subheader("Sleep History")
        st.dataframe(st.session_state.sleep_data)

    elif page == "Sleep Plan":
        st.header("Personalized Sleep Plan")
        st.write("Based on your baby's sleep patterns, here's a recommended sleep plan.")

        if not st.session_state.sleep_data.empty:
            avg_bedtime = pd.to_datetime(st.session_state.sleep_data["Bedtime"]).mean().time()
            avg_wakeup = pd.to_datetime(st.session_state.sleep_data["Wakeup Time"]).mean().time()
            avg_nap_duration = st.session_state.sleep_data["Nap Duration"].mean()

            st.write(f"**Recommended Bedtime:** {avg_bedtime.strftime('%I:%M %p')}")
            st.write(f"**Recommended Wakeup Time:** {avg_wakeup.strftime('%I:%M %p')}")
            st.write(f"**Recommended Nap Duration:** {avg_nap_duration:.1f} hours")
        else:
            st.warning("No sleep data available. Please log some sleep entries first.")

    elif page == "Milestones":
        st.header("Milestones Tracker")
        st.write("Log your baby's developmental milestones here.")

        milestone = st.text_input("Enter a milestone (e.g., 'Started crawling')")
        if st.button("Add Milestone"):
            add_milestone(milestone)
            st.success("Milestone added!")

        st.subheader("Milestones History")
        for milestone in st.session_state.milestones:
            st.write(f"{milestone['Date']}: {milestone['Milestone']}")

# Run the app
if __name__ == "__main__":
    main()
