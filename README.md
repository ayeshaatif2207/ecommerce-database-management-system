# ecommerce-database-management-system

An AI-powered e-commerce management system that combines database management, web development, and large language models to make an interface for managing business data.

Me and my team developed this as my university Database Systems project. My team helped my out with designing the ERD diagram and creating the dataset while I took over to develop the web-application, that included a role-based web management portal, and AI-powered natural language querying through both an LLM and an Ollama chatbot in a kaggle notebook using hugging face tokens.

## Features implemented alongside my team members:

### Database
- Relational database designed using MySQL
- Normalized database schema
- SQL queries for business operations
- Entity relationships and constraints

### Documentation
- Documenting the 2 phases of our project and its details

## Features implemented by myself:

### Web Application
- Employee authentication and login system
- Role-Based Access Control (RBAC)
- Secure access based on employee roles
- Create, Read, Update and Delete (CRUD) operations
- User-friendly dashboard for managing business records

### AI Integration
- Natural language to SQL conversion
- LLM-generated SQL queries
- Automatic execution of generated SQL queries
- Human-readable responses from database results

### Ollama Chatbot
- Local AI chatbot using Ollama, Qwen
- Database-aware conversational interface
- Query business data using plain English

### Kaggle Notebook
- SQLite implementation of the database
- Demonstration of the AI pipeline
- Hugging Face model integration
- Natural language database querying

## Technologies Used

### Backend
- Python

### Database
- MySQL
- SQLite

### Web
- HTML
- CSS
- JavaScript

### AI
- Hugging Face Transformers
- Ollama
- LLM-based Natural Language to SQL
- langchain

### Tools
- Kaggle Notebooks
- Git
- GitHub

## How It Works

1. Employees log into the web application.
2. Access permissions are determined by their assigned role.
3. Authorized users can manage products, customers, inventory, and other records.
4. Users can alternatively ask questions in natural language.
5. The AI model converts the request into an SQL query.
6. The query is executed on the database.
7. Results are returned in a readable format.
8. The Ollama chat interface provides a conversational interface for the same functionality.

## Example Queries

- Show all products that are low in stock.
- Which customers placed the most orders this month?
- List today's completed orders.
- Display all pending shipments.
- What is the total revenue for this week?

## Screenshots

### kaggle notebook features:
<img width="1077" height="330" alt="image" src="https://github.com/user-attachments/assets/e71555d5-78fe-48ac-b429-7511673310b5" />

### Login Page:
<img width="1261" height="550" alt="image" src="https://github.com/user-attachments/assets/acc61400-93d0-4f68-a3ed-6cd1b2892541" /> 

### Dashboard:
<img width="1262" height="552" alt="image" src="https://github.com/user-attachments/assets/ef687e81-0e39-4f5a-a857-fcb336ac1b35" />

### Database Schema:
<img width="1263" height="549" alt="image" src="https://github.com/user-attachments/assets/e523fdb9-2d64-4892-8ca1-015e077c4e80" />

### AI Query Interface:
<img width="1279" height="491" alt="image" src="https://github.com/user-attachments/assets/f2a75e8e-ff70-4ad3-ac85-da46399ca620" />

### Ollama interactive chat interface with ipywidgets
<img width="1082" height="315" alt="image" src="https://github.com/user-attachments/assets/69a3ec1e-71b1-4161-b9cd-8a2d968b1b37" />

## Contributors

As mentioned earlier this project was developed as part of a university Database Systems course.
Contributors:
- Ayesha Atif
- Noor Fatima
- Zainab Tariq
- Zoha Sohail
