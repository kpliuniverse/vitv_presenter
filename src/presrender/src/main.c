/*
Raylib example file.
This is an example main file for a simple raylib project.
Use this as a starting point or replace it with your code.

by Jeffery Myers is marked with CC0 1.0. To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/

*/

#include "raylib.h"


int main ()
{
	// Tell the window to use vsync and work on high DPI displays 
	SetConfigFlags(FLAG_VSYNC_HINT | FLAG_WINDOW_HIGHDPI);

	// Create the window and OpenGL context
	InitWindow(1, 1, "");
	SetWindowState(FLAG_WINDOW_HIDDEN);
	RenderTexture2D target = LoadRenderTexture(800, 450);

	// drawing
	BeginTextureMode(target);

	// Setup the back buffer for drawing (clear color and depth buffers)
	ClearBackground(WHITE);

	// draw some text using the default font
	DrawText("kaitentou kara nai gengo haitenshon to katai tenpo i sendou suru jaiken go kara daikenkai senhou!", 200,200,20,BLUE);

	EndTextureMode();
    // Now, capture the render texture as an image
    Image screenshot = LoadImageFromTexture(target.texture); // Get image from texture
	
	ImageFlipVertical(&screenshot);
 
    // Save the image to a file
    ExportImage(screenshot, "offscreen_screenshot.png");

    // Unload resources
    UnloadImage(screenshot);
    UnloadRenderTexture(target);
	
	// destroy the window and cleanup the OpenGL context
	CloseWindow();
	return 0;
}
