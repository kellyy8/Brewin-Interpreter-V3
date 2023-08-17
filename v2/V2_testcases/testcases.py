# DUPLICATE FIELD NAMES  --> error: Fields cannot share the same name.
(class main
    (field string n "one")
    (field int n 1)
    (method void main ()
      (print "hello")
    )
)

# FIELD INIT == FIELD TYPE ≠ INIT_VAL TYPE
(class main
    (field string s 1)
    (method void main ()
      (print "hello")
    )
)

# REASSIGNMENT - set statement (primitive types match)
(class main
    (field string s "one")
    (field int i 1)
    (method void main ()
      (begin (set i 5) (print i))
    )
)

# REASSIGNMENT - set statement (primitive types DONT match) -- error
(class main
    (field string s "one")
    (field int i 1)
    (method void main ()
      (begin (set i "wrong") (print i))
    )
)

# from spec / barista
(class main
    (method int value_or_zero ((int q))
      (begin
        (if (< q 0)
          (print "q is less than zero")
          (return q) # else case
        )
       )
    )
    (method void main ()
      (begin
        (print (call me value_or_zero 10))  # prints 10
        (print (call me value_or_zero -10)) # prints 0
      )
    )
  )

# INPUTI/INPUTS
(class main
    (field string s "one")
    (method void main ()
      (begin (print s) (inputs s) (print s))
    )
)

(class main
    (field int i 5)
    (method void main ()
      (begin (print i) (inputi i) (print i))
    )
)

# from spec under 'local variables' section
(class main
 (method void foo ((int x))
   (begin
     (print x)  					# Line #1: prints 10
     (let ((bool x true) (int y 5))
       (print x)					# Line #2: prints true
       (print y)					# Line #3: prints 5
     )
     (print x)					# Line #4: prints 10
   )
 )
 (method void main ()
   (call me foo 10)
 )
)

# Check field initialization & get_const_or_var_val()
(class main
    (field person p null)
    (field int i 1)
    (field string s "hello world")
    (field bool b true)
    (method void main ()
      (begin (set p (new person)) (print i s b))
    )
)

(class person (method void foo () (print "food")))

# RETURNED VALUES & DEFAULT RETURN VALUES (TYPE CHECKING) ----------------------------------------------------------
# returned values ==> void function returns values (type error) (incorrectness)
(class main
    (field int i 1)
    (field string s "hello world")
    (field bool b true)

    (method void main ()
      (call me foo)
    )

    (method void foo ()
      (return 5)
    )
)

# returned values -- void function does not return value (correctness) -- (nothing)
(class main
    (field int i 1)
    (field string s "hello world")
    (field bool b true)

    (method void main ()
      (call me foo)
    )

    (method void foo ()
      (return)
    )
)

# returned values -- non void functionn did not return value (return default value) -- 0
(class main
    (field int i 1)
    (field string s "hello world")
    (field bool b true)

    (method void main ()
      (print (call me foo))
    )

    (method int foo ()
      (return)
    )
)

# returned values -- non void function has no return statement (return default value: 0, "", false, null)
(class main
    (field int i 1)
    (field string s "hello world")
    (field bool b true)

    (method void main ()
      (print (call me foo))
    )

    (method int foo ()
      (print "nothing")
    )
)

(class person (method void foo () (print "food")))

# default returns:
(class main
    (field int i 1)
    (field string s "hello world")
    (field bool b true)
    (field person p null)

    (method void main ()
      (begin (print (call me default_int))
             (print (call me default_string))
             (print (call me default_boolean))
             (print (call me default_person))
      )
    )

    (method int default_int ()
      (print "int default")
    )

    (method string default_string ()
      (print "string default")
    )
    
    (method bool default_boolean ()
      (print "bool default")
    )
    
    (method person default_person ()
      (print "person default")
    )
)

(class person (method void foo () (print "food")))

