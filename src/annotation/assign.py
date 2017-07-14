#!/usr/bin/env python3

info = [
    ("jp1", "1077", ["2006-06-05-12-second.txt", "2008-06-03-11-first.txt"]),
    ("jp2", "1080", ["2007-07-03-06-second.txt", "2007-06-17-06-second.txt"]),
    ("jp3", "936", ["2006-06-01-12-second.txt"]),
    ("jp4", "1099", ["2009-01-05-11-first.txt", "2013-10-28-03-first.txt", "2012-11-30-14-first.txt", "2012-02-03-20-first.txt"]),
    ("jp5", "1090", ["2007-12-17-04-first.txt", "2006-12-10-09-second.txt"]),
    ("va1", "1019", ["2005-07-25-11-first.txt", "2012-12-15-02-first.txt", "2005-02-08-02-second.txt", "2013-05-05-18-first.txt", "2013-05-07-02-first.txt", "2005-05-19-11-first.txt", "2012-06-02-18-first.txt"]),
    ("va2", "968", ["2008-04-27-06-first.txt"]),
    ("va3", "1053", ["2007-06-04-10-second.txt", "2010-08-29-20-first.txt"]),
    ("va4", "1055", ["2013-01-30-01-first.txt", "2013-02-24-02-first.txt", "2010-08-05-11-first.txt", "2006-02-24-10-first.txt"]),
    ("va5", "1098", ["2007-08-19-01-first.txt", "2012-05-20-16-first.txt", "2013-09-12-11-first.txt"]),
    ("jkk1", "984", ["2005-06-20-03-second.txt", "2009-03-25-11-first.txt", "2010-02-13-01-first.txt"]),
    ("jkk2", "933", ["2012-11-24-20-first.txt", "2012-05-04-04-first.txt", "2013-07-19-03-first.txt", "2013-05-19-22-first.txt", "2013-12-02-21-first.txt"]),
    ("jkk3", "1098", ["2008-04-30-08-first.txt", "2011-04-28-09-first.txt"]),
    ("jkk4", "1037", ["2006-08-23-03-first.txt", "2007-09-07-07-second.txt"]),
    ("jkk5", "984", ["2007-01-19-07-first.txt", "2008-04-20-09-first.txt"]),
    ("jkk6", "553", ["2011-08-17-08-first.txt", "2013-08-30-11-first.txt", "2013-07-10-23-first.txt", "2013-10-11-07-first.txt", "2013-01-11-13-first.txt", "2013-10-04-12-first.txt"]),
]

for name, count, filenames in info:
    out = open(name +"-list.txt", 'w')
    print("../../guide.txt", 'tmp-file', 0, 0, file=out)
    for filename in filenames:
        to_annotate = "../../raw/"+ filename
        to_save = filename +".annotated."+ name[:-1]
        print(to_annotate, to_save, 101, 0, file=out)
    out.close()
