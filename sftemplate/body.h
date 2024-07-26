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

	float prog_angle = 0.f;
	float angle = 0.f;
	float rad_angle = 0.f;

	bool print = false;

	vec2 prevAngs = { 0.f, 0.f };
	vec2 prev2Angs = { 0.f, 0.f };

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

		this->angle = atan2f(dist.y, dist.x);

		this->acc = { this->acc.x + modacc * cos(angle), this->acc.y + modacc * sin(angle) };


		//Calculate dA
		float rmod = vecmod(this->pos);

		float vmod = vecmod(this->vel);


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

		this->rad_angle = this->angle - this->angular_progression;




		float angVel = vth0 / moddist;

		this->angular_progression += angVel * dt;
		if (this->angular_progression > 2 * pi)
			this->angular_progression -= 2 * pi;
		else if (this->angular_progression < - pi)
			this->angular_progression += 2 * pi;

		float ct = ( vth0 * (1 - ecc * ecc) * a / h  - 1) / ecc;
		float st = (vr0 * (1 - ecc * ecc) * a / h) / ecc;

		float th = acosf(ct) - this->angular_progression - pi;
		float th_a = pi - acosf(ct) - this->angular_progression;

		if (th - prevAngs.x < th_a - prevAngs.y)
			this->prog_angle = th_a;
		else
			this->prog_angle = th;

		if (this->prog_angle > pi)
			this->prog_angle -= 2 * pi;
		else if (this->prog_angle < - pi)
			this->prog_angle += 2 * pi;

		prevAngs = { th, th_a };

		//Objective Updates
		this->ec = ecc;
		this->p = ppar;

		//Print
		if (this->print) {
			Print(rad_angle);
		}

	}

	void reset() {
		std::string dat;
		std::string appDat;
		std::ifstream myfile("cel1dat.txt");
		if (myfile.is_open())
		{

			while (std::getline(myfile, dat)) {
				appDat += dat;
			}
			myfile.close();
		}

		std::string celDat[4];
		int app = 0;
		for (int i = 0; i < sizeof(appDat) / sizeof(char); i++)
		{
			if (appDat[i] == ',')
				app++;
			else
				celDat[app] += appDat[i];
		}

		ec = 0;
		p = 0;
		E = 0;
		L = 0;

		prog_angle = 0.f;
		angle = 0.f;
		rad_angle = 0.f;

		prevAngs = { 0.f, 0.f };

		angular_progression = 0.f;

		this->pos = { std::stof(celDat[0]), std::stof(celDat[1]) };
		this->vel = { std::stof(celDat[2]), std::stof(celDat[3]) };
	}

};