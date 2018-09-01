package main

import "fmt"
import "os"
import "reflect"

func partition(ints []int) int {
	return len(ints) / 2
}

func quicksort(ints []int, start int, end int) {
	if start < end {
		var p = qpartition(ints, start, end)
		quicksort(ints, start, p)
		quicksort(ints, p+1, end)
	}
}

func qpartition(ints []int, start int, end int) int {
	var pivot = ints[start]
	var i = start
	var j = end
	for {
		for ints[i] < pivot {
			i++
		}
		for ints[j] > pivot {
			j = j - 1
		}

		if i >= j {
			return j
		}
		var tmp = ints[i]
		ints[i] = ints[j]
		ints[j] = tmp
		i++ // force iteration to next index
		j--
	}
}

func bubblesort(ints []int) {
	for i := 0; i < len(ints); i++ {
		for j := 1; j < len(ints); j++ {
			if ints[j-1] > ints[j] {
				var tmp int = ints[j-1]
				ints[j-1] = ints[j]
				ints[j] = tmp
			}
		}
	}
}

func main() {
	var unsorted = []int{4, 3, 2, 1, 9, 10, 23, 2}
	var sorted = []int{1, 2, 2, 3, 4, 9, 10, 23}

	bubblesort(unsorted)
	if !reflect.DeepEqual(unsorted, sorted) {
		fmt.Println("Did not sort correctly %v ", unsorted)
		os.Exit(-1)
	}

	unsorted = []int{4, 3, 2, 1, 9, 10, 23, 2}
	fmt.Println("Sorting %v ", unsorted)
	quicksort(unsorted, 0, len(unsorted)-1)
	if !reflect.DeepEqual(unsorted, sorted) {
		fmt.Println("Did not sort correctly %v ", unsorted)
		os.Exit(-1)
	}

	unsorted = []int{4, 3, 12, 9, 9, 10, 23, 2}
	sorted = []int{2, 3, 4, 9, 9, 10, 12, 23}
	fmt.Println("Sorting %v ", unsorted)
	quicksort(unsorted, 0, len(unsorted)-1)
	if !reflect.DeepEqual(unsorted, sorted) {
		fmt.Println("Did not sort correctly %v ", unsorted)
		os.Exit(-1)
	}

}
