CREATE DATABASE Sonata;
USE Sonata;

CREATE TABLE user (
    email VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50),
    date_of_birth DATE,
    gender VARCHAR(20),
    profile_iamge VARCHAR(99),
    password VARCHAR(100)
);

CREATE TABLE playlist (
    playlist_id INT PRIMARY KEY AUTO_INCREMENT,
    user_email VARCHAR(50),
    playlist_name VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_email) REFERENCES user(email)
);

CREATE TABLE track (
    track_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    duration TIME,
    artist VARCHAR(100),
    album VARCHAR(100),
    genre VARCHAR(50)
);

CREATE TABLE playlist_track (
    playlist_id INT,
    track_id INT,
    FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id),
    FOREIGN KEY (track_id) REFERENCES track(track_id),
    PRIMARY KEY (playlist_id, track_id)
);
playlist_track