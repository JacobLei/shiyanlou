#include <stdio.h>

struct ListNode
{
    int value;
    ListNode *next;
    ListNode(int x) : value(x), next(NULL)
    {
    }  
};

class Solution
{
    public:
        ListNode* reverseList(ListNode* head)
        {
            ListNode* new_head = NULL;
            while( head )
            {
                ListNode* head_next = head->next;   // 备份head->next
                head->next = new_head;      // 更新head->next
                new_head = head;            // 移动new->head
                head = head_next;
            }
            return new_head;      
        }

};

int main()
{
    ListNode a(1);
    ListNode b(2);
    ListNode c(3);
    ListNode d(4);
    ListNode e(5);

    a.next = &b;
    b.next = &c;
    c.next = &d;
    d.next = &e;
   
    Solution solve; 
    ListNode *head = &a;

    printf(" before change...\n");

    while(head)
    {
        printf("%d\n", head->value);
        head = head->next;
    }    
    
    printf(" after change...\n");

    head = solve.reverseList(&a);

	while(head)
    {
        printf("%d\n", head->value);
        head = head->next;
    } 
    
    return 0;
}
