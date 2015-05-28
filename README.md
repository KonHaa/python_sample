# python_sample

this little piece of code is written to be executed
as a cronjob or by incron.
with this combination you can monitor a logfile
and send an email that contains the new log entries.


start it with 2 args:
the first arg is the logfile you want to monitor
the second arg is the recipient who should recieve an email
that contains the new log entries

if the linecount between 2 runtimes differs it will
mail the new lines to the recipient.
