#include <iostream>
#include <algorithm>
#include <ctime>
#include <vector>
#include <time.h>
using namespace std;
#define size 1048576
int main(){
	clock_t t;
	vector<int> bws;
	int i = 16;
	while(i>=0){
		int *arr = (int*)malloc(size*sizeof(int));
		for(long i=0;i<size;i++){
			arr[i] = 0;
		}

		int sum = 0;
		t=clock();
		for(long i=0;i<size;i++){
			sum+=arr[i];
			printf("%d\n",sum);

		}
		t=clock()-t;
		free(arr);
		arr = NULL;
		//cout<<"time is "<<t<<endl;
		float buf = (float)size/t;
		printf("Bandwidth = %lf\n", buf);
		bws.push_back(buf);
	}
	cout<<endl<<"Bws are: "<<endl;
	for(int i=0;i<16;i++){
		cout<<bws[i]<<'\t';
	}


}