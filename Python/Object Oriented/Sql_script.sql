CREATE TABLE IF NOT EXISTS MovieIndex (
    MovieID INTEGER PRIMARY KEY,
    MovieName TEXT,
    MovieSeatsLeft INTEGER,
    MovieTheaterID INTEGER
);

CREATE TABLE IF NOT EXISTS Theater (
	TheaterID	INTEGER PRIMARY KEY,
	TheaterName	TEXT UNIQUE,
	TheaterSeats	INTEGER,
);

INSERT INTO MovieIndex (MovieID, MovieName, MovieSeatsLeft, MovieTheaterID) VALUES
(1, 'The Matrix', 30, 1),
(2, 'Inception', 50, 2),
(3, 'Interstellar', 100, 3),
(4, 'The Dark Knight', 20, 1),
(5, 'Avatar', 70, 2),
(6, 'Avengers: Endgame', 120, 3),
(7, 'The Lord of the Rings', 10, 1),
(8, 'Pirates of the Caribbean', 50, 2),
(9, 'Titanic', 180, 3),
(10, 'Jurassic Park', 40, 1),
(11, 'Toy Story', 60, 2),
(12, 'Finding Nemo', 160, 3),
(13, 'Harry Potter', 70, 1),
(14, 'Star Wars', 80, 2),
(15, 'Frozen', 150, 3),
(16, 'Spider-Man', 25, 1),
(17, 'Black Panther', 95, 2),
(18, 'Iron Man', 170, 3),
(19, 'Shrek', 60, 1),
(20, 'Mission Impossible', 110, 2);
