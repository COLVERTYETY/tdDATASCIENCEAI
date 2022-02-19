#ifndef CARTES
#define CARTES
#include <iostream>
#include <iomanip> // setw

class Carte{
    private:
        int *mycards;
        float weight36;
        float weight360;
        float score36=-1;
        float score360=-1;
        float score=-1;
    public:
        Carte();
        ~Carte();
        void mutate();
        void crossover(const Carte& other);
        void evaluate();
        int getscore();
        friend bool operator<(const Carte& a,const Carte& b);
        friend std::ostream& operator<<( std::ostream&  out, const Carte& C);
        static bool comp(const Carte* a, const Carte* b);
};


#endif