# returned values ==> non void function RETURNS compatible values
# f1, f2, f3 have primitive return type & they all return primitive type values (constants)
# foo returns a Person object ==> can return 'null'
# bar returns a Dog object ==> can return Dog object
(class main
    (field person p null)
    (field dog d null)
    (method void main ()
      (begin 
        (print (call me f1) " " (call me f2) " " (call me f3))
        (set p (new person))
        (print (call p foo))
        (set d (new dog))
        (call d bar d)        # trace through to check that returned value is Dog object
      )
    )

    (method int f1 () (return 5))
    (method string f2 () (return "five"))
    (method bool f3 () (return true))
)

(class person (method person foo () (return null)))
(class dog (method dog bar ((dog d1)) (return d1)))

# returned values ==> function has return type INT & returns compatible/incompatible values
# i1 == success; i2 to i5 == failure
(class main
    (field person p null)
    (method void main ()
      (begin     
        (set p (new person)) 
           
        (print (call me i1))
        #(print (call me i2))
        #(print (call me i3))
        #(print (call me i4))
        #(print (call me i5))
      )
    )

    (method int i1 () (return 5))
    (method int i2 () (return "five"))
    (method int i3 () (return true))
    (method int i4 () (return null))
    (method int i5 () (return p))
)

(class person (method person foo () (return null)))    # random func defs

# returned values ==> function has return type STRING & returns compatible/incompatible values
# s1 == success; s2 to s5 == failure
(class main
    (field person p null)
    (method void main ()
      (begin     
        (set p (new person)) 
           
        (print (call me s1))
        #(print (call me s2))
        #(print (call me s3))
        #(print (call me s4))
        #(print (call me s5))
      )
    )

    (method string s1 () (return "five"))
    (method string s2 () (return 5))
    (method string s3 () (return true))
    (method string s4 () (return null))
    (method string s5 () (return p))
)

(class person (method person foo () (return null)))    # random func defs

# returned values ==> function has return type BOOL & returns compatible/incompatible values
# b1 == success; b2 to b5 == failure
(class main
    (field person p null)
    (method void main ()
      (begin     
        (set p (new person)) 
           
        (print (call me b1))
        #(print (call me b2))
        #(print (call me b3))
        #(print (call me b4))
        #(print (call me b5))
      )
    )

    (method bool b1 () (return true))
    (method bool b2 () (return 5))
    (method bool b3 () (return "five"))
    (method bool b4 () (return null))
    (method bool b5 () (return p))
)

(class person (method person foo () (return null)))    # random func defs

# returned values ==> function has return type PERSON (object reference) & returns compatible/incompatible values
# p1 and p2 == success; p3 to p6 == failure
(class main
    (field person p null)
    (field dog d null)
    (method void main ()
      (begin     
        (set p (new person)) 
        (set d (new dog))
           
        (print (call me p1))
        (print (call me p2))
        #(print (call me p3))
        #(print (call me p4))
        #(print (call me p5))
        #(print (call me p6))
      )
    )

    (method person p1 () (return null))
    (method person p2 () (return p))
    (method person p3 () (return 5))
    (method person p4 () (return "five"))
    (method person p5 () (return true))
    (method person p6 () (return d))
)

(class person (method person foo () (return null)))    # random func defs
(class dog (method dog bar ((dog d1)) (return d1)))    # random func defs

# return and set polymorphism
(class main
    (field person p null)
    (field student s null)
    (field teacher t null)
    (method void main ()
      (begin     
        (set p (new person)) 
        (set p (new student))      # ok
        #(set s (new teacher))     # error
        #(set s (new person))      # error

        (set s (new student))
        (set t (new teacher))
           
        #(print (call me p1))
        #(print (call me p2))
        #(print (call me p7))
        #(print (call me p8))

      )
    )

    (method person p1 () (return null))
    (method person p2 () (return p))
    (method person p7 () (return s))
    (method person p8 () (return t))
)

