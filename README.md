# 💰 Expense Tracker

A simple and user-friendly Streamlit application that analyzes your spending by automatically categorizing transactions from your bank statement CSV.

## Project Structure

```
expense_tracker/
├── .claude/                    # Claude Code configuration
│   ├── commands/              # Custom slash commands
│   │   ├── setup.md          # /setup command
│   │   ├── test.md           # /test command
│   │   └── deploy.md         # /deploy command
│   └── settings.json         # Project settings
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── sample_transactions.csv    # Sample data for testing
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Features

- 📊 **CSV Upload**: Import your bank statement in CSV format
- 🤖 **Auto-Categorization**: Automatically categorizes transactions using keyword matching
- 📈 **Pie Chart Visualization**: Visual breakdown of spending by category
- 📋 **Summary Table**: Detailed table showing spending amounts and percentages
- 💡 **User-Friendly**: Clean and intuitive interface

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd expense_tracker
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Using the App

1. **Prepare your CSV file**: Export your bank transactions as CSV with at least these columns:
   - Description (transaction description or merchant name)
   - Amount (transaction amount)
   - Date (optional, but recommended)

2. **Upload CSV**: Click "Browse files" and select your CSV file

3. **View Results**: The app will automatically:
   - Categorize all transactions
   - Show total spending and transaction count
   - Display a pie chart of spending by category
   - Show a summary table with percentages
   - List recent transactions with their categories

### Sample Data

Try the app with the included `sample_transactions.csv` file to see how it works!

## Categories

The app automatically categorizes transactions into the following categories:

- **Food & Dining**: Restaurants, cafes, fast food, food delivery
- **Groceries**: Supermarkets, grocery stores
- **Transportation**: Uber, Lyft, gas stations, parking, public transit
- **Shopping**: Retail stores, online shopping (Amazon, etc.)
- **Entertainment**: Movies, streaming services, concerts, events
- **Bills & Utilities**: Electric, water, internet, phone, rent, insurance
- **Healthcare**: Pharmacy, doctors, hospitals, medical
- **Education**: School, courses, books, tuition
- **Travel**: Hotels, flights, vacation expenses
- **Other**: Anything that doesn't fit the above categories

## CSV Format Examples

Your CSV can have various formats. The app automatically detects columns for:
- Date, description, and amount
- Common variations like "Transaction Date", "Merchant", "Debit", etc.

Example 1 - Simple format:
```csv
Date,Description,Amount
2024-01-01,Starbucks,5.50
2024-01-02,Shell Gas,45.00
```

Example 2 - Bank statement format:
```csv
Transaction Date,Merchant Name,Debit Amount
01/01/2024,STARBUCKS #12345,-5.50
01/02/2024,SHELL OIL,-45.00
```

## Troubleshooting

**Issue**: CSV won't upload or shows error
- **Solution**: Ensure your CSV has at least a description and amount column

**Issue**: Categories seem incorrect
- **Solution**: You can modify the `CATEGORY_KEYWORDS` dictionary in `app.py` to add more keywords for better matching

**Issue**: App shows $0.00 for amounts
- **Solution**: Check that your amount column contains numeric values

## Future Enhancements

Potential features for future versions:
- Date range filtering
- Budget tracking per category
- Export analyzed results
- Manual category editing
- Monthly/yearly comparisons
- Custom category creation

## License

MIT License - Feel free to use and modify for your needs!