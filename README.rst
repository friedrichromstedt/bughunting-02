Hunting Down a Bug related to ImageTk in Python on Cygwin
#########################################################

:author: Friedrich Romstedt
:date: August 2021, last revised in October 2021

.. contents::


Summary
=======

`Pillow <https://github.com/python-pillow/Pillow>`_ is a library to work
with raster images in Python.
It provides a package `PIL.ImageTk
<https://pillow.readthedocs.io/en/stable/reference/ImageTk.html>`_, used to
create ``tkinter`` compatible image objects.  These objects can be used to
display ``PIL`` images in a tkinter GUI.
However, when attempting to use ``PIL.ImageTk`` with Cygwin in October 2021
(on Windows 10), one is presented with a traceback instead.
This article describes the observed behaviour and some attempts to remedy
the defect.
None of these attempts led to success.  They also did not reveal any hint
on where the reason of the dysfunction might originate from.
It is still not clear whether the error can be repoduced on other machines.
This repository provides a self-contained Python script intended to
reproduce the exception.  The repository is maintained separate from any
upstream tracker until the piece of software triggering the failure is
identified.


Description of the Bug and of the Expected Behaviour
====================================================

The bug turns up when trying to display a PIL/Pillow Image in a
``tkinter.Canvas`` using ``PIL.ImageTk`` in Cygwin:

.. code:: python

    # Developed since: August 2021

    import tkinter
    from PIL import Image, ImageTk


    image = Image.new('RGB', (100, 100))

    tk = tkinter.Tk()
    canvas = tkinter.Canvas(tk)
    canvas.pack()

    photoimage = ImageTk.PhotoImage(image)
    canvas.create_image((0, 0),
        image=photoimage,
        anchor='nw',
    )

    tk.mainloop()

The expected result on-screen is (produced with Windows Python 3.8):

.. figure:: Expected.png

    The expected on-screen result of running the reproduction script.


When running the script with Cygwin-Python 3.8 however the following
traceback is produced instead:

.. code:: python

    Traceback (most recent call last):
      File "/usr/lib/python3.8/site-packages/PIL/ImageTk.py", line 176, in paste
        tk.call("PyImagingPhoto", self.__photo, block.id)
    _tkinter.TclError: invalid command name "PyImagingPhoto"

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "reproduce.py", line 13, in <module>
        photoimage = ImageTk.PhotoImage(image)
      File "/usr/lib/python3.8/site-packages/PIL/ImageTk.py", line 115, in __init__
        self.paste(image)
      File "/usr/lib/python3.8/site-packages/PIL/ImageTk.py", line 180, in paste
        from . import _imagingtk
    RuntimeError: No such process


Versions Involved
=================

The current versions in the Cygwin package manager are:

    ``Pillow-8.1.2``: ``python38-imaging-8.1.2-1`` +
    ``python38-imaging-tk-8.1.2-1``.

Also available via the Cygwin package manager:

    ``Pillow-7.2.0``: ``python38-imaging-7.2.0-1`` +
    ``python38-imaging-tk-7.2.0-1``.

