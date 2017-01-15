def extract_jpg_from_PDF(pdfName):
    '''Extracts the JPGs images in a PDF file by analising the binary structure of the PDF
        The beggining of a JPG is tagged by a b"\xff\xd8" and the end by a "\xff\xd9"
        We basically take the characters in between (quick and dirty)'''
        '''Credit to Ned Batchelder'''

    directoryName = pdfName + ' images'
    os.makedirs(directoryName) #Directory where jpgs will be extracted
    currentDirectory = os.getcwd() #Gets the current directory

    pdf = open(pdfName,'rb')
    pdf = pdf.read()
    path = os.path.join(currentDirectory,directoryName)
    os.chdir(path) #Change to the images folder

    startmark = b"\xff\xd8"
    startfix = 0
    endmark = b"\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:
        istream = pdf.find(b"stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream + 20)
        if istart < 0:
            i = istream + 20
            continue
        iend = pdf.find(b"endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend - 20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")

        istart += startfix
        iend += endfix
        print("JPG %d from %d to %d" % (njpg, istart, iend))
        jpg = pdf[istart:iend]
        with open("jpg%d.jpg" % njpg, "wb") as jpgfile:
            jpgfile.write(jpg)

        njpg += 1
        i = iend

    jgpfile.close()
    os.chdir(currentDirectory)
    pdf.close()
