package main

import (
	"fmt"
)

func arrondiAuMutilple(x int, a int) int {
	return ((x + a/2) / a) * a
}

func recalculPrix(prix int) map[string]int {
	if prix < 30 {
		return map[string]int{
			"Exté":      arrondiAuMutilple(prix, 5) + 20,
			"CETEN":     arrondiAuMutilple(prix, 5) + 10,
			"Staff":     arrondiAuMutilple(prix, 5) + 5,
			"Privilège": arrondiAuMutilple(prix, 5) + 5,
			"Menu":      arrondiAuMutilple(prix, 5) + 10,
		}
	} else if prix >= 30 && prix < 130 {
		return map[string]int{
			"Exté":      arrondiAuMutilple(prix*15/10, 5),
			"CETEN":     arrondiAuMutilple(prix*13/10, 5),
			"Staff":     arrondiAuMutilple(prix*108/100, 5),
			"Privilège": arrondiAuMutilple(prix*11/10, 5),
			"Menu":      arrondiAuMutilple(prix*13/10, 5),
		}
	} else if prix >= 130 && prix <= 300 {
		return map[string]int{
			"Exté":      arrondiAuMutilple(prix*14/10, 5),
			"CETEN":     arrondiAuMutilple(prix*11/10, 5),
			"Staff":     arrondiAuMutilple(prix*108/100, 5),
			"Privilège": arrondiAuMutilple(prix*11/10, 5),
			"Menu":      arrondiAuMutilple(prix*12/10, 5),
		}
	} else if prix >= 300 {
		return map[string]int{
			"Exté":      arrondiAuMutilple(prix*125/100, 5),
			"CETEN":     arrondiAuMutilple(prix*11/10, 5),
			"Staff":     arrondiAuMutilple(prix*105/100, 5),
			"Privilège": arrondiAuMutilple(prix*11/10, 5),
			"Menu":      arrondiAuMutilple(prix*1125/1000, 5),
		}
	}
	return nil
}

func main() {
	fmt.Println(arrondiAuMutilple(20, 5))
	fmt.Println(recalculPrix(23))
	fmt.Println(recalculPrix(30))
	fmt.Println(recalculPrix(200))
	fmt.Println(recalculPrix(501))
}