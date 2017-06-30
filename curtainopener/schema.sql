drop table if exists entries;
create table entries (
  id INTEGER primary key autoincrement,
  hours INTEGER not null,
  minutes INTEGER not null,
  date DATE not null,
  open BOOLEAN not null,
  done BOOLEAN DEFAULT 0
);