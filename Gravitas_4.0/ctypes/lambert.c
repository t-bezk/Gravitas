#include <stdio.h>
#include <math.h>
#include <omp.h>

const double PI = 3.141592653589793238462643383279502884197169399375105821;

const double f23 = 2. / 3.;

double hyp2f1b(double x) {
    if (x >= 1.0)
        return INFINITY;
    else {
        double res = 1.0;
        double term = 1.0;
        double ii = 0;
        for (int ii = 0; ii < 100; ii++) {
            term = term * (3 + ii) * (1 + ii) / (2.5 + ii) * x / (ii + 1);
            double res_old = res;
            res += term;
            if (res_old == res) 
                return res;
        }
    }
}


double _compute_psi(double x, double y, double ll)   {

    if (-1. <= x < 1.)
        return acos(x * y + ll * (1. - x * x));  // Elliptic Motion
    else if (x > 1.)
        return asinh((y - x * ll) * sqrt(x * x - 1.)); // Hyperbolic Motion
    else
        return 0.;  //Parabolic Motion
}


double _tof_equation(double x, double y, double T0, double ll, short M)    {

    double T_;
    if (M == 0 && sqrt(0.6) < x && x < sqrt(1.4))   {
        double eta = y - ll * x;
        double hS_1 = hyp2f1b((1. - ll - x * eta) * .5);
        double Q = 2 * f23 * hS_1;
        T_ = (eta * eta * eta * Q + 4 * ll * eta) * .5;
    }
    else    {
        double psi = _compute_psi(x, y, ll);
        T_ = 0.;
    }

    return T_ - T0;
}


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
    return (3. * T * x - 2. + 2. * pow(ll, 3.) * x / y) / (1 - x * x);
}

double _tof_equation_p2(double x, double y, double T, double dT, double ll) {
    return (3 * T + 5 * x * dT + 2 * (1 - ll * ll) * pow(ll, 3) / pow(y, 3)) / (1 - x * x);
}

double _tof_equation_p3(double x, double y, double _, double dT, double ddT, double ll) {
    return (7 * x * ddT + 8 * dT - 6 * (1 - ll * ll) * pow(ll, 5) * x / pow(y, 5)) / (1 - x * x);
}

int main(){

    double val = _initial_guess(200., 0.5, 0);

    printf("%f", val);

    return 0;
}