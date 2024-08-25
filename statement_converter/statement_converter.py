import streamlit as st
from sources.sbi.sbi_tabs import display_sbi_tabs

# Set up the Streamlit page
st.set_page_config(page_title="Credit Card Statement Converter", page_icon="💳")

# Main title
st.title("Credit Card Statement Converter")

# Bank selector
bank = st.selectbox("Select your bank", ["State Bank of India"], index=0)

# Display tabs based on selected bank
if bank == "State Bank of India":
    display_sbi_tabs()

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by [@MishraMishry](https://x.com/MishraMishry)")
st.markdown(
    "Psst! This app is open source. Check out the [GitHub repo](https://github.com/SarthakMishra/simple-business-tools) if you're into that sort of thing. 😉"
)
