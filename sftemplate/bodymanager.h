#pragma once
#include "body.h"

class bodymanager {
public:
	body* cele;
	int nobodies = 2;
	vec2 relCom = { 0,0 };


	bodymanager() {
		bool ra = false;

		this->cele = new body[nobodies];

		this->cele[1].print = true;

		if (ra) {	//Debug Physics using N randomly-assorted points
			for (int i = 0; i < nobodies; i++) {
				cele[i].pos = { (float)random(-400.0,400.0),(float)random(-400.f,400.f) };
				cele[i].vel = { (float)random(-10.f,10.f),(float)random(-10.f,10.f) };
				cele[i].mass = random(100.f, 10000.f);
			}
		}
		else {
			cele[0].pos = { 0,0 };
			cele[0].vel = { 0,0 };
			cele[0].mass = 10000.f;

			cele[1].pos = { 200,0 };
			cele[1].vel = { 0,4 };
			cele[1].mass = 0.1f;
		}

		/*
		{	//Positions
			cele[0].pos = { 0,0 };
			cele[1].pos = { 0,100 };
			cele[2].pos = { 0,200 };
			cele[3].pos = { 0,300 };
			cele[4].pos = { 0,500 };
			cele[5].pos = { -1000,-400 };

			Log(random(1, 4));
		}

		{	//Velocities
			cele[0].vel = { 0,0 };
			cele[1].vel = { 10,0 };
			cele[2].vel = { 7.071,0 };
			cele[3].vel = { 5.774,0 };
			cele[4].vel = { 5,0 };
			cele[5].vel = { 5,0 };
		}

		{	//Masses
			cele[0].mass = 10000;
			cele[1].mass = 0.01;
			cele[2].mass = 0.1;
			cele[3].mass = 10000;
			cele[4].mass = 10;
			cele[5].mass = 10000;
		}*/
	}

	~bodymanager() { delete[] cele; }

	vec2 com() {
		vec2 com = { 0.0, 0.0 };
		double M = 0.0;
		for (int i = 0; i < nobodies; i++) {
			com.x += cele[i].mass * cele[i].pos.x *exp(-pow(vecmod(cele[i].pos - relCom), 2) / 1000);
			com.y += cele[i].mass * cele[i].pos.y *exp(-pow(vecmod(cele[i].pos - relCom), 2) / 1000);
			M += cele[i].mass *exp(-pow(vecmod(cele[i].pos - relCom), 2) / 1000);
		}
		this->relCom = com * (1 / M);
		return relCom;
	}

	void multireact() {
		for (int i = 0; i < nobodies; i++) {
			for (int j = 0; j < nobodies; j++) { //Let j = i,
				if (i != j) {
					float dist = vecmod(cele[i].pos - cele[j].pos);
					if (dist < 5) {
						cele[i].vel = cele[i].vel * -1;
						cele[j].vel = cele[j].vel * -1;
					}
					else
						cele[i].accel(cele[j].pos, cele[j].mass);
				}
			}
		}
		for (int i = 0; i < nobodies; i++) {
			cele[i].timeStep();
		}

	}

	void draw(sf::RenderWindow& window) {
		for (int i = 0; i < nobodies; i++) {
			cele[i].draw(window);
		}
	}

};