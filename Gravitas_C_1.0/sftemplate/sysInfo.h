#pragma once
#include "backgrounds.h"
/*
The following functions retrieve system information such as
cpu model, and ram for the top-left debug block.
*/
std::string getSystemInformation()
{
	int CPUInfo[4] = { -1 };
	__cpuid(CPUInfo, 0x80000000);
	unsigned int nExIds = CPUInfo[0];

	// Get the information associated with each extended ID.
	char CPUBrandString[0x40] = { 0 };
	for (unsigned int i = 0x80000000; i <= nExIds; ++i)
	{
		__cpuid(CPUInfo, i);

		// Interpret CPU brand string and cache information.
		if (i == 0x80000002)
		{
			memcpy(CPUBrandString,
				CPUInfo,
				sizeof(CPUInfo));
		}
		else if (i == 0x80000003)
		{
			memcpy(CPUBrandString + 16,
				CPUInfo,
				sizeof(CPUInfo));
		}
		else if (i == 0x80000004)
		{
			memcpy(CPUBrandString + 32, CPUInfo, sizeof(CPUInfo));
		}
	}
	return CPUBrandString;
}
float getRamInfo()
{
	MEMORYSTATUSEX statex;

	statex.dwLength = sizeof(statex); // I misunderstand that

	GlobalMemoryStatusEx(&statex);
	return (float)statex.ullTotalPhys / (1024 * 1024 * 1024);
}