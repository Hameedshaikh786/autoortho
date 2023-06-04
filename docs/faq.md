# FAQ and Troubleshooting

## On Windows the executable/zip is detected as a malware/virus by Windows Defender
That is a false positive.  Unfortunately, Windows is very dev and opensource unfriendly.  You can choose to ignore this false positive or not, it's your computer.  Alternatively, you can run this directly via source.

## On Linux this does not start/gives a FUSE error
Make sure that your `/etc/fuse.conf` files is set to `user_allow_other`.  You may need to uncomment a line.

## I get an error like `Failed to find resource '../textures/22304_34976_BI16.dds', referenced from file 'Custom Scenery/z_eur_11/terrain/'.`

What's happening is that X-Plane has found a terrain file, but is not finding a linked texture.  This could be caused by a few issues:

  * AutoOrtho isn't running
  * You may have broken the links from your texture directories to the AutoOrtho mount location. Perhaps you manually moved around directories after downloading these from the configuration utility.
  * The directory AutoOrtho is configured to run from is now different from the directory links the scenery packs point to.

First verify that AutoOrtho is running and there are no obvious errors shown in a log.  If it is running then verify that all the directory links are correct, and consider simply cleaning up and reinstalling scenery from scratch, keeping a consistent 'Custom Scenery' directory configured.

If in doubt, re-install the scenery packs.

## Something went wrong with scenery setup and I'd like to start again.  How do I reinstall?
AutoOrtho checks for metadata for installed scenery packs in `Custom Scenery/z_autoorth/**_info.json`  Where '**' is a shortname for each scenery pack installed.  You can delete the corresponding .json file, and re-run the configuration utility and should be able to reinstall the scenery pack

## I installed scenery, setup Custom Scenery, and clicked 'Fly' but X-Plane did not automatically startup
You have to start X-Plane separately from this tool.  It's also best to start X-Plane _after_ starting autoortho so that all new files and directories are picked up.

## When using Windows I see an error using the run.bat file such as ` note: This error originates from a subprocess, and is likely not a problem with pip. error: legacy-install-failure`

This is likely due to having a very new version of Python and a package dependency that does not have a pre-built 'wheel' binary.  Further in that error you will see a link to visual studio build tools that can be installed.  You could also try downgrading your version of Python.  For instance try uninstalling Python 3.11 and install Python 3.10.
