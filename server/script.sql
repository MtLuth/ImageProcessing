
create database xulyanh;

create table license (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    license VARCHAR(120) UNIQUE NOT NULL,
    gioVao VARCHAR(120),
    gioRa VARCHAR(120),
    maThe VARCHAR(120),
);
