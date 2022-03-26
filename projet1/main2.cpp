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
#include <bits/stdc++.h>

#define POPULATION_SIZE 10000
#define EPOCHS 1000
#define N_KEEPS 0.2
#define N_KEEPS_2 0.6

using namespace std;

vector<vector<string>> parse_csv(string filename);
void print_csv(vector<vector<string>> csv_data);
vector<vector<double>> parse_csv_to_double(string filename);
void print_csv(vector<vector<double>> csv_data);

int main(){
    // parse csv from file "position_sample.csv" to vector of vector of string
    vector<vector<string>> csv_data = parse_csv("position_sample.csv");
    // parse to double
    vector<vector<double>> csv_data_double = parse_csv_to_double("position_sample.csv");
    
    set<Satellite*> set_pop;

    random_device rd;
    mt19937 gen(rd());

    exponential_distribution<double> dist(3);

    while(set_pop.size() < POPULATION_SIZE){
        Satellite* s = new Satellite();
        set_pop.insert(s);
    }

    // transform set to vector
    vector<Satellite*> population;
    for(auto it = set_pop.begin(); it != set_pop.end(); it++){
        population.push_back(*it);
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

        // choose randomly N_KEEPS*POPULATION_SIZE in population with probability (1/item.get_loss())/total

        vector<Satellite*> new_population; 

        double total = 0;
        for(int j = 0; j < POPULATION_SIZE; j++){
            total += 1/population[j]->get_loss();
        }
        
        for(int j = 0; j < POPULATION_SIZE; j++){
            double prob = 1/population[j]->get_loss()/total;
            if(dist(gen) < prob){
                new_population.push_back(population[j]);
            }
        }



        

        int keep_size = (int)(N_KEEPS * POPULATION_SIZE);
        
        
        vector<Satellite*> new_population;
        for(int j = 0; j < keep_size; j++){
            new_population.push_back(population[(int)dist(gen)]);
        }

        for(int j = 1; j < keep_size; j++){
            population[j] = new_population[j];
        }
        int keep_size_2 = (int)(N_KEEPS_2 * POPULATION_SIZE);
        // fill rest of population with new satellites
        for(int j = keep_size; j < keep_size+keep_size_2; j++){
            Satellite* s = new Satellite(*population[(int)dist(gen)], *population[(int)dist(gen)]);
            population[j] = s;
        }

        // remove all duplicates
        sort(population.begin(), population.end());
        population.erase(unique(population.begin(), population.end()), population.end());

        // fill with new satellites
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

void print_csv(vector<vector<string>> csv_data){
    for(int i = 0; i < csv_data.size(); i++){
        for(int j = 0; j < csv_data[i].size(); j++){
            cout << csv_data[i][j] << " ";
        }
        cout << endl;
    }
}
