# SQL for Data Engineering

## Table of Contents

#### Chapter 1: SQL Fundamentals

##### 1.1 Querying and Filtering
*   `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIMIT`

##### 1.2 Data Aggregation
*   `GROUP BY` with Functions like `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`
*   `HAVING` Clause for Filtering Groups

##### 1.3 Joining Tables
*   `INNER`, `LEFT`, `RIGHT`, and `FULL OUTER` Joins

##### 1.4 Data Manipulation Language (DML)
*   `INSERT`: Adding New Rows
*   `UPDATE`: Modifying Existing Rows
*   `DELETE`: Removing Rows
*   Transaction Control (`BEGIN`, `COMMIT`, `ROLLBACK`)

##### 1.5 Data Definition Language (DDL)
*   `CREATE TABLE`: Building Tables (Data Types, Constraints)
*   `ALTER TABLE`: Modifying Existing Tables
*   `DROP TABLE`: Deleting Tables (`TRUNCATE` vs. `DELETE` vs. `DROP`)

#### Chapter 2: Advanced SQL & Data Modeling

##### 2.1 Complex Queries
*   Subqueries (in `WHERE`, `FROM`, `SELECT` clauses)
*   Common Table Expressions (CTEs): `WITH` Clause for Readability
*   Views: Creating Virtual Tables for Simplicity and Security

##### 2.2 Window Functions
*   Ranking Functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`
*   Aggregate Functions over a Window (e.g., Running Totals, Moving Averages)
*   Offset Functions: `LAG()` and `LEAD()`

##### 2.3 Advanced Techniques
*   Pivoting Data with `CASE` Statements or `PIVOT`
*   Stored Procedures and User-Defined Functions (UDFs) for Reusable Logic
*   Materialized Views for Pre-computing and Storing Query Results

#### Chapter 3: Data Warehousing & Performance

##### 3.1 Data Warehouse Design
*   Schema Design: In-depth Comparison of Star vs. Snowflake Schemas
*   Slowly Changing Dimensions (SCDs): Techniques (Type 1, Type 2) for Tracking Historical Changes

##### 3.2 Data Modeling
*   Normalization: Reducing Redundancy
*   Denormalization: Optimizing for Read Performance
*   Surrogate Keys: Unique Identifiers for Data Warehouses

##### 3.3 Query Performance and Optimization
*   Reading Execution Plans (`EXPLAIN`) to Identify Bottlenecks
*   Indexing Strategies: How to Choose the Right Indexes for Faster Queries
*   Data Partitioning: Improving Performance by Scanning Less Data
*   Choosing Efficient Data Types to Save Storage and Improve Speed

#### Chapter 4: SQL in the Modern Data Stack

##### 4.1 ETL/ELT Pipelines
*   Writing Idempotent `INSERT`/`UPDATE` (Upsert) Logic (`MERGE` Statement)
*   Transaction Management to Ensure Data Integrity

##### 4.2 SQL with Modern Tools
*   Using SQL with Orchestration Tools like Apache Airflow
*   Leveraging SQL-centric Transformation Tools like dbt


## Introduction

**SQL (Structured Query Language)** remains the universal language for interacting with data. It is the indispensable tool for querying, defining, and manipulating data stored in relational databases, data warehouses, and modern distributed query engines.

For a data engineer, SQL is not just a query language; it is a way of thinking. It provides a declarative framework for expressing complex data retrieval and aggregation logic. A deep understanding of SQL is the most critical and transferable skill in the data profession. From PostgreSQL to BigQuery, from Spark SQL to dbt, proficiency in SQL is the foundation upon which all other data engineering skills are built.

This book is designed to be a comprehensive guide to SQL specifically for data engineering. We will move from the fundamental building blocks of querying to the advanced techniques required for designing data models, optimizing performance, and building robust data transformation pipelines.

## Chapter 1: SQL Fundamentals

This section covers the essential commands that form the bedrock of all SQL work. We will explore how to retrieve data, perform calculations, and combine information from multiple tables. We will also cover the commands used to define and manipulate the structure of the data itself.

### **1.1 Querying and Filtering: The `SELECT` Statement**

The `SELECT` statement is the workhorse of SQL. It is used to retrieve data from one or more tables. Every query you write will begin with `SELECT`.

**The Basic Clauses:**

*   `SELECT`: Specifies the columns you want to retrieve. Use `*` to select all columns.
*   `FROM`: Specifies the table you are querying.
*   `WHERE`: Filters rows based on a specified condition.
*   `ORDER BY`: Sorts the result set based on one or more columns.
*   `LIMIT`: Restricts the number of rows returned.

**Example Scenario:**
We will use a sample `employees` table for our queries.

| employee_id | first_name | last_name   | department    | hire_date  | salary |
| :---------- | :--------- | :---------- | :------------ | :--------- | :----- |
| 101         | Alice      | Williams    | Engineering   | 2022-08-15 | 90000  |
| 102         | Bob        | Johnson     | Engineering   | 2021-11-01 | 115000 |
| 103         | Charlie    | Brown       | Sales         | 2023-02-20 | 78000  |
| 104         | David      | Smith       | Sales         | 2022-05-10 | 82000  |
| 105         | Eve        | Davis       | HR            | 2023-01-09 | 65000  |

---
**1. `SELECT` and `FROM`**
To retrieve the names and departments of all employees:

```sql
SELECT first_name, last_name, department
FROM employees;
```
**Result:**
| first_name | last_name | department    |
| :--------- | :-------- | :------------ |
| Alice      | Williams  | Engineering   |
| Bob        | Johnson   | Engineering   |
| Charlie    | Brown     | Sales         |
| David      | Smith     | Sales         |
| Eve        | Davis     | HR            |

---
**2. The `WHERE` Clause: Filtering Data**
To find all employees in the 'Engineering' department:

```sql
SELECT employee_id, first_name, salary
FROM employees
WHERE department = 'Engineering';
```
**Result:**
| employee_id | first_name | salary |
| :---------- | :--------- | :----- |
| 101         | Alice      | 90000  |
| 102         | Bob        | 115000 |

You can use various operators (`=`, `!=`, `>`, `<`, `>=`, `<=`) and combine conditions with `AND` and `OR`.

```sql
-- Find all employees in Sales with a salary greater than 80000
SELECT first_name, salary
FROM employees
WHERE department = 'Sales' AND salary > 80000;
```
**Result:**
| first_name | salary |
| :--------- | :----- |
| David      | 82000  |

---
**3. The `ORDER BY` Clause: Sorting Results**
To list employees by their hire date, from oldest to newest:

```sql
SELECT first_name, hire_date
FROM employees
ORDER BY hire_date ASC; -- ASC is for ascending (default), DESC is for descending
```
**Result:**
| first_name | hire_date  |
| :--------- | :--------- |
| Bob        | 2021-11-01 |
| David      | 2022-05-10 |
| Alice      | 2022-08-15 |
| Eve        | 2023-01-09 |
| Charlie    | 2023-02-20 |

---
**4. The `LIMIT` Clause: Restricting Output**
To find the top 3 highest-paid employees:

```sql
SELECT employee_id, first_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3;
```
**Result:**
| employee_id | first_name | salary |
| :---------- | :--------- | :----- |
| 102         | Bob        | 115000 |
| 101         | Alice      | 90000  |
| 104         | David      | 82000  |

---
### **Data Engineering Perspective**

*   **Data Exploration**: These fundamental clauses are your primary tools for exploring source data. Before building a pipeline, you will use `SELECT` with `WHERE`, `ORDER BY`, and `LIMIT` to sample the data, understand its structure, check for anomalies, and validate your assumptions.
*   **Source Queries**: The "Extract" step of an ELT pipeline often involves a `SELECT` statement that pulls a specific subset of data from a source table. The `WHERE` clause is critical for incremental processing (e.g., `WHERE created_at > 'yesterdays_date'`).
*   **Debugging**: When a pipeline produces incorrect results, your first step is to write `SELECT` statements against the source, intermediate, and destination tables to trace the data's journey and pinpoint where the logic went wrong. `LIMIT` is essential here to avoid querying billions of rows while debugging.

***
### **1.2 Data Aggregation: The `GROUP BY` Clause**

Raw, row-level data is useful, but the most valuable insights often come from aggregated data. **Aggregation** is the process of summarizing data by calculating a statistic—like a count, sum, or average—over a set of rows.

The `GROUP BY` clause is the cornerstone of aggregation in SQL. It groups rows that have the same values in specified columns into summary rows. It is almost always used in conjunction with aggregate functions.

**Common Aggregate Functions:**

*   `COUNT()`: Counts the number of rows. `COUNT(*)` counts all rows; `COUNT(column_name)` counts non-null values in that column.
*   `SUM()`: Calculates the sum of a numeric column.
*   `AVG()`: Calculates the average of a numeric column.
*   `MAX()`: Returns the maximum value in a column.
*   `MIN()`: Returns the minimum value in a column.

---
**1. `COUNT()`: Counting Rows**
To find the total number of employees:

```sql
SELECT COUNT(*) AS total_employees
FROM employees;
```
**Result:**
| total_employees |
| :-------------- |
| 5               |

To count the number of employees in each department:
```sql
SELECT department, COUNT(*) AS number_of_employees
FROM employees
GROUP BY department;
```
**Execution Flow:**
1.  `FROM employees`: The database looks at the `employees` table.
2.  `GROUP BY department`: It groups the rows based on their `department` value ('Engineering', 'Sales', 'HR').
3.  `SELECT department, COUNT(*)`: For each group, it selects the department name and counts the number of rows within that group.

**Result:**
| department    | number_of_employees |
| :------------ | :------------------ |
| Engineering   | 2                   |
| Sales         | 2                   |
| HR            | 1                   |

---
**2. `SUM()`, `AVG()`, `MAX()`, `MIN()`**
To calculate salary statistics for each department:

```sql
SELECT
    department,
    SUM(salary) AS total_salary_paid,
    AVG(salary) AS average_salary,
    MAX(salary) AS highest_salary,
    MIN(salary) AS lowest_salary
