# EMI Saver 💰

> **Smart Loan Optimization Platform** - Save thousands on your EMIs by finding the best refinancing options

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🚀 Overview

EMI Saver is an intelligent loan optimization platform that analyzes your current loans and compares them with market alternatives to find significant savings opportunities. By leveraging real-time market data and AI-powered recommendations, users can potentially save thousands of rupees on their EMIs through smart refinancing decisions.

### ✨ Key Features

- **🔍 Smart Loan Analysis** - Comprehensive analysis of your existing loan portfolio
- **📊 Market Comparison** - Real-time comparison with available market loan options  
- **💡 AI-Powered Recommendations** - Personalized refinancing suggestions based on your financial profile
- **💰 EMI Savings Calculator** - Calculate potential savings from loan switching
- **🤖 Intelligent Chatbot** - RAG-powered assistance for loan-related queries
- **📱 User-Friendly Dashboard** - Intuitive interface to manage and track your loans
- **🔐 Secure Authentication** - Firebase-based phone authentication with OTP

## 🏗️ Architecture

### Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: Firebase Auth
- **AI / ML**: Google ADK, Vertex AI, Cloud Run, Cloud Storage
- **RAG Pipeline**: Custom implementation for loan recommendations

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Fi MCP        │    │   EMI Saver      │    │   Market Data   │
│   Integration   │───▶│   Engine         │◀───│   RAG Pipeline  │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Data     │    │   Comparison     │    │   Loan          │
│   • Loans       │    │   Engine         │    │   Alternatives  │
│   • Bank Acc    │    │                  │    │                 │
│   • Investments │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 13+
- Firebase Project (for authentication)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/shubhamprajapati7748/emisaver.git
   cd emisaver
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Initialize the database
   python -m app.database.init_db
   ```

5. **Environment Configuration**
   ```bash
   # Create .env file with your configurations
   cp .env.example .env
   ```
   
   Configure the following variables:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/emisaver
   FIREBASE_CONFIG_PATH=path/to/firebase-config.json
   VERTEX_AI_PROJECT_ID=your-vertex-ai-project
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The application will be available at `http://localhost:8000`

## 📱 Features Deep Dive

### User Journey

1. **Onboarding**
   - Phone number registration
   - OTP verification via Firebase Auth
   - Initial loan data collection

2. **Dashboard Overview**
   - Current loans summary
   - Potential savings overview
   - Quick access to recommendations

3. **Loan Analysis**
   - Detailed breakdown of existing loans
   - Interest rate comparisons
   - EMI optimization suggestions

4. **Market Alternatives**
   - Real-time loan options from various lenders
   - Side-by-side comparisons
   - Projected savings calculations

5. **Refinancing Guidance**
   - Step-by-step switching process
   - Document requirements
   - Timeline and milestones

### AI-Powered Recommendations

Our recommendation engine uses:

- **Real User Data**: Integration with Fi MCP for actual loan and financial data
- **Market Intelligence**: RAG pipeline for up-to-date loan products
- **Personalization**: AI algorithms considering user's financial profile
- **Risk Assessment**: Evaluation of switching costs and benefits


## 🤖 Chatbot Integration

The platform includes an intelligent chatbot powered by:

- **RAG Pipeline**: Retrieval-Augmented Generation for accurate loan information
- **Loan Agent**: Specialized AI agent for loan-related queries  
- **Vertex AI**: Google's advanced AI platform
- **LangChain**: Framework for building AI applications

### Chatbot Capabilities

- Loan comparison queries
- EMI calculations
- Refinancing process guidance
- Market rate information
- Document requirements

## 🗄️ Database Schema

### Core Tables

- `users`: User profiles and authentication data
- `loans`: Current user loans with details
- `loan_alternatives`: Market loan products
- `recommendations`: AI-generated suggestions
- `savings_calculations`: Historical savings analysis

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please reach out through:

- Email: shubhamprajapati7748@gmail.com
- GitHub Issues: [Create an issue](https://github.com/shubhamprajapati7748/emisaver/issues)
---

**Made with ❤️ to help users save money on their loans**