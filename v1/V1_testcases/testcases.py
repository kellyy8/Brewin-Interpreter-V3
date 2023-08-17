# from spec
test_statement =['print', '1', '"here\'s a result "', ['*', '3', '5'], '" and here\'s a boolean"', 'true', '" "', ['+', '"race"', '"car"']]
test_statement = ['begin', ['print', '"hello "', ['*', '3', '5']], ['print', '"world"'], ['print', '"goodbye"']]

# test if all valid operations work for integer operands 9
# output: 9 3 18 1 0 false true true false true false 
test_statement = [['print', ['+', '6', '3']],
                  ['print', ['-', '6', '3']],
                  ['print', ['*', '6', '3']],
                  ['print', ['/', '6', '5']],
                  ['print', ['%', '6', '3']],
                  ['print', ['==', '6', '3']],
                  ['print', ['!=', '6', '3']],
                  ['print', ['>', '6', '3']],
                  ['print', ['<', '6', '3']],
                  ['print', ['>=', '6', '3']],
                  ['print', ['<=', '6', '3']]]

# test if all valid operations work on string operands
# output: ab false true false true false true
test_statement = [['print', ['+', '"a"', '"b"']],
                  ['print', ['==', '"a"', '"b"']],
                  ['print', ['!=', '"a"', '"b"']],
                  ['print', ['>', '"a"', '"b"']],
                  ['print', ['<', '"a"', '"b"']],
                  ['print', ['>=', '"a"', '"b"']],
                  ['print', ['<=', '"a"', '"b"']]]

# test if all valid operations work on boolean operands
# output: true false false true
test_statement = [['print', ['==', 'true', 'true']],
                  ['print', ['!=', 'true', 'true']],
                  ['print', ['&', 'true', 'false']],
                  ['print', ['|', 'true', 'false']]]

# test if all valid operations work on null operand
# output: false true
test_statement = [['print', ['==', 'null', 'true']],
                  ['print', ['!=', 'null', 'true']]]

# catch incompatible types for '+'
test_statement = ['print', ['+', '"a"', '1']]
test_statement = ['print', ['+', '1', '"b"']]
test_statement = ['print', ['+', 'true', 'null']]
test_statement = ['print', ['+', 'null', 'false']]
test_statement = ['print', ['+', '1', 'false']]
test_statement = ['print', ['+', '1', 'null']]
test_statement = ['print', ['+', '"a"', 'false']]
test_statement = ['print', ['+', '"a"', 'null']]

# catch incompatible types for math operations
test_statement = ['print', ['-', '"a"', '1']]
test_statement = ['print', ['*', '1', '"b"']]
test_statement = ['print', ['/', 'true', 'null']]
test_statement = ['print', ['%', 'null', 'false']]
test_statement = ['print', ['-', '1', 'false']]
test_statement = ['print', ['*', '1', 'null']]
test_statement = ['print', ['/', '"a"', 'false']]
test_statement = ['print', ['%', '"a"', 'null']]

# catch incompatible types for comparison operands
test_statement = ['print', ['&', '"a"', '1']]
test_statement = ['print', ['&', 'true', 'null']]
test_statement = ['print', ['|', '1', '"b"']]
test_statement = ['print', ['|', 'null', 'false']]
test_statement = ['print', ['>', '1', 'false']]
test_statement = ['print', ['>', '1', 'null']]
test_statement = ['print', ['<', '"a"', 'false']]
test_statement = ['print', ['<', '"a"', 'null']]
test_statement = ['print', ['>=', '"a"', '1']]
test_statement = ['print', ['>=', '1', '"b"']]
test_statement = ['print', ['<=', 'true', 'null']]
test_statement = ['print', ['<=', 'null', 'false']]
test_statement = ['print', ['==', '1', 'false']]
test_statement = ['print', ['==', 'false', '"a"']]
test_statement = ['print', ['!=', '"a"', 'false']]
test_statement = ['print', ['!=', '1', 'false']]

# catch incompatible types for nested NOT operation
test_statement = ['print', ['!', ['==', '3', '5']]]

