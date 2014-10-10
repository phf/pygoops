=======================================
Frame-based versus Time-based Animation
=======================================

:Author: Peter H. Froehlich <phf@acm.org>
:Organization: Johns Hopkins Gaming Lab <http://gaming.jhu.edu/>

Almost all games feature animated objects of some kind: meteors,
space ships, Mario, dinosaurs, what have you. Usually we'd like
the animations to play at some constant speed, constant no matter
how powerful (or busy) the machine they run on is (at the moment).

---------------------
Frame-based Animation
---------------------

The simplest kind of animation works like this: clear the screen,
draw the objects, update the objects, repeat until done. Smooth
animation requires that we synchronize drawing and video refresh
somehow, something PyGame does for us with pygame.display.flip().

The problem with this sort of animation is that objects move at a
constant speed *per* *frame* and if we have too many objects for
the machine to update before the frame is over, their speed won't
be constant anymore. This is called frame-based animation: simple
but (often) wrong.

--------------------
Time-based Animation
--------------------

We can do better by keeping track of how long it takes to perform
all the drawing for our objects, and then moving them at a speed
*per* *second* which will stay constant *regardless* of frames per
second. This is called time-based animation: slightly harder to
do, but (mostly) correct.

Of course there are some problems too, most notably that game-play
will "skip" if there is a large enough delay while drawing, a
problem that can even lead to collisions not working out as they
should. However, frame-based animation is the bigger problem, at
least with time-based animation your game remains consistent under
"normal" circumstances.

-----------------------------------
Fixed-interval Time-based Animation
-----------------------------------

Of course we don't really want to live with the chance of a missed
collision. The big problem with simple time-based animation is that
drawing time still influences how updates are performed.

What we need to do is separate the game logic from drawing on the
screen. One way to do this is to update the game logic in fixed
intervals, say 50 milliseconds. As long as we have no objects of
truly bizzare speed or amazingly small size, we should be able to
detect all necessary collisions that way.

Of course we still need to draw to the screen, and that will still
take time. So just as in the simple time-based animation approach,
we keep track of the elapsed time, but then divide that time into
a (variable) number of 50 millisecond update steps. We update our
objects in fixed intervals yet we still draw on the screen as fast
as we can.

-----------------------------------------------------------
Minimum-interval and Leftover-interval Time-based Animation
-----------------------------------------------------------

One remaining problem is that 50 milliseconds may be *too* *long* on
a fast machine: Imagine that it takes only 10 milliseconds to draw
everything, then we'll never update the game objects! What we need
to do is somehow account for "partial" intervals.

A first technique would be to use the minimum of the actual drawing
time and our fixed interval. In the above example, we would update
our objects for 10 milliseconds worth of time. If drawing took 120
milliseconds, we'd perform 3 updates: 2 for 50 milliseconds each,
1 for 20 milliseconds of "leftover" time.

Another technique is to keep track of "leftover" time from frame
to frame instead. In the case of 10 milliseconds frame time, we
would draw the same frame 4 more times before updating the game
objects for another 50 milliseconds worth.

The first technique has the advantage of performing all updates
before the next frame is drawn, so we never draw two identical
frames in a row, something that seems like a big waste.

But the second technique has the advantage of *always* using the
same interval for updates. This can be useful if the game state
has to be reproducible across different machines, for example in
a networked multi-player game.

-----------
Python Code
-----------

There are five demo programs to illustrate the ideas above with
actual Python code:

  ====================   ============================
  Program                Arguments
  ====================   ============================
  frame-based.py         #objects
  time-based.py          #objects target-fps
  fixed-interval.py      #objects target-fps interval
  minimum-interval.py    #objects target-fps interval
  leftover-interval.py   #objects target-fps interval
  ====================   ============================

All of these use some common code in util.py, most importantly
the Circle class found there.

If you want to compare the different approaches closely, first
run frame-based.py with, say, 50 objects and note the FPS your
machine gets. Then run time-based.py with the same number of
objects and the FPS you got before as its target-fps argument.
First you should see that the animation comes out at about the
same effective speed. Second you should note the time required
for one frame. Now run the remaining three with the same number
of objects and the same target-fps, and pick an interval about
half the length of the time required from time-based.py before.
All three should come out with about the same effective speed
again. Both fixed-interval.py and leftover-interval.py should
mostly run two updates per frame while minimum-interval.py is
bound to run mostly three if you followed our advice about the
interval size to pick.

Now increase the number of objects to about 200 and re-run the
programs. You should see that frame-based.py now displays the
animation much more slowly, whereas the other four techniques
maintain the original speed. Of course the animation becomes
more choppy in the process since we can no longer push as many
frames per second to the screen.

Now increase the number of objects further, too some really high
number, 5000 say (depends on your system though, you may have to
try a few times). Eventually time-based.py will start to "lose"
objects because the initial time-step was so big that some flew
off the screen right past the collision code. If you try any of
the interval-based programs (with a large enough interval!) you
will see that they still process all the collisions correctly.
(See "Time required for updates" below if you pick an interval
that's too small.)

Now go back to 50 circles and run the interval-based programs
with an interval that's larger than the time you measured from
time-based.py earlier, say about twice that number. You should
notice that fixed-interval.py has (almost) no animation anymore
because we (almost) never require enough time to draw. In the
case of minimum-interval.py you should still get a rather smooth
animation because this program will keep updating the objects
with the time it actually took to draw them if the interval you
picked was too large. For leftover-interval.py you should get
a choppier animation; the effective speed should still be as we
want it, but since we now "skip" every other frame of rendering
we end up with a choppy presentation.

-------------------------
Time required for updates
-------------------------

There is, of course, one last issue to keep in mind. As soon as
we use time-based animation, it is *imperative* that we compute
our updates in *less* time than we're trying to simulate. If we
have, for example, 50 milliseconds worth of updating to do, we
*better* do it in at *most* 50 milliseconds, ideally even more
quickly than that. Otherwise each trip around the loop requires
longer and longer updates, ad infinitum. :-/

You can see this effect clearly in the interval-based examples,
just use a lot of objects and a small interval. From frame to
frame, you'll see the number of updates performed go up, with
no limit in sight.

---------------
Further Reading
---------------

- http://sacredsoftware.net/tutorials/Animation/TimeBasedAnimation.xhtml
- http://gafferongames.com/game-physics/fix-your-timestep/
- http://goingamerica.blogspot.com/2009/02/pygame-decoupling-rendering-from-game.html

-------
The End
-------