FROM
    employees
GROUP BY
    department;
```
**Result:**
| department    | total_salary_paid | average_salary | highest_salary | lowest_salary |
| :------------ | :---------------- | :------------- | :------------- | :------------ |
| Engineering   | 205000            | 102500.00      | 115000         | 90000         |
| Sales         | 160000            | 80000.00       | 82000          | 78000         |
| HR            | 65000             | 65000.00       | 65000          | 65000         |

---
### **The `HAVING` Clause: Filtering Groups**

The `WHERE` clause filters rows *before* they are grouped. But what if you want to filter the results *after* the aggregation has happened? This is the job of the `HAVING` clause.

**`WHERE` vs. `HAVING`**
*   `WHERE` filters individual rows.
*   `HAVING` filters groups created by `GROUP BY`.

**Example:**
Find departments where the average salary is greater than $100,000.

You cannot use `WHERE AVG(salary) > 100000` because `WHERE` operates on rows, and the `AVG(salary)` only exists after the `GROUP BY` operation.

```sql
SELECT
    department,
    AVG(salary) AS average_salary
FROM
    employees
GROUP BY
    department
HAVING
    AVG(salary) > 100000;
```
**Execution Flow:**
1.  `FROM employees`: Gets the table.
2.  `GROUP BY department`: Groups rows by department.
3.  `AVG(salary)`: Calculates the average salary for each group.
4.  `HAVING AVG(salary) > 100000`: Filters out the groups that do not meet this condition.
5.  `SELECT`: Selects the final columns for the remaining group(s).

**Result:**
| department    | average_salary |
| :------------ | :------------- |
| Engineering   | 102500.00      |

---
### **Data Engineering Perspective**

*   **Building Summary Tables**: A primary task for data engineers is to pre-aggregate raw data into summary tables (or "materialized views"). For example, instead of letting analysts query a massive `transactions` table with billions of rows, you would create a `daily_sales_summary` table using `GROUP BY` on the date and product ID. This makes reporting dashboards vastly faster and cheaper to run.
*   **Data Profiling and Quality Checks**: Aggregation is key to data profiling. You use `GROUP BY` and `COUNT(*)` to find the distribution of values in a column, identify duplicates (`GROUP BY key HAVING COUNT(*) > 1`), and check for cardinality issues.
*   **The "T" in ELT**: In an ELT (Extract, Load, Transform) workflow, the "Transform" step, which often happens inside the data warehouse itself (e.g., using dbt), is heavily reliant on aggregation. You load raw data into the warehouse and then run a series of SQL models that clean, join, and aggregate the data into new, analysis-ready tables. These models are almost entirely composed of `SELECT` statements with `GROUP BY` clauses.

***
### **1.3 Joining Tables: Combining Data**

Rarely is all the information you need stored in a single table. Data is typically normalized—split into multiple related tables to reduce redundancy and improve data integrity. The process of combining rows from two or more tables based on a related column is called a **JOIN**.

The `JOIN` clause is a fundamental part of SQL, allowing you to enrich your data by linking tables together.

**Example Scenario:**
In addition to our `employees` table, we now have a `departments` table that contains more information about each department.

**`employees` table:**
| employee_id | first_name | department_id |
| :---------- | :--------- | :------------ |
| 101         | Alice      | 1             |
| 102         | Bob        | 1             |
| 103         | Charlie    | 2             |
| 104         | David      | NULL          |

**`departments` table:**
| department_id | department_name | location      |
| :------------ | :-------------- | :------------ |
| 1             | Engineering     | Building A    |
| 2             | Sales           | Building B    |
| 3             | Marketing       | Building C    |

The `department_id` column is the **foreign key** in the `employees` table that relates to the **primary key** in the `departments` table.

---
### **1. `INNER JOIN`: The Intersection of Data**

An `INNER JOIN` (often written simply as `JOIN`) returns only the rows where the join condition is met in **both** tables. It finds the intersection of the two tables.

**Example:**
To get a list of employees and the name of the department they work in:

```sql
SELECT
    e.first_name,
    d.department_name,
    d.location
FROM
    employees AS e
INNER JOIN
    departments AS d ON e.department_id = d.department_id;
```
*   `e` and `d` are **aliases**, which are temporary, shorter names for tables to improve readability.
*   The `ON` clause specifies the join condition.

**Execution Flow:**
The database compares each row in `employees` with each row in `departments`. If the `department_id` values match, it combines the columns and includes the row in the result.

**Result:**
| first_name | department_name | location   |
| :--------- | :-------------- | :--------- |
| Alice      | Engineering     | Building A |
| Bob        | Engineering     | Building A |
| Charlie    | Sales           | Building B |

*   **David** is not included because his `department_id` is `NULL` and doesn't match any ID in `departments`.
*   The **Marketing** department is not included because no employee is assigned to `department_id` 3.

---
### **2. `LEFT JOIN`: Preserving the Left Table**

A `LEFT JOIN` (or `LEFT OUTER JOIN`) returns **all** rows from the **left** table (the first one mentioned) and the matched rows from the right table. If there is no match, the columns from the right table will contain `NULL`.

This is extremely useful for finding records in one table that do not have a corresponding record in another.

**Example:**
To get a list of *all* employees and their department, even if they don't have one assigned:

```sql
SELECT
    e.first_name,
    d.department_name
FROM
    employees AS e
LEFT JOIN
    departments AS d ON e.department_id = d.department_id;
```
**Result:**
| first_name | department_name |
| :--------- | :-------------- |
| Alice      | Engineering     |
| Bob        | Engineering     |
| Charlie    | Sales           |
| David      | NULL            |

*   **David** is now included, and his `department_name` is `NULL` because his `department_id` did not find a match in the `departments` table.

**A `RIGHT JOIN`** does the exact opposite: it keeps all rows from the right table and fills in `NULL`s for the left table's columns where there is no match. You can almost always rewrite a `RIGHT JOIN` as a `LEFT JOIN` by swapping the table order, which is often preferred for readability.

---
### **3. `FULL OUTER JOIN`: Preserving All Data**

A `FULL OUTER JOIN` returns **all** rows when there is a match in either the left or the right table. It combines the functionality of `LEFT JOIN` and `RIGHT JOIN`. If there's no match, the missing side's columns will be `NULL`.

This is useful for seeing a complete picture of all data from both tables, regardless of whether a relationship exists.

**Example:**
To list all employees and all departments, matching them where possible:

```sql
SELECT
    e.first_name,
    d.department_name
FROM
    employees AS e
FULL OUTER JOIN
    departments AS d ON e.department_id = d.department_id;
```
**Result:**
| first_name | department_name |
| :--------- | :-------------- |
| Alice      | Engineering     |
| Bob        | Engineering     |
| Charlie    | Sales           |
| David      | NULL            |
| NULL       | Marketing       |

*   This result includes **David** (who has no department) and the **Marketing** department (which has no employees).

---
### **Data Engineering Perspective**

*   **Data Enrichment**: `JOIN`s are the primary mechanism for data enrichment. You join your primary fact table (e.g., `transactions`) with dimension tables (e.g., `products`, `users`, `stores`) to add descriptive context to your raw data. An `INNER JOIN` is often used when the relationship is mandatory, while a `LEFT JOIN` is used to enrich data with optional attributes.
*   **Data Reconciliation and Quality Checks**: `LEFT JOIN` is a powerful tool for data quality. To find "orphan" records in a table (e.g., employees with an invalid `department_id`), you can use a query like:
    ```sql
    SELECT e.*
    FROM employees AS e
    LEFT JOIN departments AS d ON e.department_id = d.department_id
    WHERE d.department_id IS NULL AND e.department_id IS NOT NULL;
    ```
    This query finds all employees who have a non-null `department_id` that does not exist in the `departments` table.
*   **Building Analysis-Ready Tables**: The goal of many data transformation pipelines is to produce a wide, "denormalized" table that is easy for analysts to query. This is achieved by joining multiple normalized source tables into a single table, eliminating the need for analysts to perform complex joins themselves.

***
### **1.4 Data Manipulation Language (DML): Modifying Data**

While `SELECT` is used for querying data, Data Manipulation Language (DML) commands are used to modify the data within your tables. The three core DML commands are `INSERT`, `UPDATE`, and `DELETE`. These commands are essential for managing the lifecycle of your data, from creation to modification to removal.

---
### **1. `INSERT`: Adding New Rows**

The `INSERT INTO` statement is used to add one or more new rows to a table.

**Syntax:**
```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

**Example:**
To add a new employee, Frances, to the `employees` table:

