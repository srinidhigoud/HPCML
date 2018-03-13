#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include "mkl.h"

#define size 1024*1024*1024*512
#define max(x,y) (((x) > (y)) ? (x) : (y))
void c1(){
	//clock_t start_t,end_t,total_t;
	double max_BW = 0;
	int epochs = 16;	
	while(epochs>=0){
	struct timeval t1, t2;
        double total_t;
  
	int *arr = (int*)malloc(size*sizeof(int));
		for(long i=0;i<size;i++){
			arr[i] = 0;
		}

		int sum = 0;
		gettimeofday(&t1, NULL);
		for(long i=0;i<size;i++){
			sum = (sum+arr[i])%1024;
			//printf("%d\n",sum);

		}
		gettimeofday(&t2, NULL);
		free(arr);
		arr = NULL;
		//cout<<"time is "<<t<<endl;
		total_t = (t2.tv_sec-t1.tv_sec)*1000000 + t2.tv_usec-t1.tv_usec;
		double buf = (double)size*sizeof(int)/total_t;
		printf("%d \t %d \t Bandwidth = %f MB/s\n",16-epochs,sum, buf);
		max_BW = max(max_BW,buf);
		epochs--;
	}
	printf("\nThe maximum Bandwidth is: \t %f\n", max_BW);
}

double* initS4(int l){
	double *x = (double*)malloc(l*l*sizeof(double));
	int k =0;
	for(int i=0;i<l;i++){
 		for(int j=0;j<l;j++){
 			x[k] = 0.5 + (double)((i+j)%50-30)/50.0;
 			k++;
 		}
 	}
 	return x;
}
double** init4(int l, int h){
	double **w = (double**)malloc(l*sizeof(double*));
	for(int i=0;i<l;i++) w[i] = (double*)malloc(h*sizeof(double));
	for(int i=0;i<l;i++){
 		for(int j=0;j<h;j++){
 			w[i][j] = 0.5 + (double)((i+j)%50-30)/50.0;
 		}
 	}
 	return w;
}

double* forward4(double** mat, double* x, int l, int h){
	double *output = (double*)malloc(l*sizeof(double));

	for(int i=0;i<l;i++){
		output[i] = 0;
		for(int j=0;j<h;j++){
			output[i] += mat[i][j]*x[j];
		}
		output[i] = max(0.0,output[i]);
	}
	return output;

}

void c4(){
	printf("\n Question C4---------------------------------------- \n");
	//clock_t start_t,end_t,total_t;
	struct timeval t1, t2;
	double total_t;
	double* x = initS4(224);
	double** w1 = init4(4000,50176);
	double** w2 = init4(1000,4000);
	gettimeofday(&t1, NULL);
	double* z = forward4(w2,forward4(w1,x, 4000, 50176), 1000, 4000);
	gettimeofday(&t2, NULL);
	total_t = t2.tv_usec-t1.tv_usec;
	// double buf = (double)size*sizeof(int)/total_t;
	double sum = 0;
	for(int i=0;i<1000;i++) sum += z[i];
	printf("Sum is %f\n", sum);
	printf("The elapsed time is: \t %f",total_t);
 	
}

 double* initS5(int l){
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
double* init5(int l, int h){
	double *w = (double*)mkl_malloc(l*h*sizeof(double),64);
	for(int i=0;i<l;i++){
 		for(int j=0;j<h;j++){
 			w[i*h+j] = 0.5 + (double)((i+j)%50-30)/50.0;
 		}
 	}
 	return w;
}

double* forward5(double* mat, double* x, int l, int h){
	double *output = (double*)mkl_malloc(l*sizeof(double),64);
	//h is input layer, l is output layer dimensions
    cblas_dgemv(CblasRowMajor, CblasNoTrans, l, h, 1, mat, h, x, 1, 0, output, 1);
    for(int i=0;i<l;i++) output[i] = (output[i]<0)?0:output[i];
	return output;

}

void c5(){
	printf("\n Question C5---------------------------------------- \n");
	//clock_t start_t,end_t,total_t;
	struct timeval t1, t2;
	double total_t;
	double* x = initS5(224);
	double* w1 = init5(4000,50176);
	double* w2 = init5(1000,4000);
	gettimeofday(&t1, NULL);
	double* z = forward5(w2,forward5(w1,x, 4000, 50176), 1000, 4000);
	gettimeofday(&t2, NULL);
	total_t = t2.tv_usec-t1.tv_usec;
	// double buf = (double)size*sizeof(int)/total_t;
	double sum = 0;
	for(int i=0;i<1000;i++) sum += z[i];
	printf("Sum is %f\n", sum);
	printf("The elapsed time is: \t %f",total_t); 
}

int main(){
	c1();
	c4();
	c5();
	return 0;
}
