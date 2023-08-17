# from spec -- DEFAULT VALUES; output ==> quack\nhello
(class Dog
  (method void foo () (print ""))
)

(class main
 (field Dog e)
 (method void main ()
  (let ((bool b) (string c) (int d))
    (print b)  # prints False
    (print c)  # prints empty string
    (print d)  # prints 0
    (if (!= e null) (print "value") (print "null")) # prints null
  )
 )
)


# Check that default values work for fields and local variables.
(class main
    (field bool f)
    (method void main() 
        (let ((int x) (string s))
            (print x)
            (print f)
            (print s)
        )
    )
)

# from barista / spec ==> returns 5
(tclass node (field_type)
    (field node@field_type next null)
    (field field_type value)
    (method void set_val ((field_type v)) (set value v))
    (method field_type get_val () (return value))
    (method void set_next((node@field_type n)) (set next n))
    (method node@field_type get_next() (return next))
  )

  (class main
    (method void main ()
      (let ((node@int x null))
        (set x (new node@int))
        (call x set_val 5)
        (print (call x get_val))
      )
    )
  )

# from spec -- class templates example ==> output: Shape's area: 100/nAnimal's name: koda
(class Square
  (field int side 10)
  (method int get_area () (return (* side side)))
)

(class Dog
  (field string name "koda")
  (method string get_name () (return name))
)

(tclass MyTemplatedClass (shape_type animal_type)
    (field shape_type some_shape)
    (field animal_type some_animal)
    (method void act ((shape_type s) (animal_type a))
        (begin
        (print "Shape's area: " (call s get_area))
        (print "Animal's name: " (call a get_name))
        )
    ) 
)

(class main
  (method void main ()
    (let ((Square s) (Dog d) (MyTemplatedClass@Square@Dog t))
      (set s (new Square))
      (set d (new Dog))
      (set t (new MyTemplatedClass@Square@Dog))
      (call t act s d)
    )
  )
)

# Parameters can be of parameterized types == foo()
# New object instantations and method return types can be parameterized types == bar()
(class Square
  (field int side 10)
  (method int get_area () (return (* side side)))
)

(class Dog
  (field string name "koda")
  (method string get_name () (return name))
)

(tclass MyTemplatedClass (shape_type animal_type)
    (field shape_type some_shape)
    (field animal_type some_animal)
    (method void act ((shape_type s) (animal_type a))
        (begin
        (print "Shape's area: " (call s get_area))
        (print "Animal's name: " (call a get_name))
        )
    ) 
)

(class main
    (method void main()
        (call me bar)
    )

    (method void foo ((MyTemplatedClass@Square@Dog x))
        (print "hello world")
    )

    (method MyTemplatedClass@Square@Dog bar ()
        (return (new MyTemplatedClass@Square@Dog)) 
    )
)

# Type mismatch between parameterized types == TYPE ERROR(class Square
(class Square
  (field int side 10)
  (method int get_area () (return (* side side)))
)

(class Dog
  (field string name "koda")
  (method string get_name () (return name))
)

(class Cat
  (field string name "yoda")
  (method string get_name () (return name))
)

(tclass MyTemplatedClass (shape_type animal_type)
    (field shape_type some_shape)
    (field animal_type some_animal)
    (method void act ((shape_type s) (animal_type a))
        (begin
        (print "Shape's area: " (call s get_area))
        (print "Animal's name: " (call a get_name))
        )
    ) 
)

(class main
    (field MyTemplatedClass@Square@Dog x null)
    (method void main()
        (set x (new MyTemplatedClass@Square@Cat))
    )
)

# Comparing mismatched parameterized types:
(class Square
  (field int side 10)
  (method int get_area () (return (* side side)))
)

(class Dog
  (field string name "koda")
  (method string get_name () (return name))
)

(class Cat
  (field string name "yoda")
  (method string get_name () (return name))
)

(tclass MyTemplatedClass (shape_type animal_type)
    (field shape_type some_shape)
    (field animal_type some_animal)
    (method void act ((shape_type s) (animal_type a))
        (begin
        (print "Shape's area: " (call s get_area))
        (print "Animal's name: " (call a get_name))
        )
    ) 
)