```sql
INSERT INTO employees (employee_id, first_name, last_name, department_id, hire_date, salary)
VALUES (106, 'Frances', 'Green', 2, '2023-05-12', 81000);
```
After this command, a new row with `employee_id` 106 will be present in the table. You can also insert multiple rows at once:

```sql
INSERT INTO employees (employee_id, first_name, department_id)
VALUES
    (107, 'Grace', 1),
    (108, 'Heidi', 3);
```

**Data Engineering Perspective:**
`INSERT` is the "Load" part of an ETL process. After extracting and transforming data, your pipeline will use `INSERT` to load the clean, processed records into a final destination table. For large volumes of data, data warehouses have highly optimized bulk-loading utilities that are far more efficient than row-by-row `INSERT` statements. However, `INSERT` is still fundamental for smaller batches or single record additions.

---
### **2. `UPDATE`: Modifying Existing Rows**

The `UPDATE` statement is used to modify existing rows in a table. It is almost always used with a `WHERE` clause.

**WARNING:** If you omit the `WHERE` clause in an `UPDATE` statement, you will update **all rows** in the table. This is a common and dangerous mistake.

**Syntax:**
```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

**Example:**
Employee Charlie Brown gets a promotion and a salary raise, and moves to the Engineering department.

```sql
UPDATE employees
SET
    salary = 85000,
    department_id = 1
WHERE
    employee_id = 103;
```
Before this `UPDATE`, Charlie's `salary` was 78000 and `department_id` was 2. After, the values in that specific row are changed.

You can also perform calculations in an `UPDATE` statement. To give all employees in the Sales department a 5% raise:
```sql
UPDATE employees
SET salary = salary * 1.05
WHERE department_id = 2;
```

**Data Engineering Perspective:**
`UPDATE` statements are critical for maintaining the state of your data. They are used extensively in managing "Slowly Changing Dimensions" (which we will cover later) to update historical records. They are also used for data correction; if bad data is found in a table, an `UPDATE` script is often written to fix it.

---
### **3. `DELETE`: Removing Rows**

The `DELETE FROM` statement is used to remove existing rows from a table. Like `UPDATE`, it should almost always be used with a `WHERE` clause.

**WARNING:** If you omit the `WHERE` clause in a `DELETE` statement, you will delete **all rows** in the table.

**Syntax:**
```sql
DELETE FROM table_name
WHERE condition;
```

**Example:**
Employee Eve Davis (ID 105) leaves the company.

```sql
DELETE FROM employees
WHERE employee_id = 105;
```
This will permanently remove the row for employee 105 from the table.

---
### **Transaction Control**

DML operations are typically executed within a **transaction**. A transaction is a sequence of operations performed as a single logical unit of work. All operations in a transaction must complete successfully, or none of them are applied.

*   `BEGIN TRANSACTION` (or `START TRANSACTION`): Starts a transaction.
*   `COMMIT`: Saves all the changes made in the transaction to the database, making them permanent.
*   `ROLLBACK`: Undoes all the changes made in the transaction, reverting the database to the state it was in before the transaction began.

This is a crucial safety mechanism. If you are in a transaction and realize you made a mistake with an `UPDATE` or `DELETE` statement, you can issue a `ROLLBACK` command (before you `COMMIT`) to undo the error.

**Example:**
```sql
BEGIN TRANSACTION;

-- Give everyone in Engineering a 10% raise
UPDATE employees
SET salary = salary * 1.10
WHERE department_id = 1;

-- Let's check the result before making it permanent
-- SELECT * FROM employees WHERE department_id = 1;
-- (You would review the output here)

-- If everything looks good:
COMMIT;

-- If you made a mistake (e.g., forgot the WHERE clause):
-- ROLLBACK;
```

**Data Engineering Perspective:**
Transactions are the foundation of data integrity. When building a pipeline that loads data into a database, you should wrap your DML operations in a transaction. For example, if your task is to delete yesterday's data and insert today's data, you would wrap both the `DELETE` and `INSERT` statements in a single transaction. If the `INSERT` fails for any reason, the `ROLLBACK` ensures that the `DELETE` is also undone, preventing a state of incomplete or missing data.

***
### **1.5 Data Definition Language (DDL): Defining Data Structures**

While DML commands modify the data *inside* tables, Data Definition Language (DDL) commands are used to define and manage the database objects themselves—primarily the tables. DDL statements create the "skeleton" of the database that will later be populated and modified by DML commands.

The main DDL commands are `CREATE`, `ALTER`, and `DROP`.

---
### **1. `CREATE TABLE`: Building Your Tables**

The `CREATE TABLE` statement is used to construct a new table in your database. When creating a table, you must define each column with a name and a data type. You also define **constraints**, which are rules to enforce data integrity.

**Common Data Types:**

| Data Type           | Description                                                 |
| :------------------ | :---------------------------------------------------------- |
| `INTEGER` or `INT`  | Whole numbers.                                              |
| `VARCHAR(n)`        | Variable-length string of characters, with a maximum length of `n`. |
| `CHAR(n)`           | Fixed-length string of characters.                          |
| `TEXT`              | Long-form text of variable length.                          |
| `DATE`              | Stores a date (year, month, day).                           |
| `TIMESTAMP`         | Stores a date and time. Can include time zone information.  |
| `BOOLEAN`           | Stores `TRUE` or `FALSE` values.                            |
| `DECIMAL(p, s)`     | Fixed-precision number with `p` total digits and `s` decimal places. Essential for financial data. |
| `FLOAT`             | Floating-point number.                                      |

**Common Constraints:**

*   `PRIMARY KEY`: Uniquely identifies each record in a table. It must contain unique values and cannot contain `NULL` values. A table can only have one primary key.
*   `FOREIGN KEY`: Uniquely identifies a record in *another* table. It is the link between tables and is crucial for enforcing referential integrity.
*   `NOT NULL`: Ensures that a column cannot have a `NULL` value.
*   `UNIQUE`: Ensures that all values in a column are different from each other.
*   `DEFAULT`: Provides a default value for a column when no value is specified during an `INSERT`.

**Example:**
Creating the `departments` and `employees` tables we've been using.

```sql
CREATE TABLE departments (
    department_id   INTEGER PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    location        VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employees (
    employee_id     INTEGER PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50),
    department_id   INTEGER,
    hire_date       DATE NOT NULL,
    salary          DECIMAL(10, 2), -- e.g., 99,999,999.99

    -- Define the foreign key constraint
    CONSTRAINT fk_department
        FOREIGN KEY(department_id) 
        REFERENCES departments(department_id)
);
```
This structure ensures that an `employee` cannot be created with a `department_id` that does not already exist in the `departments` table.

---
### **2. `ALTER TABLE`: Modifying Existing Tables**

As requirements change, you will inevitably need to modify the structure of your existing tables. The `ALTER TABLE` statement is used for this purpose.

**Common `ALTER` Operations:**

*   **Adding a Column:**
    ```sql
    ALTER TABLE employees
    ADD COLUMN email VARCHAR(100) UNIQUE;
    ```
*   **Dropping a Column:**
    ```sql
    ALTER TABLE employees
    DROP COLUMN last_name;
    ```
*   **Modifying a Column's Data Type:** (Syntax can vary between databases)
    ```sql
    -- PostgreSQL syntax
    ALTER TABLE employees
    ALTER COLUMN salary TYPE DECIMAL(12, 2);
    ```
*   **Adding a Constraint:**
    ```sql
    ALTER TABLE employees
    ADD CONSTRAINT check_salary_positive CHECK (salary > 0);
    ```

---
### **3. `DROP TABLE`: Deleting Tables**

The `DROP TABLE` statement is used to permanently delete a table, including all its data, indexes, triggers, and constraints. This action is irreversible.

```sql
DROP TABLE employees;
```

**`TRUNCATE TABLE` vs. `DELETE` vs. `DROP`**

It's important to understand the difference between these three commands:

*   `DELETE FROM employees WHERE ...;`: This is a DML command. It removes rows one by one and logs each deletion. It can be rolled back. It's slower for large tables.
*   `TRUNCATE TABLE employees;`: This is a DDL command. It quickly removes *all* rows from a table by deallocating the data pages. It does not log individual row deletions, so it's much faster than `DELETE`. It cannot be rolled back in most database systems. The table structure remains.
*   `DROP TABLE employees;`: This is a DDL command. It removes all data *and* the table structure itself. It is permanent and irreversible.

---
### **Data Engineering Perspective**

*   **Infrastructure as Code**: DDL scripts are the "source code" for your database schema. Data engineers write and maintain these scripts to build the structure of their data warehouses, data marts, and staging areas. These scripts should always be kept under version control (e.g., Git) to track changes over time.
*   **Schema Evolution**: When a source system adds a new field, a data engineer is responsible for "evolving" the schema of the downstream tables. This involves writing an `ALTER TABLE ... ADD COLUMN` script and deploying it to production databases. Tools like **dbt**, Flyway, or Liquibase are often used to manage these schema migrations in a systematic and repeatable way.
*   **Staging Tables**: A very common pattern is to `CREATE` a "staging" table that has a schema that loosely matches a source file or API response. Raw data is loaded into the staging table first, and then SQL `INSERT ... SELECT` statements are used to clean, transform, and load that data into the final, well-structured analytics tables. The staging tables are then often truncated (`TRUNCATE TABLE`) to be ready for the next run.


## Chapter 2: Advanced SQL & Data Modeling

With the fundamentals in place, we can now explore the techniques that allow for more complex and sophisticated data transformations. This section focuses on writing cleaner, more readable queries and introduces the core principles of data modeling used in analytics. These skills are what enable a data engineer to move beyond simple data retrieval and start building robust, scalable, and analysis-ready datasets.

### **2.1 Complex Queries: Managing Logic and Readability**

As your data retrieval logic becomes more complex, a single `SELECT` statement can become long, nested, and difficult to understand. SQL provides several constructs for breaking down complex logic into manageable, logical steps: Subqueries, Common Table Expressions (CTEs), and Views.

---
### **1. Subqueries (or Inner Queries)**

A **subquery** is a `SELECT` statement that is nested inside another SQL statement. The subquery is executed first, and its result is used by the outer query. Subqueries can be used in the `WHERE`, `FROM`, and `SELECT` clauses.

**Example Scenario:** Find all employees who work in 'Building A'.

The `employees` table does not have location information. We must first find which `department_id`s are in 'Building A' from the `departments` table and then use that list to filter the `employees` table.

**Using a Subquery in the `WHERE` Clause:**

```sql
SELECT first_name, last_name
FROM employees
WHERE department_id IN (
    SELECT department_id
    FROM departments
    WHERE location = 'Building A'
);
```
**Execution Flow:**
1.  The inner query `(SELECT department_id FROM departments WHERE location = 'Building A')` runs first, returning the result set `(1)`.
2.  The outer query then becomes `SELECT first_name, last_name FROM employees WHERE department_id IN (1);`, which is then executed.

**Result:**
| first_name | last_name |
| :--------- | :-------- |
| Alice      | Williams  |
| Bob        | Johnson   |

**Using a Subquery in the `FROM` Clause:**
When a subquery is used in the `FROM` clause, it acts as a temporary table. It must be given an alias.

```sql
SELECT
    avg_salaries.department_name,
    avg_salaries.avg_dept_salary
