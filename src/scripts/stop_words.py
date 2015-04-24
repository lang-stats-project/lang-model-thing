#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
#from nltk.corpus import stopwords
#stop = stopwords.words('english')
#for word in sorted(stop): print word

stop_words = """
a
about
above
after
again
against
all
am
an
and
any
are
as
at
because
been
before
below
between
both
but
by
can
did
down
during
each
few
for
from
further
had
has
he
her
here
hers
herself
him
himself
his
how
i
if
in
into
is
it
its
itself
just
me
more
most
my
myself
no
nor
not
now
of
off
on
once
only
or
other
our
ours
ourselves
out
over
own
same
she
should
so
some
such
than
that
the
their
theirs
them
themselves
then
there
these
they
this
those
through
to
too
under
until
up
very
was
we
were
what
when
where
which
while
who
whom
why
will
with
you
your
yours
yourself
yourselves
one
two
three
four
five
six
seven
eight
nine
ten
eleven
twelve
twenty
thirty
forty
fifty
sixty
seventy
eighty
ninety
hundred
really
yes
get
well
new
old
must
every
all
none
"""
delimeters = ['</s>', '<s>']
stop_words = delimeters + stop_words.split()

bad_res = [
    r"\w*'\w*",
    r"(think|go|do|know|be|have|want)(ing|ed|s)?"
]

# this lowers the word
def is_stop(word):
    word = word.lower()
    if word in stop_words:
        return True
    for bad_re in bad_res:
        match = re.match(bad_re, word)
        if match:
            return True
    return False

def is_delimeter(word):
    return word in delimeters
