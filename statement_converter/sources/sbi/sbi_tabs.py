import streamlit as st
from io import BytesIO
from .process_monthly_statements import process_monthly_statements
from .process_transaction_history_exports import process_transaction_history
from .utils import get_date_range_filename, sort_and_reindex_df


def display_transaction_history_tab():
    """
    Display the transaction history tab in the Streamlit app.
    This function handles file upload, processing, and displaying results for transaction history exports.
    """
    st.markdown("#### Convert exported transaction history to csv:")
    uploaded_file = st.file_uploader(
        "Upload your transaction history PDF to convert it into CSV",
        type="pdf",
    )

    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' successfully uploaded!")

        with st.spinner("Processing PDF..."):
            df = process_transaction_history(uploaded_file)

        if df is not None:
            df = sort_and_reindex_df(df)
            st.success(f"Successfully extracted {len(df)} transactions!")

            # Display transaction summary
            st.subheader("Transaction Summary")

            # Transaction statistics cards
            col1, col2, col3 = st.columns(3)
            with col1:
                with st.container(border=True):
                    st.metric("Total Transactions", len(df))
            with col2:
                with st.container(border=True):
                    st.metric(
                        "Total Debits",
                        f"₹{df['Debit (Rs.)'].sum():,.2f}",
                    )
            with col3:
                with st.container(border=True):
                    st.metric(
                        "Total Credits",
                        f"₹{df['Credit (Rs.)'].sum():,.2f}",
                    )

            # Display transaction history
            st.dataframe(df.set_index("No."), width=1000)

            # Provide download option
            csv_filename = get_date_range_filename(df)
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            st.download_button(
                label="Download Statement as CSV",
                data=csv_buffer,
                file_name=csv_filename,
                mime="text/csv",
            )

        else:
            st.error(
                "No transactions found in the uploaded PDF. Please make sure it's a valid statement."
            )
    else:
        st.info("Please upload a transaction history PDF to get started.")


def display_monthly_statements_tab():
    """
    Display the monthly statements tab in the Streamlit app.
    This function handles file upload, processing, and displaying results for monthly statement PDFs.
    """
    st.markdown("#### Convert monthly statements to csv:")
    uploaded_files = st.file_uploader(
        "Upload your monthly statement PDF(s) to convert them into CSV",
        type="pdf",
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) successfully uploaded!")

        with st.spinner("Processing PDFs..."):
            df = process_monthly_statements(uploaded_files)

        if not df.empty:
            df = sort_and_reindex_df(df)
            st.success(f"Successfully extracted {len(df)} transactions!")

            # Display transaction summary
            st.subheader("Transaction Summary:")

            # Transaction statistics cards
            col1, col2, col3 = st.columns(3)
            with col1:
                with st.container(border=True):
                    st.metric("Total Transactions", len(df))
            with col2:
                with st.container(border=True):
                    st.metric(
                        "Total Debits",
                        f"₹{df['Debit (Rs.)'].sum():,.2f}",
                    )
            with col3:
                with st.container(border=True):
                    st.metric(
                        "Total Credits",
                        f"₹{df['Credit (Rs.)'].sum():,.2f}",
                    )

            # Display transaction history
            st.dataframe(df.set_index("No."), width=1000)

            # Provide download option
            csv_filename = get_date_range_filename(df)
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            st.download_button(
                label="Download Statement as CSV",
                data=csv_buffer,
                file_name=csv_filename,
                mime="text/csv",
            )

        else:
            st.error(
                "No transactions found in the uploaded PDFs. Please make sure they are valid monthly statements."
            )
    else:
        st.info("Please upload one or more monthly statement PDFs to get started.")


def display_sbi_tabs():
    """
    Display the main tabs for SBI statement processing in the Streamlit app.
    """
    tab1, tab2 = st.tabs(["Transaction History Export", "Monthly Statements"])

    with tab1:
        display_transaction_history_tab()

    with tab2:
        display_monthly_statements_tab()
