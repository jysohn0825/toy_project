CREATE TABLE drowsiness(
	d_id CHAR(10)  PRIMARY KEY,
    d_pw CHAR(15),
    d_phone CHAR(13)
);


CREATE TABLE d_time(
	d_id CHAR(10),
    d_time CHAR(30),
    FOREIGN KEY (d_id) REFERENCES drowsiness(d_id)
);