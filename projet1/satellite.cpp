#include "satellite.h"
#include <math.h>
#include <iomanip>

double fRand(double fMin, double fMax)
{
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}

double gaussianRand(double mean, double std)
{
    double u1 = fRand(0.0, 1.0);
    double u2 = fRand(0.0, 1.0);
    double randStdNormal = sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
    return mean + std * randStdNormal;
}

Satellite::Satellite(){
    p0 = fRand(-100, 100);
    p1 = fRand(-100, 100);
    p2 = fRand(-100, 100);
    p3 = fRand(-100, 100);
    p4 = fRand(-100, 100);
    p5 = fRand(-100, 100);
    loss=0;
}

Satellite::Satellite(Satellite sa, Satellite sb){
    p0 = sa.p0;
    p1 = sa.p1;
    p2 = sa.p2;
    p3 = sb.p3;
    p4 = sb.p4;
    p5 = sb.p5;
    loss=0;
}

void Satellite::mutate(){
    p0 += gaussianRand(0, 0.1);
    p1 += gaussianRand(0, 0.1);
    p2 += gaussianRand(0, 0.1);
    p3 += gaussianRand(0, 0.1);
    p4 += gaussianRand(0, 0.1);
    p5 += gaussianRand(0, 0.1);
}

void Satellite::reset_loss(){
    loss = 0;
}

double Satellite::get_loss(){
    return loss;
}

void Satellite::evaluate(double t, double x, double y){
    double rx = pow((x-p0*sin(p1*t+p2)),2);
    double ry = pow((y-p3*sin(p4*t+p5)),2);
    loss += rx + ry;
}

bool operator<(const Satellite& s1, const Satellite& s2){
    return s1.loss < s2.loss;
}

bool Satellite::compare_loss(const Satellite* s1, const Satellite* s2){
    return s1->loss < s2->loss;
}

ostream& operator<<(ostream& os, const Satellite& s){
    os << "p0: " << setw(10) << s.p0 << " p1: " << setw(10) << s.p1 << " p2: " << setw(10) << s.p2 << " p3: " << setw(10) << s.p3 << " p4: " << setw(10) << s.p4 << " p5: " << setw(10) << s.p5 << " loss: " << setw(6) << s.loss << endl;
    return os;
}

bool Satellite::operator==(const Satellite& s){
    return (p0 == s.p0 && p1 == s.p1 && p2 == s.p2 && p3 == s.p3 && p4 == s.p4 && p5 == s.p5);
}