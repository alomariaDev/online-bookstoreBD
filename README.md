# 📚 Online Bookstore Database Management System – SQL Project

This project is based on an Online Bookstore database system where data is stored, managed and analyzed using SQL & PostgreSQL.

The project includes:
✔ Database schema design  
✔ CSV dataset import  
✔ Table relationships using Primary & Foreign Keys  
✔ Data analysis queries  
✔ Sales & inventory insights  


## 📁 Dataset Files

The project uses three CSV files:

- Books.csv  
- Customers.csv  
- Orders.csv  


## 🗄 Database Tables

### 🟦 Books Table
Stores book-related data such as:
Book_ID, Title, Author, Genre, Published_Year, Price, Stock

### 🟩 Customers Table
Stores customer details:
Customer_ID, Name, Email, Phone, City, Country

### 🟨 Orders Table
Stores transaction records:
Order_ID, Customer_ID, Book_ID, Order_Date, Quantity, Total_Amount


## 🔗 Table Relationships (Keys)

- Book_ID → Links Books & Orders
- Customer_ID → Links Customers & Orders

✔ Ensures referential integrity  
✔ Avoids duplicate & inconsistent data  


## 🛠 SQL Operations Performed

✔ Table creation with constraints  
✔ Data import using CSV  
✔ SELECT, WHERE, ORDER BY  
✔ Aggregate functions  
✔ GROUP BY & HAVING  
✔ INNER JOIN / LEFT JOIN  
✔ Business case queries  


## 🧮 Basic SQL Queries Covered

1️⃣ Retrieve all books in a specific genre  
2️⃣ Find books published after a given year  
3️⃣ List customers from a specific country  
4️⃣ Show orders in a particular month  
5️⃣ Retrieve total stock of books  
6️⃣ Find most expensive book  
7️⃣ Show customers who ordered > 1 quantity  
8️⃣ Retrieve orders where amount exceeds $20  
9️⃣ List all genres available in Books table  
🔟 Find book with lowest stock  
11️⃣ Calculate total revenue from all orders  


## 🚀 Advanced SQL Queries

✔ Total books sold per genre  
✔ Average book price by genre  
✔ Customers who placed 2+ orders  
✔ Most frequently ordered book  
✔ Top 3 most expensive books (Fantasy)  
✔ Total quantity sold by each author  
✔ Cities with customers spending > $30  
✔ Customer who spent the most  
✔ Remaining stock after all orders  


## 🧰 Tech Stack

- PostgreSQL
- pgAdmin
- SQL
- CSV datasets


## 👤 Developed By

**Rakesh Malash**  
B.Tech — Computer Science & Engineering  


---

⭐ If you like this project, feel free to Star the repository 🙂

