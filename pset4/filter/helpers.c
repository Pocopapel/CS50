#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float red = image[i][j].rgbtRed;
            float blue = image[i][j].rgbtBlue;
            float green = image[i][j].rgbtGreen;
            // get the average //
            average = (red + blue + green) / 3;
            int grey = round(average);
            // fill in the average as new grey value //
            image[i][j].rgbtRed = grey;
            image[i][j].rgbtGreen = grey;
            image[i][j].rgbtBlue = grey;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // create copy of the color
            float red = image[i][j].rgbtRed;
            float blue = image[i][j].rgbtBlue;
            float green = image[i][j].rgbtGreen;
            // create new sepia value
            float r = (.393 * red + .769 * green + .189 * blue);
            float g = (.349 * red + .686 * green + .168 * blue);
            float b = (.272 * red + .534 * green + .131 * blue);

            // make sure rgb isnt above 255 //
            if (r > 255)
            {
                r = 255;
            }
            if (g > 255)
            {
                g = 255;
            }
            if (b > 255)
            {
                b = 255;
            }
            image[i][j].rgbtRed = round(r);
            image[i][j].rgbtGreen = round(g);
            image[i][j].rgbtBlue = round(b);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int tempR [height][width];
    int tempG [height][width];
    int tempB [height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // create copy
            tempR[i][j] = image[i][j].rgbtRed;
            tempG[i][j] = image[i][j].rgbtGreen;
            tempB[i][j] = image[i][j].rgbtBlue;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // replace color values with value of the opposing pixel
            image[i][j].rgbtRed = tempR[i][width - 1 - j];
            image[i][j].rgbtGreen = tempG[i][width - 1 - j];
            image[i][j].rgbtBlue = tempB[i][width - 1 - j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // create copy of the image //
    RGBTRIPLE copyimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copyimage[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // set startvalue & reset of the sums and pixel counts
            float sumred = 0;
            float sumgreen = 0;
            float sumblue = 0;
            int pixels = 0;
            // create the 3x3 loop around the pixel for getting the sum
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // make sure the "out of bounds" values dont get taken in account
                    if ((i + k >= 0) && (j + l >= 0) && (i + k <= height - 1) && (j + l <= width - 1))
                    {
                        sumred = copyimage[i + k][j + l].rgbtRed + sumred;
                        sumgreen = copyimage[i + k][j + l].rgbtGreen + sumgreen;
                        sumblue = copyimage[i + k][j + l].rgbtBlue + sumblue;
                        pixels++;
                    }
                }
            }
            // replace image by average of 3x3 loop around it
            image[i][j].rgbtRed = round(sumred / pixels);
            image[i][j].rgbtBlue = round(sumblue / pixels);
            image[i][j].rgbtGreen = round(sumgreen / pixels);
        }
    }
    return;
}