# run if-body (single line)
test_statement = ['if', ['==', '0', ['%', '4', '2']], ['print', '"x is even"'], ['print', '"x is odd"']]
# run else-body (single line)
test_statement = ['if', ['==', '0', ['%', '5', '2']], ['print', '"x is even"'], ['print', '"x is odd"']]
# catch error: condition != boolean type
test_statement = ['if', ['+', '0', ['%', '5', '2']], ['print', '"x is even"'], ['print', '"x is odd"']]
# condition is boolean constant
test_statement = ['if', 'true', ['print', '"that\'s true"'], ['print', '"this won\'t print"']]
# run if-body (multi-line) (nested with begin's)
test_statement = ['if', ['==', '0', ['%', '4', '2']], ['begin', ['print', '"one line"'], ['print', '"two line"']], ['begin', ['print', '"no line"'], ['print', '"still no line"']]]
# run else-body (multi-line) (nested with begin's)
test_statement = ['if', ['==', '0', ['%', '5', '2']], ['begin', ['print', '"one line"'], ['print', '"two line"']], ['begin', ['print', '"no line"'], ['print', '"still no line"']]]
# run nested if-else statement inside if-body
test_statement = ['if', ['!=', '"a"', '"b"'], ['if', ['==', '1', '1'], ['print', '"nested if"']]]
# run nested if-else statement inside  & else-body
test_statement = ['if', ['!=', '"a"', '"b"'], ['if', ['==', '1', '1'], ['print', '"nested if in if-body"']], ['if', ['==', '1', '1'], ['print', '"nested if in else-body"']]]
test_statement = ['if', ['==', '"a"', '"b"'], ['if', ['==', '1', '1'], ['print', '"nested if in if-body"']], ['if', ['==', '1', '1'], ['print', '"nested if in else-body"']]]

# run single begin statements:
test_statement = ['begin', ['print', '"hello "', ['*', '3', '5']], ['print', '"world"'], ['print', '"goodbye"']] # from spec
# run nested begin statements:
test_statement = ['begin', ['begin', ['print', '"one line"'], ['print', '"two line"']]]
# begin nested with if statements:
test_statement = ['begin', ['if', ['==', '0', ['%', '4', '2']], ['print', '"x is even"'], ['print', '"x is odd"']]]

# return ==> [return expression] returns value to 'call expression'
(class main
        (method main ()
         (print "five = " (call me foo))
        )
        (method foo ()
          (return 5)
        )
)

# call expression ==> call function that does not exist returns NAME_ERROR
(class main
        (method main ()
         (print "created a cow " (call me zebra))
        )
)
(class cow
  (field sound "moo")
  (method sleep() (print "snoring"))
)

# RANDOM ----------------------------------------------------------------------------------------
(class main
    (method main ()
        (print "hello world!")))

(class main
   (method main ()
       (print (== 21 (+ (* 3 5) 6)))))

(class main
    (method main ()
        (print (+ (+ "a" "b") "c"))))

# if/if-else 
(class main
        (field x 0)
        (method main () 
          (begin
           (if (== 0 (% 5 2))
             (begin
               (print "one line")
               (print "two line")
             )
             (begin
               (print "no line")
               (print "still no line")
             )
           )       
           (if (== 4 7) 
             (print "lucky seven")  # no else clause in this version
           )    
          )
  )
)

# if ==> nested if statement in if body
(class main
        (field x 0)
        (method main () 
          (if (!= "a" "b")
             (if (== 1 1)
               (print "nested if")
             )
          )
  )
)

# if ==> nested if statement in if body and else body
(class main
        (field x 0)
        (method main () 
          (if (== "a" "b")
             (if (== 1 1)
               (print "nested if in if-body")
             )
             (if (== 1 1)
               (print "nested if in else-body")
             )
          )
        )
)


# CALL ==> method owned by object with no params
(class main
        (field x 0)
        (method main () 
          (call me foo)
        )
        (method foo ()
          (print "called foo! no params")
        )
)

# CALL ==> method owned by object with params (not using params)
(class main
        (field x 0)
        (method main () 
          (call me foo 1)
        )
        (method foo (n)
          (print "foo requires 1 parameter")
        )
)

# CALL ==> method owned by object with params (wrong number of args)
(class main
        (field x 0)
        (method main () 
          (call me foo 1 2)
        )
        (method foo (n)
          (print "foo requires 1 parameter")
        )
)

# CALL ==> initializing & using parameter variables
(class main
        (field x 0)
        (method main ()
          (begin (call me foo 1 ))
        )
        (method foo (n)
          (print "passed " n " into foo")
        )
)


# MAY 7, 2023 NEW TEST CASES HAHA----------------------------------------------------------------------------------------