(class main
    (field MyTemplatedClass@Square@Dog d null)
    (field MyTemplatedClass@Square@Cat c null)
    (method void main()
        (begin
            (set d (new MyTemplatedClass@Square@Dog))
            (set c (new MyTemplatedClass@Square@Cat))
            (print (== d c))
        )
    )
)

# NAME ERROR -- accessing exception variable outside of catch statement's scope
(class main
 (method void foo ()
   (while true
     (begin
       (print "argh")
       (throw "blah")
       (print "yay!")
     )
   )
 )

 (method void bar ()
  (begin
     (print "hello")
     (call me foo)
     (print "bye")
  )
 )

 (method void main ()
    (begin
      (try
       (call me bar)
       (print "The thrown exception was: " exception)
      )
      (print "This should fail: " exception)  # fails with NAME_ERROR
    )
  )

)

# from spec -- vaild access of exception variable (in-scope)
(class main
  (method void bar ()
     (begin
        (print "hi")
        (throw "foo")
        (print "bye")
     )
  )
  (method void main ()
    (begin
      (try
       (call me bar)
       (print "The thrown exception was: " exception)
      )
      (print "done!")
    )
  )
)

# nested statements inside try and catch blocks are valid
# begin
(class main
  (method void bar ()
     (begin
        (print "hi")
        (throw "foo")
        (print "bye")
     )
  )
  (method void main ()
    (begin
      (try
       (begin
            (print "try line")
            (call me bar)
        )
       (begin
            (print "catch line")
        (print "The thrown exception was: " exception)
       )
      )
      (print "done!")
    )
  )
)

# let
(class main
  (method void bar ()
     (begin
        (print "hi")
        (throw "foo")
        (print "bye")
     )
  )
  (method void main ()
    (begin
      (try
       (let ((int x 1))
            (print "try line" x)
            (call me bar)
        )
       (let ((int x 2))
            (print "catch line" x)
        (print "The thrown exception was: " exception)
       )
      )
      (print "done!")
    )
  )
)

# use debugger -- return value of 'foo' should be None due to early termination (TODO: check if this is correct)
# "miss me" is not printed, since early termination due to uncaught throw (this is correct)
# #RECHECK -- ISSUE WITH TUPLES
(class main
  (method int foo ()
     (begin
        (throw "me not in try-catch statement")
        (print "hi")
     )
  )
  (method void main ()
    (begin
        (print (call me foo))
        (print "miss me")
    )
  )
)

# throw statement's parameter must be a string (string exception value) -- TYPE ERROR
(class main
  (method void main ()
    (throw 1)
  )
)

# catch statement throws an exception -- exception variable is updated (new one in each scope)
(class main
  (method void main ()
    (try
        (begin
            (print "try line 1")
            (throw "outer try's throw")
        )
        (try
            (begin 
              (print "try line 2")
              (print "caught the: " exception)
              (throw "inner try's throw")
            )
            (print "caught the: " exception)
        )
    )
  )
)

# catch statement's substatement throws exception -- still works ^
(class main
  (method void main ()
    (try
        (begin
            (print "try line 1")
            (throw "outer try's throw")
        )
        (begin
            (try
                (begin 
                (print "try line 2")
                (print "caught the: " exception)
                (throw "inner try's throw")
                )
                (print "caught the: " exception)
            )
        )
    )
  )
)

# from spec
(class main
 (method void foo ()
   (while true
     (begin
       (print "argh")
       (throw "blah")
       (print "yay!")
     )
   )
 )

 (method void bar ()
  (begin
     (print "hello")
     (call me foo)
     (print "bye")
  )
 )

 (method void main ()
   (begin
     (try
       (call me bar)
       (print exception)
     )
     (print "woot!")
   )
 )
)

# catch block of outer try is not ran because the exception its nested try threw is caught
(class main
  (method void main ()
    (try
        (try
            (throw "outer try's throw")
            (print "sike")
        )
        (begin
            (try
                (print "try line 2")
                (print "caught the: " exception)
            )
        )
    )
  )
)