(class person (method person foo () (return null)))    # random func defs
(class student inherits person (method person foo () (return null)))    # random func defs
(class teacher inherits person (method person foo () (return null)))    # random func defs

# check in/correctness -- set polymorphism (where null is returned from method call)
(class main
    (field person p null)
    (field student s null)

    (method void main ()
      (begin
        (set p (new person))
        (set s (new student))
        
        #(set s (call me returns_person))      ## type error: student is not person null
        (set s (call me returns_tp))          ## okay: teachers_pet is student null
      )
    )

    (method person returns_person ()
      (return null)
    )
    
    (method teachers_pet returns_tp ()
      (return null)
    )
        
    (method void takes_stud ((student stud)) (print "takes_stud"))
)

(class person (method void foo () (print "food")))
(class student inherits person (method void foo () (print "food")))
(class teachers_pet inherits student (method void foo () (print "food")))

# call method -- target object != valid reference (null) -----------------------------------------------------
(class person
  (method void foo ((int x)) (print x))
)

(class main
 (field person obj null)
 (method void main ()
   (call obj foo 5)
 ) 
)

# pass by value (apham) ---------------------------------------------------------------------------------------
(class main
  (field other_class other null)
  (field int x 5)
  (method void main ()
    (begin
      (set other (new other_class))
      (call other foo x)
      (print x)
    )
  )
)

(class other_class
  (field int a 10)
  (method void foo ((int q))
    (begin
      (set q 10)
      (print q)
    )
  )
)

# PARAMETER PASSING / ARGUMENT ASSIGNMENT (TYPE CHECKING) -----------------------------------------------------------
# check correctness ==> (primitives to primitives & object references to same object refences or null) (no poly yet)
(class main
    (field person p null)
    (field int i 1)
    (field string s "hello world")
    (field bool b true)

    (method void main ()
      (begin (call me primitives i s b) (set p (new person)) (call me obj_refs p null) )
    )

    (method void primitives ((int i1) (string s1) (bool b1))
      (print "checked primitives!")
    )

    (method void obj_refs ((person p1) (person p2))
      (print "checked obj_refs!")
    )
)

(class person (method void foo () (print "food")))

# check incorrectness ==> parameter type: INT
# passing in string, bool, or class for an int
(class main
    (field person p null)
    
    (method void main ()
      (begin
        (set p (new person))
        
        (call me take_int 1)
        #(call me take_int "one")
        #(call me take_int true)
        #(call me take_int null)
        #(call me take_int p)
      )
    )

    (method void take_int ((int a))
      (print "received an integer!")
    )
)

(class person (method void foo () (print "food")))

# check incorrectness ==> parameter type: STRING
# passing in int, bool, or class for a string
(class main
    (field person p null)
    
    (method void main ()
      (begin
        (set p (new person))
        
        (call me take_str "one")
        #(call me take_str 1)
        #(call me take_str true)
        #(call me take_str null)
        #(call me take_str p)
      )
    )

    (method void take_str ((string a))
      (print "received a string!")
    )
)

(class person (method void foo () (print "food")))

# check incorrectness ==> parameter type: BOOL
# passing in int, string, or class for a boolean
(class main
    (field person p null)
    
    (method void main ()
      (begin
        (set p (new person))
        
        (call me take_bool true)
        #(call me take_bool 1)
        #(call me take_bool "one")
        #(call me take_bool null)
        #(call me take_bool p)
      )
    )

    (method void take_bool ((bool a))
      (print "received a boolean!")
    )
)

(class person (method void foo () (print "food")))

# check incorrectness ==> parameter type: PERSON (class; object reference)
# passing in int, string, bool, or diff/unrelated class for 'person' class
(class main
    (field person p null)
    (field dog d null)
    
    (method void main ()
      (begin
        (set p (new person))
        (set d (new dog))

        (call me take_person null)
        (call me take_person p)
        #(call me take_person 1)
        #(call me take_person "one")
        #(call me take_person true)
        #(call me take_person d)
      )
    )

    (method void take_person ((person a))
      (print "received a Person object!")
    )
)

