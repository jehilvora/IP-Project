#include<stdio.h>
#include<stdlib.h>

struct node
{
	int data;
	struct node *lchild;
	struct node *rchild;
};

typedef struct node *NODE;
int i=1,num,req;

void insert(NODE*,int) ;
void preorder(NODE);
void inorder(NODE);
void postorder(NODE);

int main()
{
	NODE root=0;
	scanf("%d",&req);
	while(req--)
	{
		scanf("%d",&num);
		insert(&root,num);
	}
	preorder(root);
	printf("\n");
	inorder(root);
	printf("\n");
	postorder(root);
	return 0;
}
void insert(NODE *(root1),int num)
{
	if((*root1)==0)
	{
		(*root1)=(NODE)malloc(sizeof(struct node));
		(*root1)->lchild=(*root1)->rchild=0;
		(*root1)->data=num;
	}
	else
	{
		if(num<((*root1)->data))
			insert(&((*root1)->lchild),num);
		else
			insert(&((*root1)->rchild),num);
	}
	return;
}

void preorder(NODE root4)
{
	if(root4!=0)
	{
		printf("%d ",root4->data);
		preorder(root4->lchild);
		preorder(root4->rchild);
	}
}
void inorder(NODE root5)
{
	if(root5!=0)
	{
		inorder(root5->lchild);
		printf("%d ",root5->data);
		inorder(root5->rchild);
	}
}
void postorder(NODE root6)
{
	if(root6!=0)
	{
		postorder(root6->lchild);
		postorder(root6->rchild);
		printf("%d ",root6->data);
	}
}

