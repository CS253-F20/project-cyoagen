drop table if exists accounts;
create table accounts (
  id integer primary key autoincrement,
  username text not null,
  'password' text not null
);
drop table if exists choices;
create table choices (
  id integer primary key autoincrement,
  username text not null,
  'title' text not null,
  'situation' text not null,
  'option1' text not null,
  'option2' text not null,
  'linked_situation1' integer,
  'linked_situation2' integer,
  'game_id' integer not null
);
drop table if exists games;
create table games (
  id integer primary key autoincrement,
  username text not null,
  'title' text not null,
  'description' text not null
);