drop table if exists accounts;
create table account (
  id integer primary key autoincrement,
  username text not null,
  'password' text not null
);