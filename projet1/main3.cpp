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

#define POPULATION_SIZE 200000
#define EPOCHS 200
#define N_KEEPS 0.3
#define N_KEEPS_2 0.8

using namespace std;

string dtos(double d);
double frand(double fMin, double fMax);
void print_double_csv(vector<vector<double>> csv_data);
vector<vector<string>> parse_csv(string filename);
vector<vector<double>> parse_csv_to_double(string filename);
void print_csv(vector<vector<double>> csv_data);

int main(){
    srand (time(NULL));
    // parse csv from file "position_sample.csv" to vector of vector of string
    vector<vector<string>> csv_data = parse_csv("position_sample.csv");
    // parse to double
    vector<vector<double>> csv_data_double = parse_csv_to_double("position_sample.csv");

    
    vector<Satellite*> population;



    #pragma omp parallel for
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

        double total = 0;
        for(int j = 0; j < POPULATION_SIZE; j++){
            total += 1/population[j]->get_loss();
        }

        vector<double> probabilities;
        for(int j = 0; j < POPULATION_SIZE; j++){
            probabilities.push_back((1./population[j]->get_loss())/total);
        }
        discrete_distribution <int> distribution(cbegin(probabilities), cend(probabilities));
        int const outputSize = POPULATION_SIZE * N_KEEPS;
        vector<decltype(distribution)::result_type> indices;
        indices.reserve(outputSize);
        generate_n(back_inserter(indices), outputSize,
        [distribution = std::move(distribution), 
         generator = std::default_random_engine{}
        ]() mutable {
            return distribution(generator);
        });

        vector<decltype(population)::value_type> output;

        output.reserve(outputSize);

        transform(cbegin(indices), cend(indices),
        back_inserter(output),
        [&population](auto const index) {
            return population[index];
        });

        // replace the population with the new population
        population = output;

        vector<Satellite*> new_population;

        for(int j = 0; j < (POPULATION_SIZE - population.size())*N_KEEPS_2; j++){
            // crossover
            int parent1 = rand() % population.size();
            int parent2 = rand() % population.size();
            Satellite* child = new Satellite(*population[parent1], *population[parent2]);
            new_population.push_back(child);
        }

        // extends population with new_population
        for(int j = 0; j < new_population.size(); j++){
            population.push_back(new_population[j]);
        }

        // for j in last N_KEEPS*POPULATION_SIZE, mutate
        for(int j = 0; j < N_KEEPS*POPULATION_SIZE; j++){
            population[population.size() - 1 - j]->mutate();
        }

        while(population.size() < POPULATION_SIZE){
            Satellite* s = new Satellite();
            population.push_back(s);
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

void print_double_csv(vector<vector<double>> csv_data){
    for(int i = 0; i < csv_data.size(); i++){
        for(int j = 0; j < csv_data[i].size(); j++){
            cout << csv_data[i][j] << ";";
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