
#include<stdio.h>
int main()
{
	int n, a[100], i, max, small;
	//printf("Enter the number of Elements\n"); 	
	scanf("%d", &n);
	//printf("Enter the Elements of the array\n"); 
	for(i=0; i<n; i++)
		scanf("%d", &a[i]);
	max=a[0];
	for(i=0; i<n; i++)
		if(a[i]>max)
			max=a[i];
	small=a[0];
	for(i=0; i<n; i++)
		if(a[i]<small)
			small=a[i];
	printf("The smallest element is %d\n", small);
	printf("The Largest element is %d\n", max);  
}
