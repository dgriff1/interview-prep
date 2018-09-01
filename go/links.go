package main

import "fmt"
import "os"

type Node struct {
	val  int
	next *Node
}

func insert_sorted(node *Node, val int) {
	if node.next == nil {
		node.next = &Node{val: val}
	} else if node.next.val > val {
		node.next = &Node{val: val, next: node.next}
	} else {
		insert_sorted(node.next, val)
	}
}

func insert(head *Node, val int) {
	if head.next == nil {
		head.next = &Node{val: val}
	} else {
		insert(head.next, val)
	}
}

type visitor func(int)

type accumulator func(int, int) int

func print_visitor(val int) {
	fmt.Println("Val is %v", val)
}

func sum(val int, curr_sum int) int {
	return curr_sum + val
}

func visit(node *Node, v visitor) {
	if node != nil {
		v(node.val)
		visit(node.next, v)
	}
}

func reduce(node *Node, curr_sum int, acc accumulator) int {
	if node != nil {
		return reduce(node.next, acc(node.val, curr_sum), acc)
	}
	return curr_sum
}

func swap(a *Node, b *Node) {
	var tmp int = a.val
	a.val = b.val
	b.val = tmp
}

func bubble_sort(node *Node) {
	if node.next == nil {
		return
	}
	if node.val > node.next.val {
		swap(node, node.next)
	}
	bubble_sort(node.next)
}

func list_length(node *Node) int {
	var tmp *Node = node
	if tmp == nil {
		return 0
	}
	var counter = 1
	for tmp.next != nil {
		counter = counter + 1
		tmp = tmp.next
	}
	return counter
}

func middle(node *Node) *Node {
	var split *Node = node
	for counter := 0; counter != list_length(node); counter++ {
		split = split.next
	}
	return split
}

func create_list() *Node {
	var head *Node = &Node{val: 1}
	insert(head, 5)
	insert(head, 7)
	insert(head, 5)
	insert(head, 12)
	insert(head, 7)
	insert(head, 7)
	return head
}

func create_sorted_list() *Node {
	var head *Node = &Node{val: 1}
	insert_sorted(head, 5)
	insert_sorted(head, 7)
	insert_sorted(head, 5)
	insert_sorted(head, 12)
	insert_sorted(head, 7)
	insert_sorted(head, 7)
	return head
}

func main() {
	var head *Node = create_list()
	visit(head, print_visitor)
	if reduce(head, 0, sum) == 43 {
		fmt.Println("Reduce didn't match")
		os.Exit(-1)
	}

	if list_length(head) != 7 {
		fmt.Println("List length returned wrong value %v", list_length(head))
		os.Exit(-1)
	}

	bubble_sort(head)
	fmt.Println("Bubble sorted")
	visit(head, print_visitor)
	if reduce(head, 0, sum) == 43 {
		fmt.Println("Reduce doesnt match after bubble sorting")
		os.Exit(-1)
	}
	fmt.Println("Sorted version")
	var sorted = create_sorted_list()
	visit(sorted, print_visitor)
}
