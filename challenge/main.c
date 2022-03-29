#include <stdio.h>
#include <stdlib.h>
#include <string.h>

double* get_data_from_csv();
void display_data(double* data, int num_lines);

int N=0;

int main(){
    printf("starting\n");
    double* data = get_data_from_csv();
    display_data(data, 10);
    free(data);
    printf("ending\n");
    return 0;
}

// get the data from the csv
double* get_data_from_csv(){
    FILE* csv = fopen("position_sample.csv", "r");
    if(csv == NULL){
        printf("Error opening file\n");
        return NULL;
    }
    // get the number of lines
    int num_lines = 0;
    char c;
    while((c = fgetc(csv)) != EOF){
        if(c == '\n'){
            num_lines++;
        }
    }
    N=3*num_lines; /// this is dirty hack
    // printf("num_lines: %d\n", N);
    // allocate memory for the data
    double* data = (double*)malloc(N * sizeof(int));
    // reset the file pointer
    fseek(csv, 0, SEEK_SET);
    // read the data of shape %d;%d;%d
    int i=0;
    while(fscanf(csv, "%lf;%lf;%lf", &data[i], &data[i+1], &data[i+2]) != EOF ){
        i+=3;
        printf("%lf;%lf;%lf\n", data[i-3], data[i-2], data[i-1]);
    }
    fclose(csv);
    return data;
}


//display the data
void display_data(double* data, int num_lines){
    for(int i = 0; i < num_lines; i++){
        printf("%lf\n", data[i]);
    }
}
