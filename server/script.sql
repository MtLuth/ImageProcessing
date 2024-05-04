
create database xulyanh;

create table parking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license VARCHAR(120) UNIQUE NOT NULL,
    check_in VARCHAR(120),
    check_out VARCHAR(120),
    series_number VARCHAR(120) 
);
