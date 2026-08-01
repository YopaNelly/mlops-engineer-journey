-- Day 8: SQL joins, aggregations, window functions
-- Practiced against the Chinook sample database (table names: Customer, Invoice, Track, Genre, Employee)

SELECT FirstName, LastName, Country FROM Customer LIMIT 10;
SELECT Country, COUNT(*) AS num_customers FROM Customer GROUP BY Country ORDER BY num_customers DESC;
SELECT c.FirstName, c.LastName, i.InvoiceDate, i.Total FROM Customer c INNER JOIN Invoice i ON i.CustomerId = c.CustomerId LIMIT 10;
SELECT c.FirstName, c.LastName, i.InvoiceDate FROM Customer c LEFT JOIN Invoice i ON i.CustomerId = c.CustomerId WHERE i.InvoiceDate IS NULL;
SELECT BillingCountry, SUM(Total) AS revenue FROM Invoice GROUP BY BillingCountry ORDER BY revenue DESC;
SELECT AVG(Total) FROM Invoice;
SELECT g.Name, COUNT(*) AS num_tracks FROM Track t JOIN Genre g ON g.GenreId = t.GenreId GROUP BY g.Name ORDER BY num_tracks DESC;
SELECT c.FirstName, c.LastName, SUM(i.Total) AS total_spent FROM Customer c JOIN Invoice i ON i.CustomerId = c.CustomerId GROUP BY c.CustomerId ORDER BY total_spent DESC LIMIT 5;
SELECT g.Name, AVG(t.UnitPrice) AS avg_price FROM Track t JOIN Genre g ON g.GenreId = t.GenreId GROUP BY g.Name;
SELECT strftime('%Y-%m', InvoiceDate) AS month, COUNT(*) AS num_invoices FROM Invoice GROUP BY month ORDER BY month;
SELECT e.FirstName, e.LastName, COUNT(c.CustomerId) AS num_customers FROM Employee e LEFT JOIN Customer c ON c.SupportRepId = e.EmployeeId GROUP BY e.EmployeeId;
SELECT Name, Milliseconds / 60000.0 AS minutes FROM Track WHERE Milliseconds > 300000 ORDER BY minutes DESC LIMIT 10;

-- Window function: most recent invoice per customer
SELECT * FROM (SELECT c.CustomerId, c.FirstName, c.LastName, i.InvoiceDate, i.Total, ROW_NUMBER() OVER (PARTITION BY c.CustomerId ORDER BY i.InvoiceDate DESC) AS rn FROM Customer c JOIN Invoice i ON i.CustomerId = c.CustomerId) ranked WHERE rn = 1;

-- Challenge: average order value from each customer's most active month
WITH monthly AS (SELECT CustomerId, strftime('%Y-%m', InvoiceDate) AS month, COUNT(*) AS num_orders, AVG(Total) AS avg_order_value FROM Invoice GROUP BY CustomerId, month), ranked AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY CustomerId ORDER BY num_orders DESC) AS rn FROM monthly) SELECT CustomerId, month, num_orders, avg_order_value FROM ranked WHERE rn = 1;
