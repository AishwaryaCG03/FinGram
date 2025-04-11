# FinGram: Financial Advisor 

A modern, GenZ-focused financial education platform that makes learning about money management fun and engaging. Built with Streamlit and Python, FinGram combines memes, quizzes, and practical tools to help young adults understand personal finance.

## 📱 Screenshots & Features

### Home Page
- Personalized dashboard with financial tips
- GenZ-style interface with dark mode
- Quick access to all features
- Trending financial challenges
  [Sign_up](https://github.com/aish250/FinGram/blob/8c88ec24f031a8b35416c49e2af6e0602d1e9b52/Screenshot%202025-04-12%20024747.png)
  [Home Page](https://github.com/aish250/FinGram/blob/8dbb6807e9cb13dbafc859612fa732c907f018a9/Screenshot%202025-04-12%20024847.png)
  
### EMI Calculator 💰
- Loan amount calculation in Indian Rupees (₹)
- Interest rate visualization
- Monthly payment breakdown
- Amortization schedule with charts

### Finance Quiz 📝
- 5 Categories: Budgeting, Investing, Credit, Taxes, Digital Money
- 10 questions per category
- Real-time scoring
- Performance tracking
- Leaderboard functionality

### Expense Tracker 💸
- Track daily expenses
- Split bills with friends
- Category-wise breakdown
- Export data to CSV
- Visual analytics

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
