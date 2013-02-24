create table wordlist (
	  id serial,
	  frequency integer not null,
	  word varchar(32) not null,
	  primary key (id)
);

create sequence stash_id_seq minvalue 10 start with 10;
create table stash (
	id integer not null default nextval('stash_id_seq'),
	created timestamp without time zone default now(),
	maxdays smallint not null default 10,
	maxviews smallint not null default 10,
	views smallint not null default 0,
	phrase varchar(2048) not null,
	primary key (id)
);
alter sequence stash_id_seq owned by stash.id;
