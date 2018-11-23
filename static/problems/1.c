#include<stdio.h>
<<<<<<< HEAD
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

=======

void tower(int n, char source, char dest, char temp)
{
	if(n>0)
	{
		tower(n-1,source,temp,dest);
		printf("%d %c %c\n",n,source,dest);
		tower(n-1,temp,dest,source);
	}
	return;
}

int main()
{
	int t;
	scanf("%d",&t);
	while(t--)
	{
		int n;
		scanf("%d",&n);
		tower(n,'S','D','T');
		printf("\n");
	}
	return 0;
}
>>>>>>> a31856866d97c0782ac69c9c3c38287607a974be
