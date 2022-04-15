
bcp <TABLENAME> in <TABSEPFILEPATH> -S <SERVERNAME> -d <DATABASENAME> -U <USERNAME> -P <PASSWORD> -c -t \t
bcp Test in "C:\Users\riced\Desktop\Powers\Customer Database\Testing\TankDataSample.txt" -S "testing-server.database.windows.net" -d "NoLedger" -U "powersadmin" -P "cr@yonstastel1kemelon" -c -t \t

insert into <TABLENAME> values('<x>', '<y>', TO_DATE('9999-99-99','YYYY-MM-DD'));