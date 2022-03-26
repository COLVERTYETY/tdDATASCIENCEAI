#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <math.h>
#include <time.h>
#include <sstream>
#include "satellite.h"
#include <iomanip>
#include <random>

#define POPULATION_SIZE 10000
#define EPOCHS 1000
#define N_KEEPS 0.8
#define N_KEEPS_2 0.8

using namespace std;

double frand(double fMin, double fMax);
vector<vector<string>> parse_csv(string filename);
void print_csv(vector<vector<string>> csv_data);
vector<vector<double>> parse_csv_to_double(string filename);
void print_csv(vector<vector<double>> csv_data);

int main(){
    srand (time(NULL));
    // parse csv from file "position_sample.csv" to vector of vector of string
    vector<vector<string>> csv_data = parse_csv("position_sample.csv");
    // parse to double
    vector<vector<double>> csv_data_double = parse_csv_to_double("position_sample.csv");
    
    vector<Satellite*> population;

    for(int i = 0; i < POPULATION_SIZE; i++){
        Satellite* s = new Satellite();
        population.push_back(s);
    }

    for(int i = 0; i < EPOCHS; i++){
        // evaluate the population
        for(int j = 0; j < POPULATION_SIZE; j++){
            population[j]->reset_loss();
            for(int k = 0; k < csv_data_double.size(); k++){
                population[j]->evaluate(csv_data_double[k][0], csv_data_double[k][1], csv_data_double[k][2]);
            }
        }
        // sort population by loss
        sort(population.begin(), population.end(), Satellite::compare_loss);

        // print the best satellite with standardized width
        cout << "Epoch " << setw(6) << i << ": " << *population[0] << endl;
        cout << "Epoch " << setw(6) << i << ": " << *population[1] << endl;
        cout << "Epoch " << setw(6) << i << ": " << *population[2] << endl;

        int keep_size = (int)(N_KEEPS * POPULATION_SIZE);

        // find loss max
        double loss_max = population[POPULATION_SIZE - 1]->get_loss();
        double loss_min = population[0]->get_loss();
        vector<Satellite*> new_population;

        for(int j = 0; j < POPULATION_SIZE && (new_population.size() < N_KEEPS*POPULATION_SIZE); j++){
            double p = frand(loss_min, loss_max);
            if(p > population[j]->get_loss()){
                new_population.push_back(population[j]);
            }
        }


        int old_size = new_population.size();
        // print old_size
        // cout << "old_size: " << old_size << endl;
        int n_children = ((int)(POPULATION_SIZE - new_population.size()))*N_KEEPS_2;

        for(int j = 0; j < n_children; j++){
            int a = rand()%(j+1);
            int b = rand()%(j+1);
            new_population.push_back(new Satellite(*new_population[a], *new_population[b]));
        }

        for(int j = 1; j < new_population.size(); j++){
            new_population[j]->mutate();
        }

        while(new_population.size() < POPULATION_SIZE){
            new_population.push_back(new Satellite());
        }
        
    }

    return 0;
}

vector<vector<double>> parse_csv_to_double(string filename){
    vector<vector<string>> csv_data = parse_csv(filename);
    vector<vector<double>> csv_data_double;
    // on se fiche de l'entete
    for(int i = 1; i < csv_data.size(); i++){
        vector<double> row;
        for(int j = 0; j < csv_data[i].size(); j++){
            row.push_back(stof(csv_data[i][j]));
        }
        csv_data_double.push_back(row);
    }
    return csv_data_double;
}

vector<vector<string>> parse_csv(string filename){
    vector<vector<string>> csv_data;
    ifstream file(filename);
    string line;
    while(getline(file, line)){
        vector<string> row;
        stringstream lineStream(line);
        string cell;
        while(getline(lineStream, cell, ';')){
            row.push_back(cell);
        }
        csv_data.push_back(row);
    }
    return csv_data;
}

void print_csv(vector<vector<string>> csv_data){
    for(int i = 0; i < csv_data.size(); i++){
        for(int j = 0; j < csv_data[i].size(); j++){
            cout << csv_data[i][j] << " ";
        }
        cout << endl;
    }
}

double frand(double fMin, double fMax)
{
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}
