#include <stdio.h>
#include <string.h>

int main()
{
	int t;
	char str1[100],str2[100];
	scanf("%d",&t);
	while(t--)
	{
		scanf("%s",str1);
		scanf("%s",str2); 
		strcat(str1,str2);
		printf("%s\n",str1);  
	}
	return 0;
}

