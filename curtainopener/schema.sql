drop table if exists entries;
create table entries (
  id INTEGER primary key autoincrement,
  hours INTEGER not null,
  minutes INTEGER not null,
  date DATE not null,
  open BOOLEAN not null,
  done BOOLEAN DEFAULT 0
);

drop table if exists settings;
create table settings (
  id INTEGER primary key autoincrement,
  value INTEGER DEFAULT 1800
);