FROM (
    -- This subquery creates a temporary table of department salary averages
    SELECT
        d.department_name,
        AVG(e.salary) as avg_dept_salary
    FROM
        employees AS e
    JOIN
        departments AS d ON e.department_id = d.department_id
    GROUP BY
        d.department_name
) AS avg_salaries
WHERE
    avg_salaries.avg_dept_salary > 90000;
```
While powerful, nested subqueries can quickly become difficult to read and debug. This is where CTEs provide a much cleaner alternative.

---
### **2. Common Table Expressions (CTEs)**

A **Common Table Expression (CTE)** is a temporary, named result set that you can reference within a `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement. CTEs are defined using a `WITH` clause before the main query.

Their primary purpose is to improve the readability and structure of complex queries by breaking them down into logical, sequential steps.

**Example:** Rewriting the previous subquery example using a CTE.

```sql
WITH DepartmentAvgSalaries AS (
    -- Step 1: Calculate the average salary for each department
    SELECT
        d.department_name,
        AVG(e.salary) as avg_dept_salary
    FROM
        employees AS e
    JOIN
        departments AS d ON e.department_id = d.department_id
    GROUP BY
        d.department_name
)
-- Step 2: Query the result of the CTE
SELECT
    department_name,
    avg_dept_salary
FROM
    DepartmentAvgSalaries
WHERE
    avg_dept_salary > 90000;
```
The result is identical to the subquery version, but the logic is far easier to follow. You read it from top to bottom, understanding each logical step before moving to the next. You can also chain CTEs, where each subsequent CTE can reference any of the ones defined before it.

---
### **3. Views: Stored Queries**

A **View** is a virtual table whose contents are defined by a `SELECT` query. Unlike a CTE, which exists only for the duration of a single query, a View is a persistent database object. It is a stored query that you can interact with as if it were a regular table.

Views are used to simplify complexity, provide a stable interface for users, and enforce security.

**Creating a View:**

```sql
CREATE VIEW employee_department_details AS
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name,
    d.location
FROM
    employees AS e
LEFT JOIN
    departments AS d ON e.department_id = d.department_id;
```
Now, a virtual table named `employee_department_details` exists in the database.

**Querying a View:**
End-users (like data analysts) can now query this simple view without needing to know about the underlying `JOIN` logic.

```sql
-- An analyst can run this simple query:
SELECT first_name, department_name
FROM employee_department_details
WHERE location = 'Building A';
```
When this query is run, the database engine executes the `SELECT` statement stored in the view's definition and then applies the `WHERE` clause from the user's query.

**Benefits of Views:**
*   **Simplicity**: Hides complex joins and calculations from end-users.
*   **Consistency**: Provides a consistent representation of data. If the underlying table structure changes, you may only need to update the view, and the end-users' queries will continue to work without modification.
*   **Security**: You can use views to expose only certain columns or rows of a table to specific users, providing a layer of access control. For example, a view could exclude salary information for general use.

---
### **Data Engineering Perspective**

*   **CTEs are the building blocks of modern data transformation.** In an ELT workflow, a single transformation "model" (e.g., in dbt) is almost always structured as a series of chained CTEs. The first CTE might select from a raw source table, the next might clean and standardize data, a third might join it with another table, and the final `SELECT` statement queries the last CTE to produce the final, transformed table. This makes the logic highly readable, testable, and maintainable.
*   **Subqueries are for tactical, simple lookups.** While CTEs are preferred for complex logic, a simple subquery in a `WHERE` clause can be perfectly clear and effective for a one-off filter.
*   **Views are for creating the "presentation layer" of your data warehouse.** After you have built your final, clean, analytics-ready tables, you often create a layer of views on top of them. These views can provide user-friendly column names, perform simple calculations, or filter data for specific business units. This gives data analysts a clean, stable, and secure set of "tables" to connect their BI tools (like Tableau or Looker) to, abstracting away the complexity of the underlying data model.

***
### **2.2 Window Functions: The "Secret Sauce" of Advanced SQL**

Standard aggregate functions (`SUM`, `AVG`, `COUNT`, etc.) operate on an entire group of rows defined by `GROUP BY`, collapsing those rows into a single summary row. **Window functions** are a powerful and sophisticated feature that also perform a calculation across a set of rows, but they do **not** collapse the output. They return a value for *each* row based on a "window" of related rows.

This allows you to perform complex analyses like calculating running totals, moving averages, and rankings without having to perform complicated self-joins or subqueries. Mastering window functions is a significant step towards advanced SQL proficiency.

**The `OVER()` Clause:**
The magic of a window function is in the `OVER()` clause, which defines the "window" of rows to operate on. The `OVER()` clause has three key components:

*   `PARTITION BY`: Divides the rows into partitions (groups). The window function is applied independently to each partition. This is similar to `GROUP BY` but doesn't collapse the rows.
*   `ORDER BY`: Orders the rows within each partition. This is essential for functions that depend on order, like ranking or running totals.
*   `ROWS BETWEEN ...`: Specifies the subset of rows within the partition to use (the "frame"). For example, `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` would create a 3-row moving window.

---
### **1. Ranking Functions**

Ranking functions assign a rank to each row within a partition based on a specified ordering.

**Example Scenario:** Rank employees within each department based on their salary (highest first).

**The Functions:**
*   `ROW_NUMBER()`: Assigns a unique, sequential integer to each row (1, 2, 3, 4...).
*   `RANK()`: Assigns a rank to each row. Leaves gaps in the ranking if there are ties. (1, 2, 2, 4).
*   `DENSE_RANK()`: Assigns a rank without gaps. If there are ties, the next rank is the next sequential integer. (1, 2, 2, 3).

```sql
SELECT
    first_name,
    department,
    salary,
    ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK()       OVER(PARTITION BY department ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS dense_rnk
FROM
    employees;
```
**Execution Flow:**
1.  `PARTITION BY department`: The data is first grouped by department ('Engineering', 'Sales', 'HR').
2.  `ORDER BY salary DESC`: Within each department group, the rows are sorted by salary from highest to lowest.
3.  The ranking functions are then applied to each sorted group independently.

**Result (example):**
| first_name | department    | salary | row_num | rnk | dense_rnk |
| :--------- | :------------ | :----- | :------ | :-- | :-------- |
| Bob        | Engineering   | 115000 | 1       | 1   | 1         |
| **Chris**  | **Engineering**   | **90000**  | **2**       | **2**   | **2**         |
| **Alice**  | **Engineering**   | **90000**  | **3**       | **2**   | **2**         |
| David      | Sales         | 82000  | 1       | 1   | 1         |
| Charlie    | Sales         | 78000  | 2       | 2   | 2         |
| Eve        | HR            | 65000  | 1       | 1   | 1         |

*Notice the difference between the functions for Alice and Chris, who have the same salary.*

---
### **2. Aggregate Window Functions**

You can use standard aggregate functions (`SUM`, `AVG`, `COUNT`, etc.) as window functions. This allows you to, for example, calculate a running total or see how each row's value compares to the group's average.

**Example Scenario:** For each employee, show their salary and the average salary for their department.

```sql
SELECT
    first_name,
    department,
    salary,
    -- The AVG function is applied to the window defined by the department partition
    AVG(salary) OVER(PARTITION BY department) AS avg_dept_salary
FROM
    employees;
```
**Result:**
| first_name | department    | salary | avg_dept_salary |
| :--------- | :------------ | :----- | :-------------- |
| Alice      | Engineering   | 90000  | 102500.00       |
| Bob        | Engineering   | 115000 | 102500.00       |
| Charlie    | Sales         | 78000  | 80000.00        |
| David      | Sales         | 82000  | 80000.00        |
| Eve        | HR            | 65000  | 65000.00        |