(class person (method void foo () (print "food")))     # random func defs
(class dog (method dog bar ((dog d1)) (return d1)))    # random func defs

# check in/correctness ==> parameter passing with polymorphism (where null is returned from method call)
(class main
    (field person p null)
    (field student s null)

    (method void main ()
      (begin
        (set p (new person))
        (set s (new student))
        
        #(call me takes_stud (call me returns_person))     ## null type tag == person (person is not student)
        (call me takes_stud (call me returns_tp))          ## null type tag == student (teachers_pet is student)
      )
    )

    (method person returns_person ()
      (return null)
    )
    
    (method teachers_pet returns_tp ()
      (return null)
    )
        
    (method void takes_stud ((student stud)) (print "takes_stud"))
)

(class person (method void foo () (print "food")))
(class student inherits person (method void foo () (print "food")))
(class teachers_pet inherits student (method void foo () (print "food")))

# FIELD INITIALIZATION -- TYPE CHECKING (correcness and incorrectness)
(class main
    (field int i1 1)
    #(field int i2 "one")
    #(field int i3 true)
    #(field int i4 null)
    
    (field string s1 "one")
    #(field string s2 1)
    #(field string s3 true)
    #(field string s4 null)
    
    (field bool b1 true)
    #(field bool b2 1)
    #(field bool b3 "one")
    #(field bool b4 null)
    
    (field person p1 null)
    #(field person p2 1)
    #(field person p3 "one")
    #(field person p4 true)
    
    (method void main ()
      (print "i called main. *sigh*")
    )
)

(class person (method void foo () (print "food")))     # random func defs

# Parameter passing with polymorphism
(class main
    (field person p null)
    (field student s null)
    (field teacher t null)
    
    (method void main ()
      (begin
        (set p (new person))
        (set s (new student))
        (set t (new teacher))

        (call me take_person null)
        (call me take_person p)
        (call me take_person s)
        (call me take_person t)

        (call me take_stud s)
        #(call me take_stud t)      # teacher is derived from person but not related to student
        #(call me take_stud p)      # person is not subclass of student
      )
    )

    (method void take_person ((person a))
      (print "received a Person object!")
    )

    (method void take_stud ((student a))
      (print "received a Student object!")
    )

)

(class person (method void foo () (print "food")))     # random func defs
(class student inherits person (method void foo () (print "food")))     # random func defs
(class teacher inherits person (method void foo () (print "food")))     # random func defs


# CHECK LOCAL VARIABLE ASSIGNMENT -----------------------------------------------------------------------------------
# correctness check: primitives to primitives, classes to classes/subclasses/null
(class main    
    (method void main ()
        (begin 
          (let ((int i1 1)
                (string s1 "one")
                (bool b1 true)
                (person p1 null))
                
                (print "VALID INITS")
          )
        )
    )
)

(class person (method void foo () (print "food")))     # random func defs
 
