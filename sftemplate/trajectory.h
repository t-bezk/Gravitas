#pragma once
#include "bodymanager.h"

class ellipse {
private:
	sf::CircleShape points[360];

public:
	ellipse() {
		for (int i = 0; i < 360; i++)
		{
			points[i].setFillColor(sf::Color::Blue);
			points[i].setRadius(1);
		}
	}

	vec2 parameters(int N, float p, float e, float phi) {
		float r = p / (1 + e * cos((float)N * pi / 180.f +  + pi + phi));
		return { r * (float)cos((float)N * pi / 180.f ), r * (float)sin((float)N * pi / 180.f ) };
	}

	void draw(sf::RenderWindow& window, float p, float e, float phi) {
		for (int i = 0; i < 360; i++) {
			vec2 posR = parameters(i, p, e, phi);
			this->points[i].setPosition(posR.x + screen.x / 2, posR.y + screen.y / 2);
			window.draw(this->points[i]);
		}
	}
};