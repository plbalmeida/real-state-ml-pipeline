CREATE TABLE IF NOT EXISTS tb01 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(255),
    sector VARCHAR(255),
    net_usable_area FLOAT,
    net_area FLOAT,
    n_rooms INT,
    n_bathroom INT,
    latitude FLOAT,
    longitude FLOAT,
    price FLOAT
);