# from spec -- output == quack; if running the last call statement, output == NAME ERROR
(tclass Foo (field_type)
  (method void chatter ((field_type x)) 
    (call x quack)         # line A
  )
  (method bool compare_to_5 ((field_type x)) 
    (return (== x 5))
  )
)

(class Duck
 (method void quack () (print "quack"))
)

(class main
(field Foo@Duck t1)
(field Foo@int t2)
(method void main () 
    (begin
        (set t1 (new Foo@Duck))	# works fine
        (set t2 (new Foo@int))		# works fine

        (call t1 chatter (new Duck))	# works fine - ducks can talk
        (call t2 compare_to_5 5)  	# works fine - ints can be compared
        #(call t1 chatter 10)  # generates a NAME ERROR on line A
    )
)
)

# from spec -- further clarifications -- 1 NAME ERROR
(tclass Foo (field_type)
  (method void chatter ((field_type x)) 
    (call x quack)))

(class Duck
  (method void quack () 
    (print "quack")))
(class main
  (field Foo@Duck t1)
    (method void main () 
      (begin
        (set t1 (new Foo@Duck))
        (call t1 chatter 5) #generates a name error
)))

# from spec -- further clarifications -- 2 TYPE ERROR
(tclass Foo (field_type)
  (method void chatter ((field_type x)) 
    (call x quack))) #error generated here

(class Duck
  (method void quack () 
    (print "quack")))
(class main
  (field Foo@Duck t1)
    (method void main () 
      (begin
        (set t1 (new Foo@int)) #changed type of t1
        (call t1 chatter 5) #generates a type error, mismatch between Foo@Duck and Foo@int
)))

# from spec -- further clarifications -- 3 TYPE ERROR
(tclass Foo (field_type)
  (method void compare_to_5 ((field_type x)) 
    (return (== x 5)) #== operator applied to two incompatible types
  )
)

(class Duck
  (method void quack () 
    (print "quack")))
(class main
  (field Foo@Duck t1)
    (method void main () 
      (begin
        (set t1 (new Foo@Duck))
        (call t1 compare_to_5 (new Duck)) #type error generated
)))

# from spec -- exception handling
(class main
 (method void foo ()
   (begin
     (print "hello")
     (throw "I ran into a problem!")
     (print "goodbye")
   )
 )

 (method void bar ()
   (begin
     (print "hi")
     (call me foo)
     (print "bye")
   )
 )

 (method void main ()
  (begin
    (try
	  # try running the a statement that may generate an exception
       (call me bar)      	  
       # only run the following statement if an exception occurs
       (print "I got this exception: " exception)  
    )
    (print "this runs whether or not an exception occurs")
  )
 )
)

# from spec -- class templates; ouptut == quack\nhello
(tclass my_generic_class (field_type)
  (method void do_your_thing ((field_type x)) (call x talk))
)

(class duck
 (method void talk () (print "quack"))
)

(class person
 (method void talk () (print "hello"))
)

(class main
  (method void main ()
    (let ((my_generic_class@duck x null)
          (my_generic_class@person y null))
      # create a my_generic_class object that works with ducks
      (set x (new my_generic_class@duck))
      # create a my_generic_class object that works with persons
      (set y (new my_generic_class@person))
      (call x do_your_thing (new duck))
      (call y do_your_thing (new person))
    )
  )
)

# 6/2 -- another test case; output ==> i threw
(class main

 (method string bar ()
  (try
       (throw "i threw")
       (return exception)
  )
 )

 (method void main ()
    (print (call me bar))
  )

)

# 6/4 or 6/5 tbh lol
# from vchinn lol: test_vexcept2.brewin -- CALL EXPRESSION THROWS UNCAUGHT EXCEPTION -- RUN CATCH STATEMENT
(class main
 (field int c 0)
 
 (method int foo () 
  (begin
   (set c (+ c 1))
    (call me foo2)
   )
 )
 
 (method int foo2 () 
  (begin
   (throw "beh")
   )
 )
 (method void main ()
  (begin
    (try
       (begin 
        (print (+ 1 (call me foo)))
        (print "def"))
       (print exception)
    )
  )
 )
)

