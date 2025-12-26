create database if not exists library_db;
use library_db;

-- 1. books table
create table books (
    book_id int auto_increment primary key,
    title varchar(150) not null,
    author varchar(100),
    price decimal(10, 2),
    stock int default 1
);

insert into books (title, author, price, stock) values 
('harry potter', 'jk rowling', 500.00, 5),
('rich dad poor dad', 'robert kiyosaki', 350.00, 3),
('wings of fire', 'apj abdul kalam', 400.00, 4),
('the alchemist', 'paulo coelho', 300.00, 6),
('python programming', 'guido van rossum', 650.00, 2),
('sherlock holmes', 'arthur conan doyle', 250.00, 4),
('atomic habits', 'james clear', 450.00, 5),
('godan', 'munshi premchand', 150.00, 8),
('history of india', 'rc majumdar', 550.00, 2),
('think and grow rich', 'napoleon hill', 200.00, 5);

select * from books;

-- 2. members table
create table members (
    mem_id int auto_increment primary key,
    name varchar(100) not null,
    phone varchar(15) unique,
    join_date date default (curdate())
);

insert into members (name, phone) values 
('amit kumar', '9988771122'),
('priya singh', '8877665544'),
('rahul verma', '7766554433'),
('sneha gupta', '6655443322'),
('vikram rathore', '5544332211'),
('anjali mehta', '4433221100'),
('rohit sharma', '3322110099'),
('kavita das', '2211009988'),
('arjun reddy', '1100998877'),
('pooja mishra', '9900887766');

select * from members;

-- 3. issue_record table
create table issue_record (
    issue_id int auto_increment primary key,
    mem_id int,
    book_id int,
    issue_date date default (curdate()),
    return_date date,
    status enum('borrowed', 'returned') default 'borrowed',
    foreign key (mem_id) references members(mem_id),
    foreign key (book_id) references books(book_id)
);

insert into issue_record (mem_id, book_id, issue_date, status) values 
(1, 1, '2023-10-01', 'borrowed'),
(2, 4, '2023-10-02', 'borrowed'),
(3, 5, '2023-10-03', 'returned'),
(4, 2, '2023-10-05', 'borrowed'),
(5, 8, '2023-10-06', 'borrowed'),
(6, 3, '2023-10-07', 'returned'),
(1, 7, '2023-10-10', 'borrowed'),
(7, 9, '2023-10-12', 'borrowed'),
(8, 10, '2023-10-15', 'returned'),
(9, 6, '2023-10-18', 'borrowed');

select * from issue_record;

-- check karne ke liye ki kisne kya liya
select m.name, b.title, i.issue_date, i.status
from issue_record i
join members m on i.mem_id = m.mem_id
join books b on i.book_id = b.book_id;