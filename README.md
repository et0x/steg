# steg
Embed data / files in PNG images using LSB steganography

## Synopsis:

This tool simply puts data/files in or pulls steganographically embedded data/files out of PNG images

## Usage:

Usage: steg.py [options]

Options:
  -h, --help              Shows help message and exit
  -f <fileToEmbed>        Embeds a file into an image
  -t <textToEmbed>        Embeds raw text into an image
  -r <ImageToEmbedInto>   The template PNG image you wish to steg your data into
  -w <NewImageName>       The new image with embedded data in it
  -d                      Turn debugging on.  This will show the pixels you have written after the command completes.
  -g                      This will pull data out of an image already steg'd with this tool.
  
Examples:

  et0x@mnstr:~$ python steg.py -f /bin/bash -r layout.png -w new.png
  [*] Calculating maximum buffer for data in given image template...
  [*] Image size sufficient for input data, moving forward...
  [*]  Dataspace (needed/max): 27160 / 75888 bytes
  [+] Successfully wrote 'new.png' ...
  
  et0x@mnstr:~$ python steg.py -g new.png > newnc
  et0x@mnstr:~$ file newnc
  newnc: ELF 64 bit LSB executable, x86-64, version 1 .....
  
  et0x@mnstr:~$ chmod 755 newnc
  et0x@mnstr:~$ ./newnc -lvp 444
  listening on [any] 444 ...
  
  --------------------------------------------------------------------
  
  et0x@mnstr:~$ python steg.py -f /etc/passwd -r layout.png -w passwd.png
  [*] Calculating maximum buffer for data in given image template...
  [*] Image size sufficient for input data, moving forward...
  [*]  Dataspace (needed/max): 2131 / 75888 bytes
  [+] Successfully wrote 'passwd.png' ...
  
  et0x@mnstr:~$ python steg.py -g passwd.png
  root:x:0:0:/root:/bin/bash
  daemon:x:1:1:daemon:/usr/sbin:/bin/sh
  ...

  ----------------------------------------------------------------------
## Motivation:

Steg all the things!
