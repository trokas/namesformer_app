import streamlit as st
import requests

# Flask app URL (adjust if running on a different host or port)
FLASK_APP_URL = "http://127.0.0.1:5000"

def generate_name(start_str):
    """Call the Flask app to generate a name based on the starting letter."""
    response = requests.post(f"{FLASK_APP_URL}/generate_name", json={"start_str": start_str})
    if response.status_code == 200:
        return response.json()
    else:
        return None

def vote(name_id, vote_type):
    """Send an upvote or downvote for a name to the Flask app."""
    response = requests.post(f"{FLASK_APP_URL}/vote", json={"id": name_id, "vote_type": vote_type})
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_names():
    """Fetch the list of names from the Flask app and sort them by votes."""
    response = requests.get(f"{FLASK_APP_URL}/get_names")
    if response.status_code == 200:
        names = response.json()
        # Sort the names by votes (descending order)
        sorted_names = sorted(names, key=lambda x: x['votes'], reverse=True)
        return sorted_names
    else:
        return []

# UI for name generation
start_letter = st.text_input("Enter a starting letter:", max_chars=1)
new_name = ""
if st.button("Generate Name"):
    result = generate_name(start_letter)
    if result and result.get("success"):
        new_name = result.get('name')  # Store the new name
        st.success(f"Generated name: {new_name}")
    else:
        st.error("Failed to generate a name.")

# Display list of names with upvote/downvote buttons and vote counts
st.header("Names List")
names = get_names()
for name in names:
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        if name["name"] == new_name:
            # Highlight the newly added name
            st.markdown(f"**{name['name']} (New!)**")
        else:
            st.write(name["name"])
    with col2:
        st.write(f"Votes: {name['votes']}")
    with col3:
        if st.button("👍", key=f"up_{name['id']}"):
            vote(name["id"], "upvote")
            st.experimental_rerun()
    with col4:
        if st.button("👎", key=f"down_{name['id']}"):
            vote(name["id"], "downvote")
            st.experimental_rerun()