To be able to compile Pillow in other versions, the following ``-devel``
libraries have been made available (based on recommendations given in
https://github.com/python-pillow/Pillow/issues/2860):

#.  ``gcc-core-10.2.0-1``;
#.  ``libjpeg-devel-2.1.0-1``;
#.  ``zlib-devel-1.2.11-1``;
#.  ``libtiff-devel-4.3.0-1``;
#.  ``libfreetype-devel-2.10.4-2``;
#.  ``libfribidi-devel-0.19.7-1``;
#.  ``libharfbuzz-devel-2.8.1-1``;
#.  ``libimagequant-devel-2.10.0-1``;
#.  ``libpng-devel-1.6.37.1``;
#.  ``liraqm-devel-0.7.0-1``;
#.  ``python38-devel-3.8.10-1``.

Furthermore I installed:

#.  ``tcl-devel-8.6.11-1``;
#.  ``tcl-tk-devel-8.6.11-1``.

in support of ``tcl-8.6.11-1`` and ``tcl-tk-8.6.11-1``.

Other versions of ``Pillow`` which have been tried instead of the ``8.1.2``
version are:

*   ``Pillow-8.3.1`` (installed from source);
*   ``Pillow-7.2.0`` (installed per Cygwin as ``python38-imaging-7.2.0-1``
    + ``python38-imaging-tk-7.2.0-1``);
*   ``Pillow-6.2.2`` (installed from source);
*   ``Pillow-5.4.1`` (installed from source).

Other versions of Tcl/Tk which have been given a try are:

*   ``tcl``, ``tcl-devel``, ``tcl-tk`` and ``tcl-tk-devel``, all in version
    ``8.6.8-1`` (via the Cygwin package manager).


Attempts to Remedy the Defect
=============================

Upgrading/Downgrading Pillow
----------------------------

All this has been worked through in a virtualenv created by::

    $ python -m virtualenv --system-site-packages <dir>

The abovementioned reproduction script fails outside of this virtualenv as
well.

In the beginning, I assumed that Cygwin doesn't provide Pillow as a
package, before I realised that it is contained under the name
``pythonXY-imaging`` and ``pythonXY-imaging-tk``, while only
``python38-imaging`` was installed.

After after having installed the supporting ``-devel`` packages for
``libjpeg``, ``zlib``, ``libtiff``, ``libfreetype``, ``libfribidi``,
``libharfbuzz``, ``libimagequant``, ``libpng``, ``libraqm``, ``tcl``,
``tcl-tk`` and ``python38``, I installed Pillow inside of the virtualenv
using::

    $ pip install --upgrade Pillow

This installed Pillow v8.3.1.  From this point on, it was possible to
import ``ImageTk``::

    >>> form PIL import Image
    >>> Image.__version__
    '8.3.1'
    >>> from PIL import ImageTk
    (ok)

However attempting to actually *use* ``ImageTk`` failed with the
abovementioned traceback.

At this point, I realised that there are Cygwin packages called
``python38-imaging`` and ``python38-imaging-tk``, so I uninstalled Pillow
in the virtualenv::

    $ pip uninstall Pillow

and installed ``python38-imaging-tk`` via the Cygwin package installer.
This incured no more dependencies, however the traceback remained present.

The Cygwin package manager offers aside of ``python38-{imaging,
imaging-tk}-8.1.2-1`` also ``7.2.0-1`` version of these packages.  I tried
these, to no avail.

Next, I tried the latest version of the 6.x series of Pillow
(https://pillow.readthedocs.io/en/stable/releasenotes/index.html)::

    $ pip install Pillow==6.2.2
    > (ok)

where the traceback persists.  Furthermore I tried Pillow-5.4.1 (the latest
5.x version)::

    $ pip install Pillow==5.4.1
    > matplotlib 3.3.3 requires pillow>=6.2.0, but you have pillow 5.4.1 which is incompatible.
    > (otherwise ok)

which was still dysfunctional.

At this moment, I suspected that the reason of the error observed might be
outside of Pillow, so I uninstalled the custom-made Pillow from the
virtualenv::

    $ pip uninstall Pillow

and upgraded the Cygwin-installed Pillow version back to ``8.1.2-1``,
intending to change tcl/tk library versions.

The Cygwin package manager offers ``tcl``, ``tcl-devel``, ``tck-tk`` and
``tcl-tk-devel`` in versions ``8.6.11-1`` and ``8.6.8-1``.  I hence
downgraded from ``8.6.11-1`` to ``8.6.8-1``, however once more to no avail.

Having reached the end of my wits at this point, I found myself writing up
this summary document to turn towards upstream.


**--- 21 October 2021 ---**

Upgrading ``freetype2`` and ``harfbuzz``
----------------------------------------

*Note*:

    From here on, logs are written in the ``/Logs/`` directory of the
    repo this files resides in.  They are referenced before the command
    which is logged, e.g.::

        [b01] $ pip install --upgrade Pillow

    is logged in the file within ``/Logs/`` starting with ``b01``.

Upgraded ``libfreetype2`` and ``libfreetype-devel`` from ``2.11.0-1`` to
``2.11.0-2`` (released 19 October 2021).

Upgraded also ``girepository-Harfbuzz0.0``, ``libharfbuzz-devel``,
``libharfbuzz-gobject0`` and ``libharfbuzz0`` from ``2.9.0-1`` to
``2.9.0-2`` (released 19 October 2021 as well).

All this has been to no avail.


Downgrading ``freetype2`` and ``harfbuzz``
------------------------------------------

The Cygwin installer permits downgrading the ``freetype2`` packages to
``2.10.4-2`` and the ``harfbuzz`` packages to ``2.8.1-1``.

This did not help either, the problem persisted in its familiar form.

Reverted the downgrades.


Building ``Pillow`` *without* ``freetype2`` and ``harfbuzz``
------------------------------------------------------------

Removed ``libfreetype-devel``, ``libharfbuzz-devel`` and ``libraqm-devel``
(``libraqm`` *requires* ``libfreetype-devel``).

Derived a virtualenv per::

    $ python -m virtualenv --system-site-packages --no-periodic-update 2021-10-21_0918

Built in this virtualenv ``Pillow`` per::

    [b01] $ pip install --upgrade Pillow
    > (Pillow 8.1.2 in /usr/lib/python3.8/site-packages/ remains untouched)
    > (otherwise ok)

Verified that in this virtualenv the new ``Pillow-8.4.0`` is used::

    $ python
    >>> import PIL
    >>> PIL.__version__
    '8.4.0'
    (ok)

Ran via this virtualenv the file ``/reproduce.py``::

    [b02] $ python reproduce.py
    (same error as before)

Restarted the machine, activated the virtualenv and ran the script again:
The error has been reproduced.

Reinstalled ``libfreetype-devel-2.11.0-2``, ``libharfbuzz-devel-2.9.0-2``
and ``libraqm-devel-0.7.0-1``.


**--- 26 October 2021 ---**

Diagnosing the Problem with Pillow Upstream
===========================================

Issue #5974 on the Pillow github.com Repository
-----------------------------------------------

I filed an Issue with `Pillow <https://github.com/python-pillow/Pillow>`_
to gather additional information (`#5974
<https://github.com/python-pillow/Pillow/issues/5795>`_).

Diagnostic output as requested in a `Comment by DWesl on 25 October 16:43
<https://github.com/python-pillow/Pillow/issues/5795#issuecomment-951001258>`_:

*   The output of ``cygcheck -svr`` is provided in file
    `[c01] <Logs/c01%20cygcheck%20-svr.txt>`_.

*   Running ``python [-v[v]] -c 'import PIL._imagingtk'`` produces the
    following output:

    1.  ``python -c 'import PIL._imagingtk'``: `[d01]
        <Logs/d01%20python%20-c%20import%20PIL._imagingtk.txt>`_

    2.  ``python -v -c 'import PIL._imagingtk'``: `[d02]
        <Logs/d02%20python%20-v%20-c%20import%20PIL._imagingtk.txt>`_

    3.  ``python -vv -c 'import PIL._imagingtk'``: `[d03]
        <Logs/d03%20python%20-vv%20-c%20import%20PIL._imagingtk.txt>`_

*   Checking the extension DLLs:

    1.  Running ``cygcheck``:

        a.  ``_imagingtk.cpython-38-x86_64-cygwin.dll``: `[e01]
            <Logs/e01%20cygcheck%20.__imagingtk.cpython-38-x86_64-cygwin.dll.txt>`_

        b.  All ``.dll`` files: `[e02] <Logs/e02%20cygcheck%20.__.dll.txt>`_

    2.  Checking executability: `[e03] <Logs/e03%20ls%20-l%20_.dll.txt>`_

    3.  Running ``ldd``:

        a.  ``_imagingtk.cpython-38-x86_64-cygwin.dll``: `[e04]
            <Logs/e04%20ldd%20_imagingtk.cpython-38-x86_64-cygwin.dll.txt>`_

        b.  All ``.dll`` files: `[e05] <Logs/e05%20ldd%20_.dll.txt>`_