**Calculating a Running Total:**
By adding an `ORDER BY` clause, the frame changes. By default, it becomes `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which is perfect for a running total.

```sql
SELECT
    first_name,
    hire_date,
    -- Calculate the cumulative number of hires over time
    COUNT(*) OVER(ORDER BY hire_date) AS cumulative_hires
FROM
    employees;
```
**Result:**
| first_name | hire_date  | cumulative_hires |
| :--------- | :--------- | :--------------- |
| Bob        | 2021-11-01 | 1                |
| David      | 2022-05-10 | 2                |
| Alice      | 2022-08-15 | 3                |
| ...        | ...        | ...              |

---
### **3. Offset Functions: `LAG()` and `LEAD()`**

These functions allow you to access data from a different row within the same result set without a self-join.

*   `LAG(column, n, default)`: Accesses the value of `column` from `n` rows *before* the current row.
*   `LEAD(column, n, default)`: Accesses the value of `column` from `n` rows *after* the current row.

**Example Scenario:** For each employee, show their salary and the salary of the next employee hired in their department.

```sql
SELECT
    first_name,
    department,
    hire_date,
    salary,
    LEAD(salary, 1) OVER(PARTITION BY department ORDER BY hire_date) AS next_hired_employee_salary
FROM
    employees;
```
**Result:**
| first_name | department    | hire_date  | salary | next_hired_employee_salary |
| :--------- | :------------ | :--------- | :----- | :------------------------- |
| Bob        | Engineering   | 2021-11-01 | 115000 | 90000                      |
| Alice      | Engineering   | 2022-08-15 | 90000  | NULL                       |
| David      | Sales         | 2022-05-10 | 82000  | 78000                      |
| Charlie    | Sales         | 2023-02-20 | 78000  | NULL                       |
| Eve        | HR            | 2023-01-09 | 65000  | NULL                       |

---
### **Data Engineering Perspective**

*   **Deduplication and Sessionization**: A common use case is to find the most recent record for each entity. You can use `ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY event_timestamp DESC) AS rn` and then select only the rows `WHERE rn = 1`. This is a highly efficient way to deduplicate records.
*   **Calculating Deltas and Growth**: `LAG()` is the go-to function for comparing a value from the current period to the previous period. To calculate month-over-month sales growth, you would `PARTITION BY product_id ORDER BY month` and then calculate `(current_month_sales - LAG(current_month_sales, 1) OVER(...)) / LAG(current_month_sales, 1) OVER(...)`.
*   **Enriching Data without Collapsing It**: The key benefit of window functions is that they allow you to add contextual information (like a group average or rank) to a row without losing the row's original detail. This is perfect for creating enriched, analysis-ready tables where an analyst can see both the individual data point and its context within the group on the same row. This is often far more useful than a `GROUP BY` summary, which discards the row-level detail.

***
### **2.3 Advanced Techniques**

Beyond window functions, there are several other advanced SQL techniques that are invaluable for data transformation and analysis. This section covers methods for restructuring data, creating reusable logic blocks, and optimizing query performance through pre-computation.

---
### **1. Pivoting Data**

Pivoting is the process of turning unique row values into columns. This is a common requirement in reporting and analytics, where you might want to transform data from a "long" format to a "wide" format.

While some SQL dialects have a dedicated `PIVOT` function (e.g., SQL Server, Snowflake), the most universal and flexible way to pivot data is by using **conditional aggregation** with the `CASE` statement.

**Example Scenario:**
You have a table `quarterly_sales` in a "long" format:
| product_id | quarter | sales_amount |
| :--------- | :------ | :----------- |
| P101       | Q1      | 5000         |
| P101       | Q2      | 6500         |
| P101       | Q3      | 7000         |
| P202       | Q1      | 3000         |
| P202       | Q2      | 3200         |

You want to transform it into a "wide" format where each quarter is its own column.

```sql
SELECT
    product_id,
    SUM(CASE WHEN quarter = 'Q1' THEN sales_amount ELSE 0 END) AS sales_q1,
    SUM(CASE WHEN quarter = 'Q2' THEN sales_amount ELSE 0 END) AS sales_q2,
    SUM(CASE WHEN quarter = 'Q3' THEN sales_amount ELSE 0 END) AS sales_q3,
    SUM(CASE WHEN quarter = 'Q4' THEN sales_amount ELSE 0 END) AS sales_q4
FROM
    quarterly_sales
GROUP BY
    product_id;
```
**Execution Flow:**
1.  `GROUP BY product_id`: The data is grouped by `P101` and `P202`.
2.  `SUM(CASE WHEN ...)`: For each group, the `SUM` function is applied.
    *   For the `P101` group, `sales_q1` will be `SUM(5000, 0, 0)`, `sales_q2` will be `SUM(0, 6500, 0)`, and so on.
    *   The `CASE` statement effectively "picks out" the value for the correct column, and the `SUM` collapses the rows.

**Result:**
| product_id | sales_q1 | sales_q2 | sales_q3 | sales_q4 |
| :--------- | :------- | :------- | :------- | :------- |
| P101       | 5000     | 6500     | 7000     | 0        |
| P202       | 3000     | 3200     | 0        | 0        |

---
### **2. Stored Procedures and User-Defined Functions (UDFs)**

As you build complex data pipelines, you'll often find yourself rewriting the same piece of logic. Stored Procedures and User-Defined Functions (UDFs) allow you to save reusable blocks of code within the database itself.

**User-Defined Function (UDF):**
A UDF accepts parameters and returns a single value (a scalar UDF) or a table (a table-valued UDF). They can be used directly within a `SELECT` statement, just like built-in functions.

**Example: A scalar UDF to standardize country names.**
```sql
-- Syntax varies significantly between databases. This is a PostgreSQL example.
CREATE OR REPLACE FUNCTION standardize_country_name(country_input TEXT)
RETURNS TEXT AS $$
BEGIN
    IF country_input IN ('USA', 'United States', 'US') THEN
        RETURN 'United States of America';
    ELSIF country_input IN ('GB', 'UK', 'United Kingdom') THEN
        RETURN 'United Kingdom';
    ELSE
        RETURN country_input;
    END IF;
END;
$$ LANGUAGE plpgsql;
```
You can now use this function in any query:
```sql
SELECT
    transaction_id,
    standardize_country_name(source_country) AS clean_country
FROM
    raw_transactions;
```

**Stored Procedure:**
A stored procedure is a set of SQL statements that are saved and can be executed by calling its name. Unlike a UDF, it does not have to return a value. It can perform a series of actions, including DML operations (`INSERT`, `UPDATE`, `DELETE`), transaction control, and calling other procedures.

**Example: A procedure to archive old data.**
```sql
-- PostgreSQL syntax
CREATE OR REPLACE PROCEDURE archive_old_logs(archive_date DATE)
AS $$
BEGIN
    -- Step 1: Insert old logs into the archive table
    INSERT INTO log_archive (log_id, event_timestamp, details)
    SELECT log_id, event_timestamp, details
    FROM logs
    WHERE event_timestamp < archive_date;

    -- Step 2: Delete the archived logs from the main table
    DELETE FROM logs
    WHERE event_timestamp < archive_date;

    -- Commit the transaction
    COMMIT;
END;
$$ LANGUAGE plpgsql;
```
You would then execute this procedure as part of a maintenance job: `CALL archive_old_logs('2023-01-01');`

---
### **3. Materialized Views**

We previously discussed that a **View** is a stored query that is executed every time it's accessed. If the query inside the view is complex and runs against billions of rows, querying the view can be slow.

A **Materialized View** is a database object that stores the *results* of a query, just like a regular table. It is a physical snapshot of the data from a specific point in time.

**Benefits:**
*   **Performance**: Querying a materialized view is as fast as querying a table because the expensive computation has already been done.
*   **Simplicity**: It provides the same simplicity as a regular view, hiding complex logic from end-users.

**The Trade-off:**
The data in a materialized view is not always up-to-date. You must **refresh** it periodically to reflect the latest changes in the underlying base tables.

**Example:**
Creating a materialized view for daily sales summaries.

```sql
-- PostgreSQL syntax
CREATE MATERIALIZED VIEW daily_product_sales AS
SELECT
    DATE_TRUNC('day', transaction_timestamp) AS sales_date,
    product_id,
    COUNT(*) AS transactions_count,
    SUM(sale_amount) AS total_revenue
FROM
    transactions
GROUP BY
    1, 2; -- Group by column position
