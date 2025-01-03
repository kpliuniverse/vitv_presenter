/*
Raylib example file.
This is an example main file for a simple raylib project.
Use this as a starting point or replace it with your code.

by Jeffery Myers is marked with CC0 1.0. To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/

*/

#include <stdio.h>

#include "window.hpp"
#include "readxml.hpp"
#include "presdata.hpp"

#include "3rdparty/tinyxml2/tinyxml2.hpp"

extern "C" {

	#include <errno.h>

    #include "raylib.h"


    #define CLAY_IMPLEMENTATION
    #include "3rdparty/clay/clay.h"

}

int main () {
	readxml::MotherResult presDataMotherResult = readxml::parse_xml();
	presdata::PresDataMother presDataMother;
	if (readxml::isSuccessful(presDataMotherResult)) {
		presDataMother = presDataMotherResult.value;

	}
	else {
		printf("Error parsing xml:%s\n", presDataMotherResult.errStr);
		return 1;
	}
	// Tell the window to use vsync and work on high DPI displays 
	SetConfigFlags(FLAG_VSYNC_HINT | FLAG_WINDOW_HIGHDPI);

	// Create the window and OpenGL context
	InitWindow(WINDOW_URUSAI, WINDOW_URUSAI, "");
	SetWindowState(FLAG_WINDOW_HIDDEN);
	RenderTexture2D target = LoadRenderTexture(presDataMother.width, presDataMother.height);

	// drawing
	BeginTextureMode(target);

	// Setup the back buffer for drawing (clear color and depth buffers)
	ClearBackground(WHITE);

	// draw some text using the default font
	DrawText("kaitentou kara nai gengo \nhaitenshon to katai tenpo \ni sendou suru jaiken go \nkara daikenkai senhou!", 200,200,20,BLUE);

	EndTextureMode();
    // Now, capture the render texture as an image
    Image screenshot = LoadImageFromTexture(target.texture); // Get image from texture
	
	ImageFlipVertical(&screenshot);
 
    // Save the image to a file
    ExportImage(screenshot, "labrats/out/offscreen_screenshot.png");

    // Unload resources
    UnloadImage(screenshot);
    UnloadRenderTexture(target);
	
	// destroy the window and cleanup the OpenGL context
	CloseWindow();
	return 0;
}
