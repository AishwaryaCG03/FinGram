# FinGram: Financial Advisor 

A modern, GenZ-focused financial education platform that makes learning about money management fun and engaging. Built with Streamlit and Python, FinGram combines memes, quizzes, and practical tools to help young adults understand personal finance.

## 📱 Screenshots & Features

### Home Page
- Personalized dashboard with financial tips
- GenZ-style interface with dark mode
- Quick access to all features
- Trending financial challenges
-[Sign_up](https://github.com/aish250/FinGram/blob/8c88ec24f031a8b35416c49e2af6e0602d1e9b52/Screenshot%202025-04-12%20024747.png)
 [Home Page](https://github.com/aish250/FinGram/blob/8dbb6807e9cb13dbafc859612fa732c907f018a9/Screenshot%202025-04-12%20024847.png)
  
### EMI Calculator 💰
- Loan amount calculation in Indian Rupees (₹)
- Interest rate visualization
- Monthly payment breakdown
- Amortization schedule with charts
- [EMI Calculator](https://github.com/aish250/FinGram/blob/403b6bb09942a5ff9367bdfc1799e0af0ef9c93f/Screenshot%202025-04-12%20025018.png)
- [EMI Schedule](https://github.com/aish250/FinGram/blob/16cffe27e6ecdd4a47620951a3987e7910f5225d/Screenshot%202025-04-12%20025047.png)
- [Graph Overview](https://github.com/aish250/FinGram/blob/1ea7d40f599eefa47d8d35ff1f83a678e63af980/Screenshot%202025-04-12%20025108.png)
- [Pro Tip](https://github.com/aish250/FinGram/blob/04d241c6d2c270ac3540c57cd67002712b0290cd/Screenshot%202025-04-12%20025205.png)

### Finance Quiz 📝
- 5 Categories: Budgeting, Investing, Credit, Taxes, Digital Money
- 10 questions per category
- Real-time scoring
- Performance tracking
- Leaderboard functionality
- [Quizz](https://github.com/aish250/FinGram/blob/86ddd08741078e55b377f63e73df6e65d648bcfe/Screenshot%202025-04-12%20031848.png)
- [Score Card](https://github.com/aish250/FinGram/blob/86ddd08741078e55b377f63e73df6e65d648bcfe/Screenshot%202025-04-12%20031835.png)

### Expense Tracker 💸
- Track daily expenses
- Split bills with friends
- Category-wise breakdown
- Export data to CSV
- Visual analytics
- [Expense Tracker](https://github.com/aish250/FinGram/blob/5ff507d141eda0c0e5b5f9a169a8d47b4fe18166/Screenshot%202025-04-12%20032709.png)
- [Split Bills](https://github.com/aish250/FinGram/blob/3f38cfec20edc7905228f1b107dcc833de8cec18/Screenshot%202025-04-12%20032725.png)

### Meme Gallery 🎭
- Financial education through memes
- Like, comment, and share functionality
- Social media integration (WhatsApp, Twitter, LinkedIn, Instagram)
- User-generated content support
- Trending hashtags

### Savings Calculator 📊
- Goal-based savings planning
- Interest calculation
- Visual progress tracking
- Monthly breakdown

## 🛠️ Technical Stack

### Frontend
- **Streamlit**: Main web framework
- **Plotly Express**: Interactive charts and visualizations
- **Pandas**: Data manipulation and analysis

### Backend
- **SQLite**: Database management
- **Python 3.x**: Core programming language

### Libraries & Dependencies
```python
streamlit==1.27.2
pandas==2.1.1
plotly==5.17.0
Pillow==10.0.1
sqlite3
urllib3==2.0.7
```

### APIs & Integrations
- WhatsApp Sharing API
- Twitter Intent API
- LinkedIn Sharing API
- Instagram Story API

## 💾 Database Schema

### Users Table
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT,
    created_at TIMESTAMP
);
```

### Quiz Scores
```sql
CREATE TABLE quiz_scores (
    id INTEGER PRIMARY KEY,
    username TEXT,
    category TEXT,
    score INTEGER,
    timestamp TIMESTAMP
);
```

### Expenses
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    username TEXT,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT,
    split_with TEXT,
    split_amount REAL
);
```

## 🚀 Setup & Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/fingram.git
cd fingram
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
streamlit run app.py
```

## 🎯 Features & Functionality

### Authentication
- User registration
- Secure login system
- Session management

### Financial Education
- Interactive learning modules
- Real-world examples
- GenZ-friendly content
- Indian context and currency

### Social Features
- Community engagement
- Meme sharing
- Social media integration
- User feedback system

### Data Analysis
- Expense tracking
- Savings projections
- Investment calculations
- Visual analytics

## 🔒 Security Features

- Password hashing
- Session state management
- Input validation
- Database security
- Error handling

## 🎨 UI/UX Features

- Dark mode interface
- Mobile-responsive design
- TikTok-inspired layout
- Emoji-rich interactions
- Modern typography
- Interactive components

## 📱 Supported Platforms

- Web browsers (Chrome, Firefox, Safari)
- Mobile devices
- Tablets
- Desktop computers

## 🤝 Contributing

Feel free to contribute to this project:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## 🙏 Acknowledgments

- Streamlit community
- Financial education resources
- Open-source contributors
- GenZ finance influencers