# print ==> prints fields, int, bool, str constants, and int, bool, str expressions
(class main
    (field x "A")
    (method main ()
     (begin (print x) (print 1) (print "a")(print true) (print (* 3 5)) (print (== "A" "A")) (print (+ "a" "b")))
    )
)

# print ==> prints parameters
(class main
    (method main () (call me sleep "1AM"))
    (method sleep (time) (print time))
)

# inputi ==> stores int value into var
(class main
        (field x 0)
        (method main () 
          (begin
           (inputi x)	# input value from user, store in x variable
           (print "the user typed in " x)
          )
  )
)

# inputs ==> stores string value into var

(class main
        (field x 0)
        (method main () 
          (begin
           (inputs x)	# input value from user, store in x variable
           (print "the user typed in " x)
          )
  )
)

# while ==> from spec, it works successfully (dependent on 'set' and 'inputi' working)
(class main
        (field x 0)
        (method main () 
          (begin
           (inputi x)	 
           (while (> x 0) (begin (print "x is " x) (set x (- x 1))))          
          )
  )
)

# set = updates an existing variable in given scope with a const; using eval_expr()
(class main
    (field x 0)
    (method main () (set x 1))
)

# set = name error, nonexistent variable in given scope
(class main
    (field x 0)
    (method main () (set y 1))
)

# set = from spec
(class main
        (field x 0)
        (method foo (q)
          (begin
            (set q true)			# setting parameter to boolean constant 	
            (print q) 
            (set x "foobar")		# setting field to a string constant	
            (print x)
            (set x 10)	 		# setting field to integer constant
            (print x)
            (set x (* x 5))		# setting field to result of expression
            (print x)
            (set x null)			# setting field to null	 
            (set x (new person))	# setting field to refer to new object
          )
        )
        (method main () 
          (call me foo 5)
  )
)
(class person
   (field name "")
   (field age 0)
   (method init (n a) (begin (set name n) (set age a)))
   (method talk (to_whom) (print name " says hello to " to_whom))
)


