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

#define POPULATION_SIZE 1000000
#define EPOCHS 100
#define N_KEEPS 0.15
#define N_KEEPS_2 0.4

using namespace std;

string dtos(double d);
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
        cout << "Epoch " << setw(6) << i << ": " << setw(8) << dtos(population[0]->get_loss()) << " > " << setw(8) << dtos(population[1]->get_loss()) << " > " << setw(8) << dtos(population[2]->get_loss()) << endl;

        int keep_size = (int)(N_KEEPS * POPULATION_SIZE);

        vector<Satellite*> new_population;
        // keep the best satellite
        new_population.push_back(population[0]);

        // keep keep_size satellites by turnament selection
        
        for(int j = 0; j < keep_size; j++){
            int index_1 = rand() % keep_size;
            int index_2 = rand() % keep_size;
            if(population[index_1]->get_loss() > population[index_2]->get_loss()){
                new_population.push_back(population[index_1]);
            }else{
                new_population.push_back(population[index_2]);
            }
        }

        int n_children = (int)(N_KEEPS_2 * (POPULATION_SIZE - keep_size));
        vector<Satellite*> children;
        // create n_children children by crossover on the new population
        for(int j = 0; j < n_children; j++){
            int index_1 = rand() % keep_size;
            int index_2 = rand() % keep_size;
            Satellite* child = new Satellite(*new_population[index_1], *new_population[index_2]);
            children.push_back(child);
        }

        // mutate the new population
        for(int j = 1; j < new_population.size(); j++){
            new_population[j]->mutate();
        }

        // merge the new population and children
        for(int j = 0; j < children.size(); j++){
            new_population.push_back(children[j]);
        }

        // fill new population with random satellites
        for(int j = 0; j < POPULATION_SIZE - new_population.size(); j++){
            Satellite* s = new Satellite();
            new_population.push_back(s);
        }

        // replace the population with the new population
        population = new_population;

        
    }

    // print the best satellite
    cout << "Best satellite: " << endl;
    cout << "Loss: " << population[0]->get_loss() << endl;
    cout << "Data: " << *population[0] << endl;

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

// double to 2 decimal string
string dtos(double d){
    stringstream ss;
    ss << fixed << setprecision(2) << d;
    return ss.str();
}