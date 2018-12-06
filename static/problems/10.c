#include<stdio.h>

int main()
{
	int n, num, sum=0, i,t;
	scanf("%d", &t);
	while(t--)
	{
		scanf("%d", &n);
		sum=0;
		for(i=0; i<n; i++) 	
		{
			scanf("%d", &num);
			sum = sum + num*num; 
		}
		printf("Sum of squares of the given numbers is %d\n", sum);
	}
	return 0;  
}

