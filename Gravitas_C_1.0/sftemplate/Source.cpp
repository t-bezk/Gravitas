
/*
	C. Tomas Bezkorowajnyj 2024 | All Rights Reserved
	Github: @Attempt4
	Indev v. 0.1 git

*/



/*--Includes--*/
#define NOMINMAX
#include <Windows.h>
#include <iostream>


/*--preprocessor--*/

#define DA_DEBUG_MODE 1

#if DA_DEBUG_MODE == 1
#define Log(x) std::cout << x << std::endl
#define Print(x) std::cout << x << std::endl
#define DA_HIDE_CONSOLE
#define DA_END_PROCESS std::cin.get()
#else 
#define Log(x)
#define Print(x)
#define DA_HIDE_CONSOLE ::ShowWindow(::GetConsoleWindow(), SW_HIDE)
#define DA_END_PROCESS 
#endif


/*--Call header file prerequisites--*/
#include "trajectory.h"


int main()
{
	sf::Event event;
	sf::Clock clock;
	sf::Clock delay;
	sf::View view;
	
	view.setViewport(sf::FloatRect(0, 0, 1.0f, 1.0f));
	view.setSize(screen.x, screen.y);

	//Window.setFramerateLimit(60);
	Window.setKeyRepeatEnabled(false);
	

	//Body definitions
	ellipse ellipse;
	bodymanager* bm;
	bm = new bodymanager;

	float angleEE = 0.f;


	bm->cele[1].reset();
	while (Window.isOpen())
	{
		
		while (Window.pollEvent(event))
		{
			switch (event.type)
			{
			case sf::Event::Closed:
			{
				Window.close();
				break;
			}
			case sf::Event::KeyPressed:
			{
				if (sf::Keyboard::isKeyPressed(sf::Keyboard::R))
					bm->cele[1].reset();
				break;
			}
			}
		}

		view.setViewport(sf::FloatRect(bm->com().x / screen.x, bm->com().y / screen.y, 1.0f, 1.0f));

		if (sf::Keyboard::isKeyPressed(sf::Keyboard::Q))
			angleEE -= 0.01f;
		if (sf::Keyboard::isKeyPressed(sf::Keyboard::W))
			angleEE += 0.01f;



		/*--Time Step Multiple Body Interactions--*/
		bm->multireact();

		/*--Draw--*/
		Window.setView(view);
		bm->draw(Window);
		ellipse.draw(Window, bm->cele[1].p, bm->cele[1].ec, bm->cele[1].prog_angle - bm->cele[1].rad_angle - pi);

		//Print(bm->cele[1].prog_angle << ", " << angleEE);

		/*--Display--*/
		Window.display();
		Window.clear();
	}

	delete bm;

	return 0;
}
