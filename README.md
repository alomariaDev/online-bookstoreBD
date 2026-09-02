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

### Modelo normalizado propuesto

El archivo [schema_libreria.sql](schema_libreria.sql) contiene un esquema PostgreSQL de cuatro tablas y [modelo_entidad_relacion.md](modelo_entidad_relacion.md) su diagrama ER editable. Este modelo separa la cabecera del pedido de sus productos, por lo que cada pedido puede incluir varios libros.

- `clientes`: datos de los compradores.
- `libros`: catálogo, precio actual e inventario.
- `pedidos`: cabecera de la compra y su estado.
- `detalle_pedido`: libros, cantidades y precio histórico de cada pedido.

Para levantar una base PostgreSQL local con este esquema, sigue [postgres_setup.md](postgres_setup.md). La configuración se encuentra en `docker-compose.yml`.

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


## 🧩 How to Run This Project

1) Create a database in PostgreSQL
2) Import Books.csv, Customers.csv, Orders.csv
3) Run the SQL script file
4) Execute Queries for analysis

This project was executed using pgAdmin & PostgreSQL.


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
