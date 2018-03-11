#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include "mkl.h"
using namespace std;
#define max(x,y) (((x) > (y)) ? (x) : (y))

double* init(int l){
	double *x = (double*)mkl_malloc(l*l*sizeof(double), 64);
	int k =0;
	for(int i=0;i<l;i++){
 		for(int j=0;j<l;j++){
 			x[k] = 0.5 + (double)((i+j)%50-30)/50.0;
 			k++;
 		}
 	}
 	return x;
}
double* init(int l, int h){
	double *w = (double*)mkl_malloc(l*h*sizeof(double),64);
	for(int i=0;i<l;i++){
 		for(int j=0;j<h;j++){
 			w[i*h+j] = 0.5 + (double)((i+j)%50-30)/50.0;
 		}
 	}
 	return w;
}

double* forward(double* mat, double* x, int l, int h){
	double *output = (double*)mkl_malloc(l*sizeof(double),64);
	//h is input layer, l is output layer dimensions
    cblas_dgemv(CblasRowMajor, CblasNoTrans, l, h, 1, mat, h, x, 1, 0, output, 1);
    for(int i=0;i<l;i++) output[i] = (output[i]<0)?0:output[i];
	return output;

}

int main(){
	clock_t start_t,end_t,total_t;
	doubl* x = init(224);
	double* w1 = init(4000,50176);
	double* w2 = init(1000,4000);
	start_t=clock();
	double* z = forward(w2,forward(w1,x, 4000, 50176), 1000, 4000);
	end_t = clock();
	total_t = (double)(end_t - star_tt_t) / CLOCKS_PER_SEC;
	double buf = (double)size*sizeof(int)/total_t;
	double sum = 0;
	for(int i=0;i<1000;i++) sum += z[i];
	printf("%f\n", sum);
 	
 	return 0;
 }