# incorrectness check
(class main    
    (field person p null)
    (field dog d null)
    (method void main ()
        (begin 
          (set p (new person))
          (set d (new dog))

          (let ((int i1 1)) (print "valid int"))
          #(let ((int i2 "one")) (print "invalid int"))
          #(let ((int i3 true)) (print "invalid int"))
          #(let ((int i4 null)) (print "invalid int"))
          #(let ((int i5 (new person))) (print "invalid int"))        # RUNTIME ERROR but i get 'invalid int'

          (let ((string s1 "one")) (print "valid string"))
          #(let ((string s2 1)) (print "invalid string"))
          #(let ((string s3 true)) (print "invalid string"))
          #(let ((string s4 null)) (print "invalid string"))
          #(let ((string s5 p)) (print "invalid string"))             # RUNTIME ERROR but i get "Variable holds values of type 'string', but value is of type 'int'."

          (let ((bool b1 true)) (print "valid boolean"))
          #(let ((bool b2 1)) (print "invalid boolean"))
          #(let ((bool b3 "one")) (print "invalid boolean"))
          #(let ((bool b4 null)) (print "invalid boolean"))
          #(let ((bool b5 p)) (print "invalid boolean"))              # RUNTIME ERROR but i get "Variable holds values of type 'bool', but value is of type 'int'."

          (let ((person p1 null)) (print "valid class"))
          #(let ((person p2 (new person))) (print "valid class"))     # RUNTIME ERROR but i get "Variable holds values of type 'class', but value is of type 'int'."
          #(let ((person p3 1)) (print "invalid class"))
          #(let ((person p4 "one")) (print "invalid class")) 
          #(let ((person p5 true)) (print "invalid class"))
          #(let ((person p6 d)) (print "invalid class"))              # RUNTIME ERROR but i get "Variable holds values of type 'class', but value is of type 'int'."
        )
    )
)

(class person (method void foo () (print "food")))     # random func defs
(class dog (method dog bar ((dog d1)) (return d1)))    # random func defs

# CHECK EVAL EXPRESSION (particularly all the comparison ops)--------------------------------------------------------
# COMPARING OBJECTS OF SAME CLASS (also checked that object references cannot be compared with primitives)
(class main
  (field person pp1 null)
  (field person pp2 null)

  (method void foo ((person p1) (person p2)) 
    (begin 
    (if (== p1 p2)   
      (print "same object")
      (print "diff object")
    )

    (if (== p1 null)   
      (print "p1 is null")
      (print "p1 is not null")
    )
    )
  )

 (method void main ()
  (begin
    (set pp1 (new person))
    (set pp2 pp1)
    (call me foo pp1 pp2)
  )
 )
)

(class person (method void foo () (print "food")))     # random func defs

# FROM V1 -- COMPARE BOOL
(class main
 (field bool t true)
 (field bool f false)
 (method void main ()
  (begin
   (print (== true true))
   (print (== false false))
   (print (== true false))
   (print (!= true false))
   (print (!= true true))
   (print (!= false false))
   (print (== (== t true) t))
   (print (== (== t false) f))
   (print (== (== f false) f))
   (print (!= (== t true) f))
   (print (!= (!= t false) t))
   (print (!= f (!= f true)))
  )
 )
)

# FROM V1 -- COMPARE INT
(class main
 (field int zero 0)
 (field int one 1)
 (field int two 2)
 (method void main ()
  (begin
   (print (< 0 1))
   (print (< 1 0))
   (print (> 1 0))
   (print (> 0 1))
   (print (<= 0 1))
   (print (<= 0 0))
   (print (<= 2 0))
   (print (>= 0 0))
   (print (>= 1 0))
   (print (>= 1 2))
   (print (== 1 1))
   (print (== 1 2))
   (print (!= 1 2))
   (print (!= 1 1))
   (print (< zero one))
   (print (< one zero))
   (print (> one zero))
   (print (> zero one))
   (print (<= zero one))
   (print (<= zero zero))
   (print (<= two zero))
   (print (>= zero zero))
   (print (>= one zero))
   (print (>= one two))
   (print (== one one))
   (print (== one two))
   (print (!= one two))
   (print (!= one one))
  )
 )
)

