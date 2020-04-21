Import VBB GTFS dataset
=======================

What
  The target of this script is to import into CrateDB_ the `VBB GTFS dataset`_.
  It was made with Python3.7. It is required to install crate for python.

How
  **Set the paths to the GTFS files**
  Once the data is donwloaded, it needs to be unziped into the same folder as the
  main python files.
  Otherwise, routes must be set in lines 64 to 73 on main.py.
  After routes are set, you can run the script on (windows) in the command
  prompt by executing:
    :\> python main.py

Dependencies
  First you need to create a node of CrateDB or connect to an existing one.
  To do so, follow the installation instructions on the link_.
  Second, you need to install the python client. For further instructions please,
  follow the link_.

Debugging
  Make sure that crate package is included in you dependencies. Also make sure
  that a connection through Crate client is established. For more information
  regarding this issue, follow this link_.

:Author:
  Miguel Alvarez Bordils





.._`VB BGTFS dataset`: https://daten.berlin.de/datensaetze/vbb-fahrplandaten-gtfs
_CrateDB: https://crate.io/
_link: https://crate.io/docs/
