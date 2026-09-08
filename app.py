import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Category keywords for automatic categorization
CATEGORY_KEYWORDS = {
    'Food & Dining': ['restaurant', 'cafe', 'coffee', 'food', 'pizza', 'burger', 'lunch', 'dinner', 'breakfast', 'starbucks', 'mcdonald', 'subway', 'doordash', 'ubereats', 'grubhub'],
    'Groceries': ['grocery', 'supermarket', 'walmart', 'target', 'costco', 'whole foods', 'trader joe', 'safeway', 'kroger', 'aldi', 'market'],
    'Transportation': ['uber', 'lyft', 'gas', 'fuel', 'parking', 'metro', 'transit', 'train', 'bus', 'taxi', 'shell', 'chevron', 'exxon'],
    'Shopping': ['amazon', 'store', 'mall', 'shop', 'retail', 'clothing', 'fashion', 'nike', 'adidas', 'zara', 'h&m'],
    'Entertainment': ['movie', 'theater', 'cinema', 'netflix', 'spotify', 'hulu', 'disney', 'game', 'concert', 'event'],
    'Bills & Utilities': ['electric', 'water', 'gas bill', 'internet', 'phone', 'utility', 'bill', 'insurance', 'rent', 'mortgage'],
    'Healthcare': ['pharmacy', 'doctor', 'hospital', 'medical', 'health', 'dental', 'clinic', 'cvs', 'walgreens'],
    'Education': ['school', 'university', 'course', 'book', 'tuition', 'education', 'learning'],
    'Travel': ['hotel', 'flight', 'airline', 'airbnb', 'booking', 'expedia', 'travel'],
    'Other': []
}

def categorize_transaction(description):
    """
    Automatically categorize a transaction based on its description.
    """
    description_lower = str(description).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if category == 'Other':
            continue
        for keyword in keywords:
            if keyword in description_lower:
                return category

    return 'Other'

def process_csv(df):
    """
    Process the uploaded CSV file and categorize transactions.
    """
    # Ensure required columns exist (try common variations)
    column_mapping = {}

    # Find date column
    date_cols = [col for col in df.columns if any(x in col.lower() for x in ['date', 'time'])]
    if date_cols:
        column_mapping[date_cols[0]] = 'Date'

    # Find description column
    desc_cols = [col for col in df.columns if any(x in col.lower() for x in ['description', 'merchant', 'name', 'detail'])]
    if desc_cols:
        column_mapping[desc_cols[0]] = 'Description'

    # Find amount column
    amount_cols = [col for col in df.columns if any(x in col.lower() for x in ['amount', 'value', 'total', 'debit', 'credit'])]
    if amount_cols:
        column_mapping[amount_cols[0]] = 'Amount'

    # Rename columns
    df = df.rename(columns=column_mapping)

    # Check if we have the required columns
    if 'Description' not in df.columns or 'Amount' not in df.columns:
        st.error("CSV must contain at least a description and amount column!")
        return None

    # Convert amount to numeric (handle negative values and currency symbols)
    df['Amount'] = pd.to_numeric(df['Amount'].astype(str).str.replace('[$,]', '', regex=True), errors='coerce')

    # Remove rows with invalid amounts
    df = df.dropna(subset=['Amount'])

    # Take absolute value of amounts (for spending analysis)
    df['Amount'] = df['Amount'].abs()

    # Add category column
    df['Category'] = df['Description'].apply(categorize_transaction)

    return df

# App title and description
st.title("💰 Expense Tracker")
st.markdown("Upload your bank statement CSV to analyze your spending by category")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        st.success(f"Successfully loaded {len(df)} transactions!")

        # Process and categorize
        df_processed = process_csv(df)

        if df_processed is not None:
            # Calculate category totals
            category_summary = df_processed.groupby('Category')['Amount'].sum().reset_index()
            category_summary = category_summary.sort_values('Amount', ascending=False)
            category_summary['Percentage'] = (category_summary['Amount'] / category_summary['Amount'].sum() * 100).round(2)

            # Total spending
            total_spending = category_summary['Amount'].sum()

            # Display metrics
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Transactions", len(df_processed))
            with col2:
                st.metric("Total Spending", f"${total_spending:,.2f}")
            with col3:
                st.metric("Categories", len(category_summary))

            st.markdown("---")

            # Create two columns for visualization
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📊 Spending by Category")
                # Create pie chart
                fig = px.pie(
                    category_summary,
                    values='Amount',
                    names='Category',
                    title='Spending Distribution',
                    hole=0.3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("📋 Category Summary")
                # Format the summary table
                display_summary = category_summary.copy()
                display_summary['Amount'] = display_summary['Amount'].apply(lambda x: f"${x:,.2f}")
                display_summary['Percentage'] = display_summary['Percentage'].apply(lambda x: f"{x}%")

                # Display as table
                st.dataframe(
                    display_summary,
                    hide_index=True,
                    use_container_width=True,
                    height=400
                )

            # Show sample transactions
            st.markdown("---")
            st.subheader("📝 Recent Transactions")

            # Show first 10 transactions
            display_df = df_processed[['Date', 'Description', 'Amount', 'Category']].head(10) if 'Date' in df_processed.columns else df_processed[['Description', 'Amount', 'Category']].head(10)
            display_df_formatted = display_df.copy()
            display_df_formatted['Amount'] = display_df_formatted['Amount'].apply(lambda x: f"${x:,.2f}")

            st.dataframe(display_df_formatted, hide_index=True, use_container_width=True)

            # Option to view all transactions
            with st.expander("View All Transactions"):
                all_display = df_processed[['Date', 'Description', 'Amount', 'Category']] if 'Date' in df_processed.columns else df_processed[['Description', 'Amount', 'Category']]
                all_display_formatted = all_display.copy()
                all_display_formatted['Amount'] = all_display_formatted['Amount'].apply(lambda x: f"${x:,.2f}")
                st.dataframe(all_display_formatted, hide_index=True, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please ensure your CSV has columns for transaction description and amount.")

else:
    # Instructions when no file is uploaded
    st.info("👆 Upload a CSV file to get started!")

    st.markdown("### Expected CSV Format")
    st.markdown("""
    Your CSV should contain at least these columns:
    - **Date** (optional): Transaction date
    - **Description**: Transaction description or merchant name
    - **Amount**: Transaction amount

    Example:
    """)

    # Show example CSV format
    example_data = {
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Description': ['Starbucks Coffee', 'Shell Gas Station', 'Amazon Purchase'],
        'Amount': [5.50, 45.00, 89.99]
    }
    st.dataframe(pd.DataFrame(example_data), hide_index=True)
