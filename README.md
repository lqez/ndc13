ndc13
=====


** This is not a official site or page of NDC **

A fan page for 'Nexon Developer Conference of 2013'. 


Behind Story of this project
----------------------------

http://lqez.github.io/blog/making-a-fan-page-for-a-developer-conference.html


Built on 
--------

 - [Django](https://www.djangoproject.com/)
 - [Haystack](http://haystacksearch.org/)
 - [jQuery](http://jquery.com/)
 - [Bootstrap](http://twitter.github.io/bootstrap/)
 - [Flat UI](http://designmodo.github.io/Flat-UI/)
 - [Flying Bootstrap](https://github.com/lqez/flying-bootstrap/)
    

INSTALL
-------

    $ git clone https://github.com/lqez/ndc13.git
    $ cd ndc13
    $ mkvirtualenv ndc13
    ( ... or use your own virtual environment )
    $ pip install -r requirements.txt
    $ python manage.py syncdb
    $ python manage.py runserver 


All done.


TODO
----

 - Reservation.
 - Room capacity limit.
 - Pagination of comments.
 - About / Contact page.


DEMO
----

![Front](https://raw.github.com/lqez/ndc13/master/demo/ndc13_front.jpg)
![Timetable](https://raw.github.com/lqez/ndc13/master/demo/ndc13_timetable.jpg)
![Session list](https://raw.github.com/lqez/ndc13/master/demo/ndc13_sessions.jpg)
![Session detail](https://raw.github.com/lqez/ndc13/master/demo/ndc13_session.jpg)
![Speaker list](https://raw.github.com/lqez/ndc13/master/demo/ndc13_speakers.jpg)
![Speaker detail](https://raw.github.com/lqez/ndc13/master/demo/ndc13_speaker.jpg)
![Company list](https://raw.github.com/lqez/ndc13/master/demo/ndc13_companies.jpg)
![Company detail](https://raw.github.com/lqez/ndc13/master/demo/ndc13_company.jpg)

Support phone screens
---------------------
![Menu in phone](https://raw.github.com/lqez/ndc13/master/demo/ndc13_phone.jpg)
![Timetable in phone](https://raw.github.com/lqez/ndc13/master/demo/ndc13_phone_timetable.jpg)
![Filter in phone](https://raw.github.com/lqez/ndc13/master/demo/ndc13_phone_filter.jpg)


LICENSE
-------
 - Source codes are distributed under MIT license.
 - Some images and fixtures are under NEXON KOREA company.


AUTHOR
------
Park Hyunwoo / [@lqez](https://twitter.com/lqez)
