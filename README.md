# Corpus Text Processor

## Contents

- [Getting started](#getting-started)
- [Installation](#installation)
- [Preparing files to be processed](#preparing-files-to-be-processed)
- [Processing a folder of files](#processing-a-folder-of-files)
- [Reviewing the results](#reviewing-the-results)
- [Advantages of our Corpus Text Processor](#advantages-of-our-corpus-text-processor)
- [Known limitations](#known-limitations)
- [Video presentation](#video-presentation)

## Getting started

The Corpus Text Processor (**[download here](https://github.com/writecrow/corpus_text_processor/releases)**) for Windows or Mac is a downloadable application for Windows and Mac that provides batched (multiple-files-at-a-time) operations for common corpus processing tasks. The screenshot of the application below shows the four tasks currently available:

<kbd>![Screenshot of application UI](https://user-images.githubusercontent.com/4305692/75635296-83c5d500-5bda-11ea-9253-13d789613dda.png)</kbd>

After running operations on a set of files, Corpus Text Processor provides debugging output that indicates how many files were processed and which files, if any, had issues.

## Installation
Download the latest version of the Corpus Text Processor for Windows or MacOS at https://github.com/writecrow/corpus_text_processor/releases

### Trouble installing?

If you get error messages related to application security upon installation, please review one of these pages based on your operating system:

- See [Windows Installation](https://github.com/writecrow/corpus_text_processor/wiki/Windows-Installation)
- See [Mac Installation](https://github.com/writecrow/corpus_text_processor/wiki/Mac-Installation)

## Preparing files to be processed
Before running the tool, place all files to be processed in a specific folder; this can include sub-directories. It is recommended that you then create a new top-level folder to save your processed files to. You can create that folder at the same level of the top-level parent directory for the files you wish to process. You don’t need to recreate the sub-directory structure because the corpus processing tool will do this for you.

You may have files in a variety of formats in the "Original" folder, such as .doc, .pdf, etc. These files, however, need to be named differently. If multiple files in different formats have the same name, they will be written over each other after being converted to .txt format. In this case, you will get only one .txt file in the "Converted" folder.

## Processing a folder of files
To run the tool, choose the folder that you want to process (below, “Original”) and your output folder to save the processed data to (below, “Converted”). You can only process a folder, not individual files. If you have multiple sub-directories to convert, just choose the parent directory. The corpus processing tool will process all the sub-directories and recreate the directory structure in the output folder. DO NOT select the same folder to read and write the files.

We recommend running the processes in the order sequentially (Convert to plaintext, Encode to UTF-8 encoding, Standardize non-ASCII characters and remove non-English characters, Remove PDF metadata). In fact, it should be noted that the "Standardize non-ASCII characters and remove non-English characters" process is designed only to work with files already in UTF-8 format. The only exception to this is that you do not generally need to run the “Remove PDF metadata” process. We use this for de-identifying files that will go into the repository as PDFs as well as plain text.


## Reviewing the results
Once the files have been processed (after each processing step), inspect documents to ensure proper conversion:
1. Check for errors in the program’s debug window.

2. Determine whether you have the same number of input and output files:

   a. If you open a folder in Windows File Explorer you can see the number of files in the bottom left corner.

<kbd><img src="https://github.com/writecrow/ciabatta/blob/master/Win%20text%20number.JPG" height="367" width="148" alt="Screenshot of Windows text number" /></kbd>

   b. For Macs, right click and choose “Get Info” to get the number of files.

<kbd><img src="https://github.com/writecrow/ciabatta/blob/master/Mac%20text%20number.JPG" height="333" width="219" alt="Screenshot of Mac text number" /></kbd>

3. Check if there are any files that haven’t been processed correctly. Look for files of size 0 bytes or 1 byte. Change your view to list view in order to see the file sizes of all the files in a folder.

4. For any files that have failed to process, troubleshoot a couple of items:

    1. **Is it read only?** If so, try opening and saving the input file in Word before running the program again.
    1. **Is the file name too long?** Try renaming the file, retaining important information in the filename (e.g., name or group number).
    1. **Are there special characters in the file name?** If a file doesn’t convert, check for special characters in the file name: colons and other symbols, other language characters, etc. Remove these from the file name and try again.

## Advantages of our Corpus Text Processor

* All three steps are in one package. Other programs are available that do one of these steps but the Corpus Text Processor allows you to do all three steps with one program.
* Like some (but not all) other programs, the Corpus Text Processor attempts to alleviate some of the problems with converting PDFs by first converting the PDFs to Word.
* We have also added logic to remove extra line breaks in cases where we are able to reliably remove them.
* The corpus text processor recreates the folder structure (and copies into a new location).
* Our team is actively using our tool, meaning that we are updating it as we encounter issues with our own corpus building.

## Known limitations
- Text-as-image PDFs are not currently supported for conversion to plaintext. We are in alpha development for a script that uses the Textract OCR library for converting text-as-image PDFs. You are free to use that project, as-is, at https://github.com/writecrow/ocr2text
- The tool can detect and convert all of the encoding types listed on the [Chardet library page](https://pypi.org/project/chardet/). The tool will make a best-effort attempt to convert other encoding types  but is not guaranteed to work.
- Text files that consist primarily of non-Romanized characters may interfere with the tool's ability to identify the encoding type and may not convert.
- Converting files of type `.doc` to plaintext is not currently supported. We recommend using a batch utility to convert `.doc` files to `.docx` format, which this application can convert. Here are recommended utilities for converting `.doc` files:
  * **MacOS**: the built-in `textutil` utility can do this. See the tutorial at https://www.chriswrites.com/convert-txt-rtf-doc-and-docx-files-with-textutil/
  * **Windows**: Zilla word-to-text is a free application. Download at https://download.cnet.com/Zilla-Word-To-Text-Converter/3000-2079_4-75118863.html
- Currently the program only works with English. We have plans for developing a tool that will work with Portuguese and Russian in the future.

## Video presentation

A video version of this content is available on our [YouTube channel.](https://www.youtube.com/channel/UCVcF4DkKDDT22AN65BJj3ng)

[![](https://img.youtube.com/vi/i4ecoRX8URk/mqdefault.jpg)](https://www.youtube.com/watch?v=i4ecoRX8URk)

[Video: Corpus Text Processor Demonstration](https://www.youtube.com/watch?v=i4ecoRX8URk)

