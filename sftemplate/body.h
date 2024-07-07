#pragma once
#include "classes.h"

class body {
private:
	sf::CircleShape circ;
public:

	float mass = 1;
	vec2 pos = { 0,0 };
	vec2 vel = { 0,0 };
	vec2 acc = { 0,0 };

	float dt = 0.05f;

	float prog_angle = 0;
	float angle = 0;

	bool print = false;

	vec2 prevAngs = { 0.f, 0.f };

	bool change_angle = true;

	float ec = 0;
	float p = 0;
	float E = 0;
	float L = 0;

	float angular_progression = 0.f;

	body() {
		this->circ.setRadius(5);
		this->circ.setPosition(screen.x / 2, screen.y / 2);
	}

	void draw(sf::RenderWindow& window) {
		this->circ.setPosition(this->pos.x + screen.x / 2, this->pos.y + screen.y / 2);
		window.draw(this->circ);
	}

	void timeStep() {
		this->vel = this->vel + this->acc * dt;
		this->pos = this->pos + this->vel * dt;
		this->acc = { 0,0 };
	}

	void accel(vec2 r2, float mass) {

		vec2 dist = r2 - this->pos;

		float mu = mass;

		float m = this->mass;

		float moddist = vecmod(dist);

		float modacc = mu / (moddist * moddist);

		angle = atan2f(dist.y, dist.x);

		this->acc = { this->acc.x + modacc * cos(angle), this->acc.y + modacc * sin(angle) };


		//Calculate dA
		float rmod = vecmod(this->pos);

		float vmod = vecmod(this->vel);

		float dA = 0.5 * rmod * (rmod + vmod * dt);


		//Semi-major axis
		float a = 1 / (2 / rmod - pow(vmod, 2) / mu);


		//Energy Calculation
		float ME = -mu / (2 * a);


		//Component Angle
		float cphi = acosf((pos.x * vel.x + pos.y * vel.y) / (rmod * vmod));


		//Specific Angular Momentum
		float h = vmod * rmod * cos(cphi - pi / 2);


		//Velocity Components
		float vr0 = (vel.x * dist.x + vel.y * dist.y) / moddist;

		float vth0 = sqrt(vmod * vmod - vr0 * vr0);


		//Eccentricity
		float ppar = h * h / (mu);

		float ecc = sqrt(1 + 2 * (ME * ppar / mu));

		float rp = ppar / (1 + ecc);

		float ra = ppar / (1 - ecc);

		float vmax = sqrt(2 * (ME + (mu / rp)));

		float vmin = sqrt(2 * (ME + (mu / ra)));


		//Angle Progression
		float angVel = vth0 / moddist;

		this->angular_progression += angVel * dt;
		if (this->angular_progression > 2 * pi)
			this->angular_progression -= 2 * pi;

		float prAng = ((1 / ecc) * ((ppar / moddist) - 1));
		if (abs(prAng) == 1)
			prAng *= pi / 2;
		else
			prAng = acosf(prAng);

		float pveSoln = this->angular_progression + prAng + pi;
		float nveSoln = this->angular_progression - prAng + pi;

		if (pveSoln - prevAngs.x < nveSoln - prevAngs.y)
			this->prog_angle = this->angular_progression + prAng + pi;
		else
			this->prog_angle = this->angular_progression - prAng + pi;

		prevAngs = { pveSoln, nveSoln };


		//Objective Updates
		this->ec = ecc;
		this->p = ppar;


		//Print
		if (this->print) {
			Print(prog_angle);
		}

	}

	void callib(vec2 r2, float mass, bool print) {
		vec2 dist = r2 - this->pos;

		float mu = mass;

		float m = this->mass;

		float moddist = vecmod(dist);
		float modacc = mu / (moddist * moddist);
		float angle = atan2f(dist.y, dist.x);
		this->acc = { this->acc.x + modacc * cos(angle), this->acc.y + modacc * sin(angle) };


	}

};