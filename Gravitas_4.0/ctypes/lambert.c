#include <stdio.h>
#include <math.h>
#include <omp.h>

const double PI = 3.141592653589793238462643383279502884197169399375105821;

const double f23 = 2. / 3.;

double _initial_guess(double T, double ll, short M)    {

    // Equation 19
    double T_0 = acos(ll) + ll * sqrt(1 - ll * ll) + M * PI;    // eq.19
    double T_1 = f23 * (1 - ll * ll * ll);  //eq.21

    double x_0;
    if (T >= T_0)
        x_0 = pow(T_0 / T, f23) - 1;
    else if (T < T_1)
        x_0 = 2.50 * ( T_1 / T ) * (T_1 - T) / (1 - pow(ll,5)) + 1;
    else    //Otherwise if T is between T_0 and T_1
        x_0 = pow(T_0 / T, log2(T_1 / T_0)) - 1;
    return x_0;
}


double _tof_equation_p(double x, double y, double T, double ll) {
    //TODO: What about derivatives when x approaches 1?
    return (3 * T * x - 2 + pow(2 * ll, 3) * x / y) / pow(1 - x, 2);
}

double _tof_equation_p2(double x, double y, double T, double dT, double ll) {
    return (3 * T + 5 * x * dT + 2 * (1 - ll * ll) * pow(ll, 3) / pow(y, 3)) / (1 - x * x);
}

double _tof_equation_p3()   {
    return 0;
}


int main(){

    double val = _initial_guess(200., 0.5, 0);

    printf("%f", val);

    return 0;
}