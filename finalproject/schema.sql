DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS recipe;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE recipe (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  dish_name TEXT NOT NULL,
  ingredients TEXT NOT NULL,
  categories TEXT NOT NULL,
  method TEXT NOT NULL,
  upvote INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE ingredient (
  id INTEGER PRIMARY AUTOINCREMENT,
  ingredient_name TEXT NOT NULL
)