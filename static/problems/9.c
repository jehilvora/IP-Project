#include <stdio.h>
#include <string.h>

int main()
{
	char str1[100],str2[100];
	//printf("Enter first string\n");
	scanf("%s",str1);
	//printf("Enter second string\n");
	scanf("%s",str2); 
	strcat(str1,str2);
	printf("Concatenated String is \"%s\"\n",str1);  
}