# RETURN STATEMENT TESTING ---------------------------------------------------------------------------------------------
# RETURN --> JUST RETURN STATEMENT (top level statement) (no nesting) -- 15
(class main
    (method foo (q) 
        (return (* 3 q)))   # returns the value of 3*q
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN --> NEST RETURN INSIDE 1 STATEMENT WHERE RETURN IS NOT LAST -- 15
(class main
    (method foo (q) 
        (begin (return (* 3 q)) (print "don't pring this" ))
    )
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN -- NEST RETURN INSIDE 1 STATEMENT WHERE RETURN IS LAST (BEGIN) -- pring this, 15
(class main
    (method foo (q) 
        (begin  (print "pring this" ) (return (* 3 q)))
    )
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN -- NEST RETURN INSIDE 1 STATEMENT WHERE RETURN IS LAST (IF) -- 15
(class main
    (method foo (q) 
        (if (== 5 5)
            (return (* 3 q))
        )
    )
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN --> NESTED RETURN INSIDE (2+) STATEMENTS WHERE STATEMENT W RETURN IS LAST -- pring this, 15
(class main
    (method foo (q) 
        (if (== 5 5)
            (begin (print "pring this" ) (return (* 3 q)))
            # NOTHING HERE AFTER INNER STATEMENT ENDS
        )
    )
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN --> NESTED RETURN INSIDE (2+) STATEMENTS WHERE STATEMENT W RETURN IS NOT LAST (FROM SPEC)
# RETURN --> NESTED WHILE-IF STATEMENTS WHERE STATEMENT W RETURN IS
# PREVIOUSLY: not terminating, after running print statement, the return value is '' which means no return value
#             but this is a call expression, will have issue in print (call me foo 5) since printing ''
(class main
    (method foo (q) 
        (while (> q 0)
            (if (== (% q 3) 0)
                (return "SUCCESS")  # immediately terminates loop and function foo
                (set q (- q 1))
            )
            # SOMEETHINGG HERE THAT LOOP COULD CONTINUE WITH AFTER INNER STATEMENT ENDS
        )  
    )
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN --> NESTED BEGIN-BEGIN STATEMENTS WHERE STATEMENT W RETURN IS NOT LAST -- 15
(class main
    (method foo (q) 
        (begin
            (begin (return (* 3 q)))
            (print "don't print this" )     #SOMETHING AFTER INNER BEGIN TERMINATES
        )
    )
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN --> NESTED BEGIN-IF STATEMENTS WHERE STATEMENT W RETURN IS NOT LAST -- 15
(class main
    (method foo (q) 
        (begin
            (if (== 4 4) (return (* 3 q)))
            (print "don't print this" )     #SOMETHING AFTER INNER IF TERMINATES
        )
    )
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN --> NESTED IF-BEGIN-IF STATEMENTS WHERE STATEMENT W RETURN IS NOT LAST -- 5
(class main
    (method foo (q) 
        (if (> q 0)
            (begin
                (if (!= (% q 3) 0) (return q))
                (print "don;t prin this")
            )
        )  
    )
    (method main () 
        (print (call me foo 5))
    )
)

# RETURN --> NESTED CALL-CALL STATEMENTS WHERE STATEMENT W RETURN IS LAST -- 125
(class main
    (method foo (q) 
        (return (* q 5))            # NOTHING AFTER THIS LINE
    )
    (method main () 
        (print (call me foo (call me foo 5)))
    )
)

# RETURN --> NESTED BEGIN-WHILE STATEMENTS WHERE STATEMENT W RETURN IS
# RETURN --> NESTED WHILE-BEGIN STATEMENTS WHERE STATEMENT W RETURN IS
# RETURN --> NESTED WHILE-WHILE STATEMENTS WHERE STATEMENT W RETURN IS
# RETURN --> NESTED IF-WHILE STATEMENTS WHERE STATEMENT W RETURN IS

# RETURN --> NO RETURN VALUE
(class main
         (method foo (q) 
           (while (> q 0)
               (if (== (% q 3) 0)
                 (return)  # immediately terminates loop and function foo
                 (begin (print q) (set q (- q 1))) # q:5 ==> prints out 5 and 4
               )
           )  
         )
         (method main () 
           (call me foo 5)
         )
)

# CALL STATEMENT TESTING ---------------------------------------------------------------------------------------------
# ONE function call -- all statements in function call have access to fields and params (no shadowing)
(class main
    (field x 0)
    (method main () (call me sleep 1))
    (method sleep (time) (begin (print "snoring") (print "still snoring")))
)

# ONE function call -- all statements in function call have access to fields and params (with shadowing) (param shadow fields)
(class main
    (field x 0)
    (method main () (call me sleep 1 2))
    (method sleep (time, x) (begin (print "snoring") (print "still snoring")))
)

# ONE function call -- 2+ levels deep; second call only sees fields & its own parameters (curr call's params shadow parent call's params)
# update's to second call's parameters should not affect first call's parameters

# i forgot ... something with updating the field value from a nested call expression??
(class main
  (field q 0)
         (method foo ()
           (return (* 3 5))
         )
         (method main () 
           (begin (print q) (set q (call me foo)) (print q))
         )
)

# CALL -- can have expressions as arguments
(class main
  (field q 0)
         (method foo (n)
           (print n)
         )
         (method main () 
           (call me foo (* 3 5))
         )
)

# CALL -- can have variables as arguments
(class main
  (field q 10)
         (method foo (n)
           (print n)
         )
         (method main () 
           (call me foo q)
         )
)

# CALL -- from spec; object call's another object's methods
# output:
# Hey Leia, knock knock!
# Siddarth says hello to Boyan
# Siddarth's age is 25
(class person
   (field name "")
   (field age 0)
   (method init (n a) (begin (set name n) (set age a)))
   (method talk (to_whom) (print name " says hello to " to_whom))
   (method get_age () (return age))
)

(class main
 (field p null)
 (method tell_joke (to_whom) (print "Hey " to_whom ", knock knock!"))
 (method main ()
   (begin
      (call me tell_joke "Leia")  # calling method in the current obj
      (set p (new person))    
      (call p init "Siddarth" 25)  # calling method in other object
      (call p talk "Boyan")        # calling method in other object
      (print "Siddarth's age is " (call p get_age))
   )
 )
)

# PASS BY VALUE -- objects have individual fields (prints 1 and 2)
(class object
  (field num 1)
  (method change (n)
    (set num n)
  )
  (method show () (print num))
)

(class main
  (field o1 null)
  (field o2 null)
  (method main ()
    (begin 
      (set o1 (new object))
      (set o2 (new object))
      (call o2 change 2)
      (call o1 show)
      (call o2 show)
    )
  )
)

# RETURN STATEMENT :)
# CONSECUTIVE IF'S -- all if statements should be ran (from spec)
(class main
        (field x 0)
        (method main () 
          (begin
           (inputi x)	# input value from user, store in x variable
           (if (== 0 (% x 2)) 
             (print "x is even")
             (print "x is odd")   # else clause
           )       
           (if (== x 7) 
             (print "lucky seven")  # no else clause in this version
           )  
           (if true (print "that's true") (print "this won't print"))    
          )
  )
)

# NESTED IF'S -- value should be propagated up & return terminates function foo -- 5
(class main
  (method foo ()
    (if (== 1 1)
      (if (== 1 1)
      (begin (return 5) (print "dont print this"))
      )
    )
   )
  (method main ()
    (print (call me foo))
  )
)

# CONSECUTIVE WHILE's
(class main
        (field x 0)
        (method main () 
          (begin
           (inputi x)	 
           (print "round 1:")
           (while (> x 0) (begin (print "x is " x) (set x (- x 1))))
           (inputi x)
           (print "round 2:")
           (while (> x 0) (begin (print "x is " x) (set x (- x 1))))          
          )
  )
)

# ^ ADD IN RETURN

# CONSECUTIVE BEGIN's
(class main
        (field x 0)
        (method main () 
          (begin
           (begin (print "first begin"))         
           (begin (print "second begin"))
          )
  )
)

# NESTED CALL'S -- 125
(class main
    (method foo (q) 
        (return (* q 5))            # NOTHING AFTER THIS LINE
    )
    (method main () 
        (print (call me foo (call me foo 5)))
    )
)

# ^ CHECK TERMINATION -- 125
(class main
    (method bar () (print "dont print this omg"))
    (method foo (q) 
        (begin (return (* q 5)) (call me bar))
    )
    (method main () 
        (print (call me foo (call me foo 5)))
    )
)

# CONSECUTIVE CALL's
# calling foo
# calling foo
(class main
  (field x 0)
  (method main () 
    (begin
      (call me foo)
      (call me foo)
    )
  )
  (method foo ()
    (print "calling foo") 
  )
)

# NESTED BEGIN'S
# round 1:
# calling foo
# round 2:
# calling foo
(class main
  (field x 0)
  (method main () 
    (begin
      (print "round 1:")
      (call me foo)
      (begin
        (print "round 2:")
        (call me foo)
      )
    )
  )
  (method foo ()
    (print "calling foo") 
  )
)

# ^ ADD RETURN
# round 1:
# calling foo
# round 2:
# no second round
(class main
  (field x 0)
  (method bar () 
    (begin
      (print "round 1:")
      (call me foo)
      (begin
        (print "round 2:")
        (return "no second round")
        (call me foo)
      )
    )
  )
  (method foo ()
    (print "calling foo") 
  )
  (method main () (print (call me bar)))
)

# NESTED WHILE'S
(class main
        (field x 0)
        (field y 0)
        (method main () 
          (begin
           (inputi x) (inputi y) 
           (while (> x 0)
            (begin
             (while (> y 0) (begin (print "y is " y) (set y (- y 1))))
             (print "x is " x)
             (set x (- x 1))
            )
           )    
          )
  )
)

# ^ ADD RETURN
(class main
        (field x 0)
        (field y 0)
        (method foo () 
          (begin
           (inputi x) (inputi y) 
           (while (> x 0)
            (begin
             (while (> y 0) (begin (print "y is " y) (set y (- y 1)) (if (== y 0) (return y))))
             (print "x is " x)
             (set x (- x 1))
            )
           )    
          )
  )
  (method main () (print (call me foo)))
)

# while-if with return
(class main
  (field x 0)
  (field y 0)
  (method foo () 
    (begin
      (inputi x)
      (inputi y)
      (while (> x 0)
      (begin 
        (if (> y 0) (begin (print "y is " y) (set y (- y 1))) (return y))
        (print "x is " x)
        (set x (- x 1))
        
        )
      )
    )
  )
 (method main () (print (call me foo)))
)

# factorial from spec
# Our first Brewin program!
(class main
 # private member fields
 (field num 0)
 (field result 1)

 # public methods
 (method main ()
 (begin
 (print "Enter a number: ")
   (inputi num)
    (print num " factorial is " (call me factorial num))
  )
  )
 (method factorial (n)
  (begin
   (set result 1)
   (while (> n 0)
    (begin
     (set result (* n result))
     (set n (- n 1))
    )
   )
   (return result)
  )
 )
)

