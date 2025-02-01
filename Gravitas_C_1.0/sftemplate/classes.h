#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/Audio.hpp>
#include <SFML/Window.hpp>
#include <fstream>
#include <iostream>
#include <ctime>
#include <cstdlib>
#include <Windows.h>
#include <string>
#include <chrono>
#include <cstdlib>
#include <intrin.h>
#include <math.h>

/*--Debug definitions--*/
#define Log(x) std::cout << x << std::endl
#define Log_s(x) std::cout << x

static double mod(double first, double last)
{
	double x1 = first / last;
	double x2 = (int)(first / last);
	return (x1 - x2) * last;
}
static double random(double bottom, double top)
{
	srand(std::chrono::duration_cast<std::chrono::nanoseconds>
		(std::chrono::system_clock::now().time_since_epoch()).count() + rand());

	double diff = top - bottom;
	double out = rand() / 100.f;
//	out /= 100.f;
	if (diff != 0) {
		out = mod(out, diff);
	}
	else {
		out = 0;
	}
	out += bottom;
	return out;
}


/*--constants--*/

const double e = 2.718281828459045235360287471352662497757247093699959574966967627724076;

const double pi = 3.141592653589793238462643383279502884197169399375105820974944592307816;

const double rt2rec = 0.7071067811865476; //	=sqrt(0.5);

float G = 6.67E-11;




float DA_log(float base, float x){
	return log(x) / log(base);
}
float DA_logApprox(float base, float x){
	int a = 0;
	while (x) {
		x /= 10;
		a++;
	}
	x *= pow(a, base);
	return -1;
}


/*--RenderWindow Declaration--*/
sf::Vector2i screen(1920, 1080);
sf::RenderWindow Window(sf::VideoMode(screen.x, screen.y), "Gravitas Indev", sf::Style::Default);

/*--SystemInformation--*/
void HideConsole()
{
	::ShowWindow(::GetConsoleWindow(), SW_SHOW);
}

void noFunction(float a, float b) { ; }

/*--struct Declarations--*/
struct vec2
{
	float x, y;

	//Overloading
	vec2 operator+(const vec2& samp) const {
		return { x + samp.x,y + samp.y };
	}
	vec2 operator*(const float& samp) const {
		return { x * samp,y * samp };
	}
	vec2 operator-(const vec2& samp) const {
		return { x - samp.x,y - samp.y };
	}
};

float vecmod(vec2 vec) {
	return sqrt(vec.x * vec.x + vec.y * vec.y);
}