```
Initially, this computes and stores the summary data. Querying it is very fast:
```sql
SELECT * FROM daily_product_sales WHERE sales_date = '2023-10-26';
```
However, as new transactions are added to the `transactions` table, this view becomes stale. You must run a command to update it:
```sql
REFRESH MATERIALIZED VIEW daily_product_sales;
```
This refresh process can be slow and resource-intensive, so it's typically scheduled to run during off-peak hours (e.g., once a night).

---
### **Data Engineering Perspective**

*   **Pivoting for Reports**: Conditional aggregation is a fundamental technique for preparing data for specific reporting layouts required by business users.
*   **UDFs for Reusable Logic**: UDFs are excellent for encapsulating common data cleaning and standardization business rules. By defining `standardize_country_name()`, you ensure that every pipeline applies the exact same logic, promoting consistency. However, be aware that UDFs can sometimes be a performance bottleneck if not written carefully.
*   **Stored Procedures for Orchestration**: Stored procedures are often used to orchestrate sequences of DML operations within the database, forming the core logic of an ELT process. A master procedure might call several other procedures to load, transform, and validate data in a specific order.
*   **Materialized Views for Performance**: Materialized views are the primary tool for performance optimization in a data warehouse. They are the final output of many transformation pipelines. Data engineers build pipelines that run nightly to refresh a set of materialized views, which then serve as the fast, pre-aggregated data sources for all the company's BI dashboards and analytical queries.

## Chapter 3: Data Warehousing & Performance

So far, we have focused on writing SQL queries to transform and analyze data. Now, we shift our focus to designing the systems that store this data for analytical purposes. This section covers the fundamental concepts of data warehousing—the art and science of structuring data for efficient querying and reporting—and the critical techniques used to optimize query performance.

### **3.1 Data Warehouse Design: Star and Snowflake Schemas**

A **data warehouse** is a central repository of integrated data from one or more disparate sources. Its purpose is to support business intelligence, reporting, and analytics. Unlike a transactional database (OLTP), which is optimized for fast read/write operations on individual records, a data warehouse (OLAP - Online Analytical Processing) is optimized for fast, complex queries over large volumes of historical data.

The most popular design paradigm for data warehouses is **dimensional modeling**, which organizes data into **facts** and **dimensions**.

*   **Fact Tables**: Contain the quantitative measurements or "facts" of a business process (e.g., sales amount, quantity sold, number of clicks). Fact tables are typically very long and narrow. They also contain foreign keys that link to dimension tables.
*   **Dimension Tables**: Contain the descriptive attributes or "context" that give meaning to the facts (e.g., product name, customer details, store location). Dimension tables are typically wide and short compared to fact tables.

---
### **1. The Star Schema**

The **star schema** is the simplest and most common dimensional modeling structure. It is characterized by a central fact table that is directly connected to a set of dimension tables. When visualized, it resembles a star, with the fact table at the center and the dimension tables radiating outwards.

**Example: A Simple Sales Star Schema**

**Fact Table: `fct_sales`**
| date_key | product_key | store_key | customer_key | units_sold | sale_amount |
| :------- | :---------- | :-------- | :----------- | :--------- | :---------- |
| 20230115 | 101         | 55        | 987          | 2          | 199.98      |
| 20230115 | 205         | 42        | 345          | 1          | 49.99       |
| 20230116 | 101         | 55        | 112          | 3          | 299.97      |

**Dimension Tables:**
*   **`dim_date`**: `date_key`, `full_date`, `day_of_week`, `month`, `quarter`, `year`
*   **`dim_product`**: `product_key`, `product_name`, `category`, `brand`
*   **`dim_store`**: `store_key`, `store_name`, `city`, `state`, `country`
*   **`dim_customer`**: `customer_key`, `customer_name`, `email`, `loyalty_tier`

**Querying a Star Schema:**
Queries are simple and performant, typically involving a `JOIN` from the central fact table to one or more dimension tables.

```sql
-- Calculate total sales for the 'Electronics' category in 'California' for Q1.
SELECT SUM(s.sale_amount) AS total_sales
FROM fct_sales AS s
JOIN dim_date AS d ON s.date_key = d.date_key
JOIN dim_product AS p ON s.product_key = p.product_key
JOIN dim_store AS st ON s.store_key = st.store_key
WHERE
    p.category = 'Electronics'
    AND st.state = 'California'
    AND d.quarter = 'Q1';
