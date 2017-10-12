CREATE TABLE Players (
  PRIMARY KEY (name),
  name       VARCHAR(100) NOT NULL,
  draft_rank INTEGER NOT NULL,
  PER        REAL NOT NULL CHECK (PER > 0)
);

CREATE TABLE Colleges (
  PRIMARY KEY (name),
  name VARCHAR(100) NOT NULL
);

CREATE TABLE Seasons (
  PRIMARY KEY (year),
  year INTEGER NOT NULL
);

CREATE TABLE CollegePerformances (
  PRIMARY KEY (college, season),
  FOREIGN KEY (college) REFERENCES Colleges(name),
  FOREIGN KEY (season) REFERENCES Seasons(year),
  college VARCHAR(100) NOT NULL,
  season    INTEGER NOT NULL,
  win     INTEGER NOT NULL,
  loss    INTEGER NOT NULL
);

CREATE TABLE PlayerPerformances (
  PRIMARY KEY (player, season),
  FOREIGN KEY (player) REFERENCES Players(name),
  FOREIGN KEY (season) REFERENCES Seasons(year),
  player VARCHAR(100) NOT NULL,
  season INTEGER NOT NULL,
  height REAL NOT NULL CHECK (height > 0),
  weight REAL NOT NULL CHECK (weight > 0),
  PER    REAL NOT NULL CHECK (PER > 0)
);

CREATE TABLE CollegeRoster (
  PRIMARY KEY (college, player),
  FOREIGN KEY (college) REFERENCES Colleges(name),
  FOREIGN KEY (player) REFERENCES Players(name),
  college    VARCHAR(100) NOT NULL,
  player     VARCHAR(100) NOT NULL,
  start_year INTEGER NOT NULL,
  end_year   INTEGER NOT NULL
);

-- Some fake sample data
INSERT INTO Players VALUES
  ('Brandon Ingram', 30, 15);
INSERT INTO Colleges VALUES
  ('Duke'),
  ('UNC');
INSERT INTO Seasons VALUES
  (2016);
INSERT INTO CollegePerformances VALUES
  ('Duke', 2016, 25, 11),
  ('UNC', 2016, 33, 7);
INSERT INTO PlayerPerformances VALUES
  ('Brandon Ingram', 2016, '6.75', '190', '14');
INSERT INTO CollegeRoster VALUES
  ('Duke', 'Brandon Ingram', '2015', '2016');
