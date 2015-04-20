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
be
because
been
before
being
below
between
both
but
by
can
did
do
does
doing
don
down
during
each
few
for
from
further
had
has
have
having
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
s
same
she
should
so
some
such
t
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
</s>
<s>
"""
stop_words = stop_words.split()

bad_res = [] # TODO: insert bad words REs here. r"bad_words_re"

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