```
**Advantages of Star Schema:**
*   **Simple and Readable**: The query structure is straightforward.
*   **High Performance**: Fewer `JOIN`s are required, leading to faster query execution.
*   **Intuitive for Analysts**: Easy for BI tools and end-users to understand and navigate.

---
### **2. The Snowflake Schema**

The **snowflake schema** is an extension of the star schema where one or more dimension tables are **normalized**. This means that a dimension table is split into additional, smaller tables. This creates a schema that can look like a snowflake, with branches coming off the main dimension tables.

**Example: "Snowflaking" the `dim_product` Dimension**

In a star schema, the `dim_product` table might contain the brand name directly. In a snowflake schema, we might normalize this by creating a separate `dim_brand` table.

**`dim_product` (Snowflake version):**
| product_key | product_name | category_key | brand_key |
| :---------- | :----------- | :----------- | :-------- |
| 101         | iPhone 15    | 1            | 1         |
| 102         | Galaxy S23   | 1            | 2         |

**`dim_brand` (New table):**
| brand_key | brand_name | headquarters |
| :-------- | :--------- | :----------- |
| 1         | Apple      | Cupertino    |
| 2         | Samsung    | Seoul        |

A query that needs brand information now requires an extra `JOIN`:
`fct_sales` -> `dim_product` -> `dim_brand`.

**Advantages of Snowflake Schema:**
*   **Reduced Data Redundancy**: Storing brand information once saves space, especially if the dimension attributes are long strings.
*   **Easier Maintenance**: If a brand's headquarters changes, you only need to update it in one place in the `dim_brand` table.

**Disadvantages:**
*   **Increased Complexity**: Queries require more `JOIN`s, which can be harder to write and debug.
*   **Potentially Slower Performance**: More `JOIN` operations can lead to slower query execution times in many modern data warehouse systems.

---
### **3. Slowly Changing Dimensions (SCDs)**

Dimension attributes are not always static. A customer might move to a new city, or a product might be moved to a different category. How you handle these changes is a critical part of dimensional modeling. This is known as managing **Slowly Changing Dimensions (SCDs)**.

*   **Type 1 SCD: Overwrite.** The old value is simply overwritten with the new value. This is the easiest method, but it loses all historical information.
    *   *Example:* Customer moves from 'New York' to 'London'. The city field is updated. You no longer know they used to live in New York.
*   **Type 2 SCD: Add a New Row.** This is the most common and powerful method for preserving history. When a change occurs, the existing row for the dimension is marked as "expired" (e.g., via an `end_date` column), and a new row is inserted with the updated information.
    
    **Example: `dim_customer` with Type 2 SCD**
    | customer_key_surrogate | customer_id | city     | start_date | end_date   | is_current |
    | :--------------------- | :---------- | :------- | :--------- | :--------- | :--------- |
    | 1234                   | 987         | New York | 2020-01-01 | 2023-05-14 | FALSE      |
    | **1235**               | **987**     | **London**   | **2023-05-15** | **9999-12-31** | **TRUE**   |

    The `fct_sales` table would join on the `customer_key_surrogate`. This allows you to accurately analyze historical sales, attributing sales made before May 15th to 'New York' and sales after that date to 'London'.

---
### **Data Engineering Perspective**

*   **The Blueprint for Transformation**: As a data engineer, your job is to build the ETL/ELT pipelines that create and populate these fact and dimension tables from raw source data. Dimensional modeling provides the blueprint for what you are building.
*   **Star Schema is the Default**: In modern analytics databases, the performance penalty of `JOIN`s is still significant, but storage is relatively cheap. For this reason, the **star schema is almost always the preferred choice**. The simplicity and query performance benefits generally outweigh the storage savings of the snowflake schema.
*   **Implementing SCD Logic**: The logic to handle SCD Type 2 changes (detecting a change, expiring the old row, and inserting the new one) is a classic data engineering task. It is a core component of many data warehousing pipelines and is often implemented using `INSERT` and `UPDATE` statements orchestrated within a stored procedure or a tool like dbt.

***
### **3.2 Data Modeling: Normalization, Denormalization, and Surrogate Keys**

Data modeling is the process of creating a visual representation of an entire information system or parts of it to communicate connections between data points and structures. For data engineers, this involves designing the logical and physical structure of databases and data warehouses to ensure data integrity, optimize storage, and facilitate efficient querying. Two fundamental concepts in this design are normalization and denormalization, often complemented by the use of surrogate keys.

---
### **1. Normalization: Reducing Redundancy**

**Normalization** is a database design technique used to organize tables in a way that minimizes data redundancy and improves data integrity. It involves breaking down large tables into smaller, related tables and defining relationships between them. This is primarily done in OLTP (Online Transaction Processing) databases, which are designed for transactional workloads (frequent inserts, updates, and deletes).

Normalization is guided by a set of rules called **Normal Forms (NF)**, with the most common being 1NF, 2NF, and 3NF.

**Example: Before and After Normalization (to 3NF)**

**Initial (Unnormalized) Table: `customer_orders`**
| order_id | customer_name | customer_address      | product_name | product_price | order_date |
| :------- | :------------ | :-------------------- | :----------- | :------------ | :--------- |
| 1        | Alice         | 123 Main St, NY       | Laptop       | 1200          | 2023-01-01 |
| 2        | Bob           | 456 Oak Ave, CA       | Mouse        | 25            | 2023-01-01 |
| 1        | Alice         | 123 Main St, NY       | Keyboard     | 75            | 2023-01-01 |
| 3        | Alice         | 123 Main St, NY       | Monitor      | 300           | 2023-01-02 |

*   **Problems with Redundancy:**
    *   Alice's name and address are repeated for each of her orders.
    *   If Alice's address changes, it must be updated in multiple places.
    *   Wasted storage space.

**Normalized Tables (3NF):**

**`orders` table:**
| order_id | customer_id | order_date |
| :------- | :---------- | :--------- |
| 1        | 1           | 2023-01-01 |
| 2        | 2           | 2023-01-01 |
| 3        | 1           | 2023-01-02 |

**`customers` table:**
| customer_id | customer_name | customer_address      |
| :---------- | :------------ | :-------------------- |
| 1           | Alice         | 123 Main St, NY       |
| 2           | Bob           | 456 Oak Ave, CA       |

**`order_items` (linking `orders` to `products`):**
| order_item_id | order_id | product_id | quantity | item_price |
| :------------ | :------- | :--------- | :------- | :--------- |
| 1             | 1        | 10          | 1        | 1200       |
| 2             | 2        | 20          | 1        | 25         |
| 3             | 1        | 30          | 1        | 75         |
| 4             | 3        | 40          | 1        | 300        |

**`products` table:**
| product_id | product_name | product_price |
| :--------- | :----------- | :------------ |
| 10         | Laptop       | 1200          |
| 20         | Mouse        | 25            |
| 30         | Keyboard     | 75            |
| 40         | Monitor      | 300           |

**Advantages of Normalization:**
*   **Reduced Redundancy**: Data is stored in only one place.
*   **Improved Data Integrity**: Changes to data (e.g., updating a customer address) only need to happen in one place, preventing inconsistencies.
*   **Smaller Tables**: More efficient for transactional inserts/updates/deletes.

**Disadvantages:**
*   **More Joins**: Retrieving a complete view of the data requires joining multiple tables, which can be slower for analytical queries.
*   **More Complex Queries**: Analysts need to understand the relationships between many tables.

---
### **2. Denormalization: Optimizing for Read Performance**

**Denormalization** is the process of intentionally introducing redundancy into a database by combining data from multiple tables into a single table, often to improve query performance. This is the opposite of normalization and is commonly applied in data warehouses (OLAP) where read performance for analytical queries is paramount, and write performance is less critical.

**Example: Denormalized `sales_fact` table for a Data Warehouse**
Combining `orders`, `customers`, and `products` into one wide table for analysis.

| order_id | order_date | customer_id | customer_name | customer_address | product_id | product_name | product_price | quantity | item_price |
| :------- | :--------- | :---------- | :------------ | :--------------- | :--------- | :----------- | :------------ | :------- | :--------- |
| 1        | 2023-01-01 | 1           | Alice         | 123 Main St, NY  | 10         | Laptop       | 1200          | 1        | 1200       |
| 2        | 2023-01-01 | 2           | Bob           | 456 Oak Ave, CA  | 20         | Mouse        | 25            | 1        | 25         |
| 1        | 2023-01-01 | 1           | Alice         | 123 Main St, NY  | 30         | Keyboard     | 75            | 1        | 75         |
| 3        | 2023-01-02 | 1           | Alice         | 123 Main St, NY  | 40         | Monitor      | 300           | 1        | 300        |

**Advantages of Denormalization:**
*   **Faster Analytical Queries**: Fewer `JOIN`s are needed, leading to significantly faster query execution. This is critical for BI dashboards and complex analytical reports.
*   **Simpler Queries for Analysts**: Analysts don't need to understand complex join logic; they can query a single, wide table.

**Disadvantages:**
*   **Increased Data Redundancy**: More storage space required.
*   **More Complex ETL**: Maintaining consistency across redundant data requires more complex ETL/ELT pipelines. If a customer's address changes, the pipeline must update every historical record in the denormalized table, not just one.

---
### **3. Surrogate Keys**

A **surrogate key** is a system-generated, unique identifier for each row in a table, typically an auto-incrementing integer or a UUID (Universally Unique Identifier). It has no business meaning and is used *in place of* a natural key (a key that has business meaning, like `customer_id` from a source system).

**Why use Surrogate Keys in Data Warehouses?**

*   **Handling Slowly Changing Dimensions (SCD Type 2)**: This is the most crucial reason. If you used the `customer_id` from the source system as the primary key in `dim_customer`, you couldn't create multiple rows for the same customer to track historical changes. A surrogate key allows each version of a customer to have a unique identifier, preserving history.
*   **Insulation from Source System Changes**: If the source system changes its primary key (e.g., changes how `customer_id` is generated), your data warehouse remains unaffected because it relies on its own internal surrogate keys.
*   **Simplified Joins**: Surrogate keys are typically integers, which are highly efficient for `JOIN` operations compared to potentially long, composite, or string-based natural keys.
*   **Consistency**: Ensures a consistent primary key type across all dimension tables.

**Example: `dim_customer` with Surrogate Key**

| `customer_sk` (Surrogate Key) | `customer_id` (Natural Key) | customer_name | city     | start_date | end_date   |
| :---------------------------- | :-------------------------- | :------------ | :------- | :--------- | :--------- |
| 1001                          | CUST123                     | Alice         | New York | 2020-01-01 | 2023-05-14 |
| 1002                          | CUST123                     | Alice         | London   | 2023-05-15 | 9999-12-31 |
| 1003                          | CUST456                     | Bob           | Paris    | 2021-03-20 | 9999-12-31 |

The `fct_sales` table would then link to `dim_customer` using `customer_sk`.

---
### **Data Engineering Perspective**

*   **OLTP vs. OLAP Design**: Understand that transactional databases (OLTP) are typically highly normalized for write efficiency and data integrity, while analytical databases (OLAP/data warehouses) are often denormalized for read performance.
*   **The ETL/ELT Challenge**: Your pipelines will be responsible for transforming data from a normalized OLTP source into a denormalized OLAP target, including the generation and management of surrogate keys and SCDs. This is a core competency.
*   **Choosing a Modeling Strategy**: For data warehouses, the Star Schema (a form of denormalization) is generally preferred due to its balance of simplicity and query performance. Surrogate keys are almost always a best practice in data warehousing dimensions.

***
### **3.3 Query Performance and Optimization**

Writing a SQL query that returns the correct result is only half the battle. In a data warehouse with billions of rows, a poorly written query can take hours to run, consume excessive resources, and impact other users. **Query optimization** is the process of writing queries in a way that allows the database's query optimizer to execute them as efficiently as possible.

A data engineer must understand the fundamentals of how a database executes a query to write performant code and to diagnose and fix slow queries.

---
### **1. The Query Optimizer and Execution Plans**

Every major database has a **query optimizer**. When you submit a SQL query, the optimizer does not run it directly. Instead, it:
1.  Parses the query to check for syntax errors.
2.  Generates several possible **execution plans** for how to retrieve the data.
3.  Evaluates the "cost" of each plan based on database statistics (e.g., table size, cardinality, data distribution).
4.  Selects the plan with the lowest estimated cost and executes it.

The most important tool for a data engineer in this process is the **`EXPLAIN`** command. `EXPLAIN` (or `EXPLAIN PLAN`, `SHOWPLAN`, depending on the database) asks the optimizer to show you the execution plan it *would* choose, without actually running the query.

**Example: Reading an Execution Plan**
```sql
EXPLAIN SELECT
    e.first_name,
    d.department_name
FROM
    employees AS e
JOIN
    departments AS d ON e.department_id = d.department_id
WHERE
    d.department_name = 'Engineering';
```
The output will be a tree-like structure showing the steps the database will take. You read it from the most indented step outwards.

**Sample Simplified Plan:**
```
-> Hash Join  (cost=... rows=...)
    -> Seq Scan on employees e  (cost=... rows=...)
    -> Hash
        -> Seq Scan on departments d (filter: department_name = 'Engineering') (cost=... rows=...)