# FROM V1 -- COMPARE STRING
(class main
 (field string a "a")
 (field string b "b")
 (method void main ()
  (begin
   (print (< "a" "b"))
   (print (< "b" "a"))
   (print (> "b" "a"))
   (print (> "a" "b"))
   (print (<= "a" "b"))
   (print (<= "a" "a"))
   (print (<= "c" "a"))
   (print (>= "a" "a"))
   (print (>= "b" "a"))
   (print (>= "b" "c"))
   (print (== "b" "b"))
   (print (== "b" "c"))
   (print (!= "b" "c"))
   (print (!= "b" "b"))
   (print (< a b))
   (print (< b a))
   (print (> b a))
   (print (> a b))
   (print (<= a b))
   (print (<= a a))
   (print (<= "c" a))
   (print (>= a a))
   (print (>= b a))
   (print (>= b "c"))
   (print (== b b))
   (print (== b "c"))
   (print (!= b "c"))
   (print (!= b b))
  )
 )
)

# FROM V1 -- COMPARE NULL (output: yes yes)
(class main
 (field person x null)
 (method void main ()
   (begin
     (if (== x null) (print "yes"))
     (set x (new person))
     (if (!= x null) (print "yes"))
   )
 )
)

(class person (method void foo () (print "food")))     # random func defs

# FROM V1 -- BOOL_EXPR
(class main
 (field bool t true)
 (field bool f false)
 (method void main ()
   (begin
     (print (| true false))
     (print (& true false))
     (print (! true))
     (print (| t f))
     (print (& t f))
     (print (! t))
     (print (| (== t true) false))
     (print (& (== t true) false))
     (print (! (== t true)))
   )
 )
)

# FROM V1 -- INT OPS
(class main
 (method void main ()
  (begin
		(print (+ 100 2))
    (print (- 100 2))
    (print (* 100 2))
    (print (/ 100 2))
    (print (% 100 6))
		(print (+ (+ (+ (+ 12 13) 25) 50) (* 1 2)))
    (print (- (- 200 100) 2))
    (print (* (% 5100 500) 2))
    (print (/ (* (* 4 5) 5) 2))
    (print (% (/ 1000 10) (* 2 3)))
  )
 )
)

# FROM V1 -- STRING OPS
(class main
 (method void main ()
  (begin
		(print (+ "abc" "def"))
		(print (+ (+ "ab" "c") (+ "d" "ef")))
  )
 )
)

# comparing object references (correctness and incorrectness) (same class, subclasses, unrelated classes)
(class main
    (field person p1 null)
    (field person p2 null)
    (field dog d null)
    (field student s null)
    (field teacher t null)
    (method void main ()
      (begin 
        (set p1 (new person))
        (set p2 p1)
        (set d (new dog))
        (set s (new student))
        (set t (new teacher))

        (print (== p1 p2))    # true
        (print (!= p1 p2))    # false
        #(print (== d p1))    # type error
        #(print (!= d p2))    # type error
        (print (== p1 s))     # false
        (print (== s p1))     # false
        (print (!= p2 s))     # true
        (print (!= s p2))     # true
        (print (== null p1))  # false
        (print (!= null p2))  # true
        (print (== d null))   # false
        (print (!= s null))   # true

        #(print (== s t))      $ type error (unrelated types despite both derived from person)
        #(print (!= s t))      $ type error (unrelated types despite both derived from person)
      )
    )
)

(class person (method string foo () (return "person")))
(class student inherits person (method string foo () (return "student")))
(class teacher inherits person (method string foo () (return "teacher")))
(class dog (method dog bar ((dog d1)) (return d1)))


# bro idk anymore
(class main
    (field person p null)
    (field student s null)
    (field dog d null)

    (method void main ()
      (begin
        (set p (new person))
        (set s (new student))
        
        (set s (call me returns_tp))      # s = null object of type tp
        (set d s)                         # type error: type mismatch dog and student
      )
    )

    (method person returns_person ()
      (return null)
    )
    
    (method teachers_pet returns_tp ()
      (return null)
    )
        
    (method void takes_stud ((student stud)) (print "takes_stud"))
)

(class person (method void foo () (print "food")))
(class student inherits person (method void foo () (print "food")))
(class teachers_pet inherits student (method void foo () (print "food")))
(class dog (method void foo () (print "food")))