#include<stdio.h>
#include<stdlib.h>
#include<math.h>
int main()
{
	int n, a[100], i,t;
	float sum=0, mean, sd;
	scanf("%d",&t);
	while(t--)
	{
		sum=0;
		scanf("%d", &n);
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
		printf("%.2f %.2f %.2f\n", mean , sd*sd , sd);
	}
	return 0;  
}

