-- used the same schema as in schema.rb in starter code

drop table if exists applicants;
create table applicants (
  id integer primary key autoincrement,
  first_name varchar(30),
  last_name varchar(30),
  region varchar(50),
  phone varchar(10),
  email varchar(100),
  phone_type varchar(30),
  source varchar(20),
  over_21 boolean,
  reason text,
  workflow_state varchar(30),
  created_at timestamp not null,
  updated_at timestamp not null
);