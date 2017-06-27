drop table if exists entries;
create table entries (
  id INTEGER primary key autoincrement,
  hours INTEGER not null,
  minutes INTEGER not null,
  'date' DATE not null
);