#include <iostream>


using namespace std;

class Satellite {
    private:
        double p0;
        double p1;
        double p2;
        double p3;
        double p4;
        double p5;
        double loss = 0;
    public:
        Satellite();

        void mutate();

        Satellite(Satellite sa, Satellite sb);

        void evaluate(double t, double x, double y);

        double get_loss();

        void reset_loss();

        friend ostream& operator<<(ostream& os, const Satellite& s);
        friend bool operator<(const Satellite& s1, const Satellite& s2);
        static bool compare_loss(const Satellite* s1, const Satellite* s2);
        bool operator==(const Satellite& s);

        // static gaussian random number generator between 0 and 1
};