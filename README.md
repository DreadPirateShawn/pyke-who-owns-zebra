pyke-who-owns-zebra
===================

A solution to the "Who owns the zebra?" puzzle in Python's Pyke module.

Who owns the zebra?
-------------------

["Who owns the zebra?"](http://en.wikipedia.org/wiki/Zebra_Puzzle) is a well-known logic puzzle. Basically, "There are 5 houses, one nationality lives in each, each has a different pet, etc. In the red house, the Swede drinks coffee. So who owns the zebra?"


Requirements
------------

* Python 2.7.5 is confirmed to work
* python-pyke is the knowledge engine
* python-texttable is used for easy debugging visualization


    apt-get install python python-pyke python-texttable


Contains
--------
* `clues.kfb` ~ Contains the baseline facts provided by the puzzle.
* `relations.krb` ~ Contains forward-chaining rules to derive additional facts.
* `driver.py` ~ Runs the test.


Sample Output
-------------

```
$ python driver.py 

== Who owns the zebra? German ==

#   Color    Nationality    Pet    Drink       Smoke    
=======================================================
1   yellow   Norwegian     cats    water    Dunhill     
2   blue     Dane          horse   tea      Blend       
3   red      English       birds   milk     Pall Mall   
4   green    German        zebra   coffee   Prince      
5   white    Swede         dog     beer     Blue Master 

Calculated in 1.21 seconds.
```


General Logic
-------------

The logic here is to create the constraints driven by two core concepts:
* exclusive relationships ~ "if nationality X has pet Y, then no other nationality has pet Y"
* spatial relationships ~ "there are 5 houses next to each other"

I've seen this done with Python's "constraint" module (http://stackoverflow.com/a/320981/128977) but I wanted to see what it takes to recreate the same logic in Pyke.

For instance, where the "constraint" module has AllDifferentConstraint, this solution creates two custom rules `if_one_related_then_others_unrelated` and `if_four_unrelated_then_remaining_is_related`.

All done and said, 14 rules are used for this solution:

| Type | Rules | Examples |
| :--- | :---- | :------- |
| definitional | categories | asserts the primitive categories, eg "is_category(DRINK, coffee)"
| inverse | inverse_relationship_positive<br>inverse_relationship_negative<br>inverse_relationship_beside | "if the Swede has a horse, then the horse is owned by the Swede" |
| transitive | transitive_positive<br>transitive_negative | eg "if the Swede has a horse and the horse is in the red house, then the Swede is in the red house" |
| exclusive | if_one_related_then_others_unrelated<br>if_four_unrelated_then_other_is_related | eg "if the Swede has a horse, then the Dane does not" |
| neighbors (basic) | expanded_relationship_beside_left<br>unrelated_to_beside | basic neighbor logic, eg "if the Swede lives next to the cats, then the Swede does not have cats" |
| neighbors (spatial) | check_next_to_either_edge<br>check_too_close_to_edge<br>check_next_to_with_other_side_impossible<br>left_of_and_only_two_slots_remaining | complex neighbor logic, eg "if the Swede is not in house #2 and cats are not in house #2, and the Swede lives next to cats, then neither Swede nor cats can be in house #1" |