```
This plan tells you the database will:
1.  Perform a **Sequential Scan** on the `departments` table, filtering for 'Engineering'.
2.  Create a **Hash** table in memory from that result.
3.  Perform a full **Sequential Scan** on the `employees` table.
4.  For each employee row, it will use the hash table to find the matching department (a **Hash Join**).

If this query were slow, you would look for expensive operations, like full table scans on very large tables, and think about how to avoid them.

---
### **2. Indexing Strategies**

An **index** is a data structure (most commonly a B-tree) that improves the speed of data retrieval operations on a database table. It works like the index in the back of a book: instead of scanning the whole book (the table) to find a topic (a row), you look up the topic in the index, which tells you the exact page number (the row's physical address on disk).

**When to Use an Index:**
*   On **Primary Key** columns (most databases create this automatically).
*   On **Foreign Key** columns. This is critical for `JOIN` performance.
*   On columns that are frequently used in `WHERE` clauses for filtering.
*   On columns that are frequently used in `ORDER BY` clauses.

**Creating an Index:**
```sql
CREATE INDEX idx_employees_department_id
ON employees (department_id);
```
After creating this index, if we re-run `EXPLAIN` on the previous query, the plan would likely change. Instead of a "Seq Scan on employees", it might use an "Index Scan", which would be much faster if the `employees` table is large.

**The Trade-off:**
Indexes are not free.
*   **Storage**: They take up disk space.
*   **Write Performance**: When you `INSERT`, `UPDATE`, or `DELETE` data, the database must also update the indexes on that table. A table with many indexes will have slower write performance.

Therefore, you should only create indexes that are necessary for your most common and important read queries.

---
### **3. Data Partitioning**

For extremely large tables (billions of rows), even indexes may not be enough. **Partitioning** is a technique that physically divides a large table into smaller, more manageable pieces (partitions) based on a partition key. However, the database treats it as a single table for querying.

Common partitioning strategies include:
*   **Range Partitioning**: Based on a range of values, most commonly a date. For example, a `transactions` table could be partitioned by month.
*   **List Partitioning**: Based on a list of discrete values, such as a region or country.
*   **Hash Partitioning**: Based on a hash value of a key, distributing data evenly across partitions.

**Example:**
Imagine the `transactions` table is partitioned by month. When you run a query like:
```sql
SELECT *
FROM transactions
WHERE transaction_timestamp >= '2023-10-01' AND transaction_timestamp < '2023-11-01';
```
The query optimizer is smart enough to know that it only needs to scan the "October 2023" partition. It completely ignores all other partitions (a technique called **partition pruning**), dramatically reducing the amount of data it needs to read and leading to a massive performance improvement.

---
### **4. Choosing Efficient Data Types**

Using the smallest and most appropriate data type for your columns can save significant storage space and improve query performance, as the database can process more rows in a single I/O operation.

*   Use `INTEGER` for whole numbers instead of `VARCHAR`.
*   Use `DATE` or `TIMESTAMP` for dates instead of `VARCHAR`.
*   Use `BOOLEAN` for true/false flags.
*   If a `VARCHAR` column will never exceed 50 characters, define it as `VARCHAR(50)`, not `VARCHAR(255)` or `TEXT`.

---
### **Data Engineering Perspective**

*   **You are a Performance Detective**: A key responsibility of a data engineer is to investigate and resolve performance issues in the data warehouse. `EXPLAIN` is your primary tool. You must be able to read an execution plan, identify bottlenecks (like full table scans or inefficient join methods), and take corrective action.
*   **Indexing is Your First Go-To**: When a query is slow, the first thing to check is whether the `JOIN` and `WHERE` clause columns are properly indexed. Adding a missing index is often the quickest and most effective way to solve a performance problem.
*   **Partitioning for Big Data**: In large-scale data warehouses, partitioning (especially by date) is a standard and critical design choice. As a data engineer, you will design the partitioning strategy for your largest fact tables and ensure your ETL/ELT pipelines load data into the correct partitions.
*   **Collaboration with Analysts**: You will work closely with data analysts who write their own queries. When they report that a dashboard is slow, you will help them analyze their query, read the execution plan, and suggest optimizations, which may involve rewriting their SQL or adding a new index to the database.

## Chapter 4: SQL in the Modern Data Stack

While the foundational SQL we've covered is timeless, its application has evolved. Modern data stacks rely on new tools and paradigms that place SQL at the very center of data transformation and orchestration. This section explores how SQL is used to build robust data pipelines and how it interacts with the key tools that define modern data engineering.

### **4.1 ETL/ELT Pipelines with SQL**

**ETL (Extract, Transform, Load)** and **ELT (Extract, Load, Transform)** are the two primary patterns for moving data from a source system to a data warehouse.

*   **ETL (Traditional)**:
    1.  **Extract**: Pull data from the source (e.g., a transactional database).
    2.  **Transform**: Run the transformation logic on the data within a separate processing engine (like a Python script using Pandas or a dedicated ETL tool).
    3.  **Load**: Load the pre-transformed, clean data into the data warehouse.

*   **ELT (Modern)**:
    1.  **Extract**: Pull raw data from the source.
    2.  **Load**: Load the raw data directly into a staging area in the data warehouse.
    3.  **Transform**: Use the power of the data warehouse itself to run SQL queries that transform the raw data into clean, analysis-ready tables.

The rise of powerful, cloud-based data warehouses (like Snowflake, BigQuery, and Redshift) has made **ELT the dominant paradigm**. The "T" in ELT is almost always executed using SQL.

---
### **Writing Idempotent Pipelines**

A critical concept in data engineering is **idempotency**. An idempotent operation is one that can be run multiple times without changing the result beyond the initial application. If you run your pipeline once, and then run it again with the same source data, the final state of your data warehouse should be identical. This is crucial for reliability and recovery from failures.

A simple `INSERT` statement is not idempotent. If you run it twice, you will get duplicate data. A common task for a data engineer is to write idempotent SQL logic for loading data, often referred to as an "upsert" (update or insert).

**The `MERGE` Statement:**
The `MERGE` statement is the most elegant and powerful tool for this. It performs `INSERT`, `UPDATE`, or `DELETE` operations on a target table based on the results of a join with a source table.

**Example Scenario:**
You have a staging table `stg_employees` with the latest data for the day, and a final production table `employees`. You want to update existing employees and insert new ones.

```sql
MERGE INTO employees AS target
USING stg_employees AS source
ON target.employee_id = source.employee_id

-- If a match is found (the employee exists), then UPDATE the record.
WHEN MATCHED THEN
    UPDATE SET
        target.salary = source.salary,
        target.department_id = source.department_id

-- If no match is found (it's a new employee), then INSERT a new row.
WHEN NOT MATCHED THEN
    INSERT (employee_id, first_name, last_name, hire_date, salary, department_id)
    VALUES (source.employee_id, source.first_name, source.last_name, source.hire_date, source.salary, source.department_id);
```
Running this `MERGE` statement once will bring the `employees` table up-to-date. Running it a second time will find matches for all rows and perform the same updates, resulting in no net change—achieving idempotency.

---
### **Transaction Management in Pipelines**

As discussed in the DML section, transactions are vital for data integrity. In the context of a SQL-based transformation pipeline, you should wrap a series of dependent DML statements in a single transaction.

**Example: A multi-step transformation.**
A common pattern is to update a dimension table and then a fact table.

```sql
BEGIN TRANSACTION;

-- Step 1: Update the Slowly Changing Dimension table for customers.
MERGE INTO dim_customer ... ;

-- Step 2: Insert today's sales data into the fact table.
-- This might use the new surrogate keys generated in Step 1.
INSERT INTO fct_sales ... ;

-- If both steps succeed, commit the changes.
COMMIT;
-- If either step fails, the entire transaction is automatically rolled back,
-- ensuring the database is not left in an inconsistent state.
```

---
### **4.2 SQL with Modern Tools**

**1. Orchestration Tools (e.g., Apache Airflow)**
An orchestration tool is used to schedule, execute, and monitor data pipelines. Apache Airflow is one of the most popular open-source orchestrators.

In Airflow, a pipeline is defined as a **DAG (Directed Acyclic Graph)** of tasks. A common pattern is to have a DAG where each task is a SQL query that performs one step of a larger transformation.

*   **Task 1**: Load raw data from S3 into a staging table in Snowflake.
*   **Task 2**: Run a SQL script (`transform_users.sql`) that cleans the staged user data and loads it into a `dim_users` table.
*   **Task 3**: Run another SQL script (`transform_orders.sql`) that populates `fct_orders`.
*   **Task 4**: Run a data quality check SQL query on the final tables.

Airflow manages the dependencies between these tasks (e.g., Task 2 only runs after Task 1 succeeds) and handles retries on failure.

**2. Transformation Tools (e.g., dbt)**
**dbt (data build tool)** has revolutionized the "T" in ELT. It is a command-line tool that allows data analysts and engineers to build complex data transformation pipelines using only `SELECT` statements.

**How dbt Works:**
*   You write a `SELECT` statement that defines a new table or view (this is called a "model").
*   You save this `SELECT` statement in a `.sql` file.
*   You use a `ref()` function to refer to other models. dbt uses these references to automatically infer the dependencies between your models and build a DAG.
*   When you run `dbt run`, dbt materializes your models (as tables or views) in your data warehouse in the correct order.

**Example `models/dim_customers.sql` in dbt:**
```sql
-- This model depends on the raw 'stg_customers' and 'stg_orders' models.
WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customer_orders AS (
    SELECT
        customer_id,
        MIN(order_date) as first_order_date,
        MAX(order_date) as most_recent_order_date,
        COUNT(order_id) as number_of_orders
    FROM orders
    GROUP BY 1
)

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    co.first_order_date,
    co.most_recent_order_date,
    coalesce(co.number_of_orders, 0) as number_of_orders
FROM customers c
LEFT JOIN customer_orders co ON c.customer_id = co.customer_id
```
dbt takes this simple `SELECT` query and automatically handles the DDL (`CREATE TABLE AS ...`) and dependency management. It allows teams to build, test, and document large, complex transformation pipelines using only SQL.

### **Data Engineering Perspective**

*   **SQL is the Transformation Engine**: In the modern data stack, SQL is not just for querying; it is the primary language for data transformation. You will spend a significant amount of your time writing SQL that cleans, joins, aggregates, and models data within the data warehouse.
*   **Embrace ELT**: The ELT paradigm leverages the immense power of cloud data warehouses. Your job is to get data into the warehouse efficiently and then orchestrate the SQL-based transformations.
*   **Master Idempotency**: Learning how to write idempotent DML, especially using the `MERGE` statement, is a critical skill for building reliable and recoverable data pipelines.
*   **Learn the Tooling**: While SQL is the core language, its power is magnified by tools like Airflow and dbt. Learning how to structure your SQL within these frameworks is what it means to be a modern data engineer. dbt, in particular, has become a standard for the transformation layer, and proficiency in it is highly valued.

