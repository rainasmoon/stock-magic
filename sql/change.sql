alter table calender modify exchange varchar(20);
alter table calender modify cal_date char(8);
alter table calender add primary key(cal_date);

alter table stock_index modify date char(10);
alter table stock_index add primary key(date);