# from vchinn lol: test_vexcept11.brewin -- CALL EXPRESSION THROWS UNCAUGHT EXCEPTION
# even if a call expression calls method from another class, uncaught exception propagated to the class that called it
(class Robot 
 (field int c 0)
 
(method int foo () 
    (call me foo2)
 )
  
  (method bool errorSnek () 
    (throw "snek")
 )
 
 
 (method int foo2 () 
  (begin
      (try
       (call me foo4)
       (begin (print exception) 
       (if (== 1 1) 
         (let ((int x 0))
            (while (call me errorSnek)
              (begin 
                (if (== 5 x) (throw "bah") (print "nay")) 
                (set x (+ x 1))
              )
            )
         )
         (print "nuu")
        )
       ) 
    )

   )
 )
 (method int foo4 () 
   (throw "beh")
 )
)

(class Dog inherits Robot
  (method void m () ())
)
(class main

 (method void main ()
  (begin
    (try
       (begin (print "abc") (print (+ 1 (call (new Dog) foo)))  (print "def"))
       (print exception)
    )
  )
 )
)

# from vchinn lol: test_vexcept12.brewin -- CALL EXPRESSION
# while statement's conditional is the reseult of a call expression with uncaught exception 
(class Robot 
 (field int c 0)
 
(method int foo () 
  (begin
   (set c (+ c 1))
    (call me foo2)
   )
 )
 
  (method int foo2 () 
  (begin
    (call me foo3)
   )
 )
 
  
  (method bool errorSnek () 
  (begin
    (throw "snek")
   )
 )
 
 
 (method int foo3 () 
  (begin
      (try
       (call me foo4)
       (begin (print exception) 
       (if (== 1 1) 
         (let ((int x 0))
           (try 
            (while (call me errorSnek)
              (begin 
                (if (== 5 x) (throw "bah") (print "nay")) 
                (set x (+ x 1))
              )
            )
            (print exception x))
         )
         (print "nuu")
        )
       ) 
    )

   )
 )
 (method int foo4 () 
  (begin
  
   (throw "beh")
   )
 )
)

(class Dog inherits Robot
  (method void m () ())
)
(class main

 (method void main ()
  (begin
    (try
       (begin (print "abc") (print (+ 1 (call(new Dog) foo)))  (print "def"))
       (print exception)
    )
  )
 )
)

# from vchinn lol: test_vexcept13.brewin -- CALL EXPRESSION
# the throw expression has a call expression that has an uncaught exception
(class Robot 
 (field int c 0)
 
(method int foo () 
  (begin
   (set c (+ c 1))
    (call me foo2)
   )
 )
 
  (method int foo2 () 
  (begin
    (call me foo3)
   )
 )
 
    (method string hee () 
  (begin
    (throw "heehee")
   )
 )
 
  (method bool errorSnek () 
  (begin
    (throw (+ "snek" (call me hee)))
   )
 )
 
 
 (method int foo3 () 
  (begin
                 (try 
            (while (call me errorSnek)
              (begin 
                (if (== 5 x) (throw "bah") (print "nay")) 
                (set x (+ x 1))
              )
            )
            (print exception))

   )
 )
 (method int foo4 () 
  (begin
  
   (throw "beh")
   )
 )
)

(class Dog inherits Robot
  (method void m () ())
)
(class main

 (method void main ()
  (begin
    (try
       (begin (print "abc") (print (+ 1 (call(new Dog) foo)))  (print "def"))
       (print exception)
    )
  )
 )
)

# from vchinn again lol: test_except13.brewin -- CALL EXPRESSION
# passing in result of call expression to initialize parameter ==> if call expression has uncaught exception, then parameter initialization should fail
(class main
 (method int foo () 
   (throw "blah")
 )
 (method int bar ((int x)) 
   (print x)
 )

 (method void main ()
  (begin
    (try
       (call me bar (call me foo))
       (print exception)
    )
  )
 )
)