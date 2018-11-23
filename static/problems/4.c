<<<<<<< HEAD
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

=======
#include<stdio.h>
#include<stdlib.h>

struct node
{
	int data;
	struct node *link;
};

typedef struct node *NODE;
NODE first=NULL;
NODE insert_front(NODE);
NODE insert_pos(NODE, int);
NODE delete_front(NODE);
NODE delete_pos(NODE, int);
void display (NODE);

int main()
{
	int q;
	scanf("%d",&q);
	while(q--)
	{
		int choice,pos;
		scanf("%d",&choice);
		switch(choice)
		{
			case 1:
			scanf("%d",&pos);
			if(pos == 0)
				first = insert_front(first);
			else
				first = insert_pos(first, pos);
			break;

			case 2:
			scanf("%d",&pos);
			if(pos == 0)
				first = delete_front(first);
			else
				first=delete_pos(first, pos);
			break;

			case 3:
			display(first);
			break;

			case 4:
			exit(0);
		}
	}
}
NODE insert_front(NODE first)
{
	NODE newnode;
	newnode=(NODE)malloc(sizeof(struct node));
	newnode->link=0;
	scanf("%d",&newnode->data);
	if(first==NULL)
	{
		first=newnode;
		return(first);
	}
	newnode->link=first;
	first=newnode;
	return(first);
}
NODE insert_pos(NODE first, int pos)
{
	NODE newnode,temp,temp1;
	newnode=(NODE)malloc(sizeof(struct node));
	newnode->link=0;
	scanf("%d",&newnode->data);
	temp=first;
	for(int i=0;i<pos;i++)
	{
		temp1=temp;
		temp=temp->link;
	}
	temp1->link=newnode;
	newnode->link=temp;
	return(first);
}

NODE delete_pos(NODE first, int pos)
{
	NODE temp,temp1;
	temp=first;
	if((pos==1)&&(first->link==0))
	{
		printf("%d\n",temp->data);
		free(temp);
		first=NULL;
		return(first);
	}
	if(pos==1)
	{
		printf("%d\n",temp->data);
		first=first->link;
		free(temp);
		return(first);
	}
	for(int i=1;i<pos;i++)
	{
		temp1=temp;
		temp=temp->link;
	}
	printf("%d\n",temp->data);
	temp1->link=temp->link;
	free(temp);
	return(first);
}

NODE delete_front(NODE first)
{
	NODE temp;
	temp=first;
	if(temp->link==0)
	{
		printf("%d\n",temp->data);
		free(temp);
		first=0;
		return(first);
	}
	printf("%d\n",temp->data);
	first=first->link;
	free(temp);
	return(first);
}

void display(NODE first)
{
	NODE temp;
	temp=first;
	while(temp!=0)
	{
		printf("%d ",temp->data);
		temp=temp->link;
	}
	printf("\n");
}
>>>>>>> a31856866d97c0782ac69c9c3c38287607a974be
