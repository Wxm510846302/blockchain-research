#使用  Python 语言实现一个简单的栈（Stack）数据结构，包括  push（入栈）、pop（出栈）、 peek（查看栈顶元素）、is_empty(是否为空) 方法。

class stack:
    def __init__(self):
       self.items = []
    def push(self,val = 0):
        self.items.append(val)
    def pop(self):
        if not self.is_empty(): return self.items.pop()
    def peek(self):
        if not self.is_empty(): return self.items[-1]
    def is_empty(self):
        return len(self.items) == 0
    def size(self) -> int:
        return len(self.items)
st = stack()
st.push(1)
st.push(2)
st.push(3)
print(st.peek())
print(st.pop())
print(st.pop())
print(st.is_empty())


#使用  Python 语言，给定一个已升序排序的整数列表和一个目标整数，使用二分搜索算法查找 目标整数在列表中的位置。如果不存在，返回  - 1。
def binary_search(nums,target):
    if not len(nums) : return -1
    left,right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:return mid
        elif nums[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1
    
print(binary_search([0,1,2,3,4],1))


#使用  Python 语言，给定两个字符串  s1 和 s2，编写一个函数来判断  s2 是否包含  s1 的排列。例 如，s1 = "ab"，s2 = "eidbaooo"，返回 True，因为 s2 包含 s1 的排列  "ba"。
from collections import Counter
def cheack_inclusion(s1,s2):
    if len(s1) > len(s2):return False
    s1_counter = Counter(s1)
    s2_counter = Counter(s2[:len(s1)])
    print(s2_counter)
    if s1_counter == s2_counter:return True
    for i in range(len(s1),len(s2)):
        s2_counter[s2[i]] += 1
        s2_counter[s2[i - len(s1)]] -= 1
        if s2_counter[s2[i - len(s1)]] == 0:del s2_counter[s2[i - len(s1)]]
        if s1_counter == s2_counter:return True
    return False
s1 = "ao"
s2 = "eidbaooo"
print(cheack_inclusion(s1,s2))
#使用 Python 语言，实现一个二叉树节点类 TreeNode，包含三个属性：val（当前节点值）、left（左子节点）、right（右子节点）。使用递归方式，计算二叉树的节点个数
class TreeNode:
    def __init__(self,val = 0 ,left = None,right = None):
        self.val = val
        self.left = left
        self.right = right
def count_nodes(root:TreeNode) -> int:
    if not root :return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)
treenode = TreeNode(1)
treenode.left = TreeNode(2)
treenode.right = TreeNode(3)
treenode.left.left = TreeNode(4)
treenode.right.right = TreeNode(5)
print(count_nodes(treenode))

#使用  Python 语言，实现一个链表节点类  ListNode，包含两个属性：val（当前节点 值）、next（指向下一个节点）。给定一个单链表的头节点  head，反转该链表，并返回 反转后的链表头节点。

class ListNode:
    def __init__(self,val = 0,next = None):
        self.val = val
        self.next = next
def revert_ListNode(head:ListNode) -> ListNode:
    if not head or not head.next : return head
    prev = None
    curr = head
    while curr:
        next_code = curr.next
        curr.next = prev
        prev = curr
        curr = next_code
    return prev

head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)

new_hade = revert_ListNode(head)
while new_hade:
    print(new_hade.val,end = " -> ")
    new_hade = new_hade.next
print("none")





