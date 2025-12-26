create database if not exists dukaan_db;
use dukaan_db;

create table categories (
    cat_id int auto_increment primary key,
    cat_name varchar(100) not null
);
insert into categories (cat_name) values ('grocery'), ('electronics');
select * from categories;

create table suppliers (
    sup_id int auto_increment primary key,
    company_name varchar(100) not null,
    phone varchar(15)
);
insert into suppliers (company_name, phone) values ('sharma distributors', '9988776655');
select * from suppliers;

create table products (
    p_id int auto_increment primary key,
    p_name varchar(150) not null,
    cat_id int,
    sup_id int,
    price decimal(10, 2) not null,
    stock int default 0,
    sku varchar(50) unique,
    foreign key (cat_id) references categories(cat_id),
    foreign key (sup_id) references suppliers(sup_id)
);
insert into products (p_name, cat_id, sup_id, price, stock, sku) values 
('basmati rice 1kg', 1, 1, 120.00, 50, 'gro-001'),
('headphones', 2, 1, 500.00, 10, 'ele-001');
select * from products;

create table customers (
    cust_id int auto_increment primary key,
    name varchar(100) not null,
    phone varchar(15) unique,
    address text,
    join_date datetime default current_timestamp
);
insert into customers (name, phone) values ('rahul verma', '9876543210');
select * from customers;

create table orders (
    order_id int auto_increment primary key,
    cust_id int,
    order_date datetime default current_timestamp,
    total_amount decimal(10, 2),
    pay_mode enum('cash', 'online', 'card') default 'cash',
    foreign key (cust_id) references customers(cust_id)
);
insert into orders (cust_id, total_amount, pay_mode) values (1, 500.00, 'online');
select * from orders;

create table order_items (
    item_id int auto_increment primary key,
    order_id int,
    p_id int,
    qty int not null,
    price decimal(10, 2),
    foreign key (order_id) references orders(order_id),
    foreign key (p_id) references products(p_id)
);
insert into order_items (order_id, p_id, qty, price) values (1, 2, 1, 500.00);
select * from order_items;