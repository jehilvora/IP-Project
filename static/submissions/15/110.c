
    
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
int main()
{
	int n, a[100], i;
	float sum=0, mean, sd;
	//printf("Enter the number of Elements\n"); 	
	scanf("%d", &n);
	//printf("Enter the Elements of the array\n"); 	
	for(i=0; i<n; i++)
	{
		scanf("%d", &a[i]);
		sum=sum+a[i]; 	
	}
	mean=sum/n;
	sum=0;
	for(i=0; i<n; i++)
		sum = sum + (a[i]*a[i]);
	sd=sqrt(sum/n - (mean*mean));
	printf("Mean is %f\n", mean);
	printf("Varience %f\n",sd*sd);
	printf("Standard deviation is %f",sd);
	return 0;  
}

