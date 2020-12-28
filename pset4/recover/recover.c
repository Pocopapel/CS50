#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // make sure the user opens the file correctly
    if (argc != 2)
    {
        printf("correct usage ./recover filename\n");
        return 1;
    }
    // open the card and if it cant be opened give an error message
    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        printf("can´t open argv[1]\n");
        return 1;
    }
    // file becomes stored as string cardname
    char *cardname = "argv[1]";
    //free space for buffer
    unsigned char *buffer = malloc(512);
    //counter of the amount of pictures
    int picturenr = 0;
    // free space for the name of the picturefile
    char *photoname = malloc(8);
    // declare the img file
    FILE *img = NULL;
    // bool to check if its a new jpeg
    bool foundjpeg = false;

    // keep reading the buffer in chunks of 512 bytes until it cant anymore
    while (fread(buffer, 512, 1, f) == 1)
    {
        // check start of jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // already a jpeg has been opened, close old one
            if (picturenr != 0)
            {
                fclose(img);
            }
            // it found a jpeg, now open it and increase counter
            foundjpeg = true;
            sprintf(photoname, "%03i.jpg", picturenr);
            img = fopen(photoname, "w");
            picturenr++;
        }
        // start writing once the jpeg is found
        if (foundjpeg == true)
        {
            fwrite(buffer, 512, 1, img);
        }
    }
    // close files and free memory and close the program
    free(buffer);
    free(photoname);
    fclose(img);
    fclose(f);
    return 0;
}