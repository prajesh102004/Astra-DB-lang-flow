import streamlit as st
import requests

# Streamlit App Title
st.title("🚀 Langflow Astra API - Trip Planner")

# User input
user_input = st.text_input("💬 Enter your request:", "give me 1 week pune trip plan according to todays date")

# API endpoint & headers (use st.secrets for production)
url = "https://api.langflow.astra.datastax.com/lf/3e1ee4ba-21f0-4b05-a479-14553904059c/api/v1/run/9c5bad27-1fa5-4e72-846f-1d82606dcb2c"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer AstraCS:sLdSDONIkfpMoljkUDrTEIZu:c4ab1d28cf1dc7e2b1913449188e172e66e1763d7b7efdf0e430fe895a5dd4f7"
    # For production: "Authorization": f"Bearer AstraCS:sLdSDONIkfpMoljkUDrTEIZu:{st.secrets['astra_token']}"
}

def extract_text(data):
    """Recursively find 'text', 'content', or 'message' in nested dict/list."""
    if isinstance(data, dict):
        if 'text' in data:
            return data['text']
        if 'content' in data:
            return data['content']
        if 'message' in data and isinstance(data['message'], dict):
            return data['message'].get('content') or data['message'].get('text')
        for v in data.values():
            result = extract_text(v)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = extract_text(item)
            if result:
                return result
    return None

# Button to send input
if st.button("Send to Langflow"):
    payload = {
        "input_value": user_input,
        "output_type": "chat",
        "input_type": "chat"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        # Extract text robustly
        text_output = extract_text(result)
        if text_output:
            st.success("✅ Trip Plan Generated")
            st.markdown(text_output)  # Use markdown for better formatting
        else:
            st.error("⚠️ Could not extract text from response")
            st.json(result)  # fallback: show full JSON

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API request failed: {str(e)}")
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {str(e)}")
. 