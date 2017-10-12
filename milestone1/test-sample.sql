-- sample query that will return to the web application players
-- that are similar to the player input by the user
SELECT name
  FROM Players, CollegeRoster
 WHERE Players.name = CollegeRoster.player
   AND CollegeRoster.college = 'Duke';
